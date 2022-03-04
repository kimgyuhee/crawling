from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
import time
import sys
import os # 폴더 집어 넣기 위해
# import xlwt
import pandas as pd
import re # 정규 표현식을 사용하기 위한 모듈 선언


# 키워드 입력받기 -> O
def query_input() :
    # 크롤링할 키워드를 입력받기 위한 반복문 생성
    while True :
        try :
            query_txt = input("크롤링할 키워드는 무엇입니까? : ")
        except Exception as e:
            print("에러발생")
            print("원인 : ", e)
        else :
            if(query_txt == "") :
                print("*** 아무것도 입력되지 않았습니다. ***")
                print("*** 다시 입력해주세요. ***")
                continue
            else :
                break
    # 크롤링할 건수를 입력받기 위한 반복문 생성
    while True :
        try :
            cnt = int(input('크롤링할 건수 : '))
        except ValueError:
            print("*** 숫자를 입력해주세요 ***")
            continue
        else :
            if(cnt < 1) :
                print('*** 자연수를 입력해주세요. ***')
                continue
            break

    return query_txt, cnt
                

# 네이버 브라우저 제어하기
def naver_webdriver_exe() :
    # 크롬 드라이버를 사용해서 웹 브라우저를 실행합니다.
    # path = "C:/web_driver/chromedriver.exe"
    driver = webdriver.Chrome()
    driver.get("https://www.naver.com/")
    time.sleep(2) # 2초 기다리기
    return driver


# 네이버 페이지에서 키워드 검색하기
def naver_keyword_search(driver, keyword) :
    element = driver.find_element_by_id('query')
    time.sleep(2)
    element.send_keys(keyword)
    time.sleep(1)
    element.send_keys(Keys.ENTER)


# 블로그 페이지 클릭하는 함수 생성
def blog_area_click() :
    full_html = driver.page_source
    soup = BeautifulSoup(full_html, 'html.parser')
    driver.find_element_by_link_text('VIEW').send_keys(Keys.ENTER)
    time.sleep(0.5)
    driver.find_element_by_link_text('기본뷰').send_keys(Keys.ENTER)
    
# 블로그 내용 추출하기
def blog_crawlling(driver, cnt) :
    
    search_result = True # 검색 결과가 존재하는지 확인하는 변수 생성
    SCROLL_PAUSE_SEC = 1
    
    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")
    count = 0
    
    titles = [] # 추출한 제목 저장할 리스트 생성
    contents = [] # 추출한 내용 저장할 리스트 생성
    addrs = [] # 블로그 주소 저장할 리스트 생성
    dates = [] # 작성한 날짜 저장할 리스트 생성
    tags = [] # 태그 내용 저장할 리스트 생성하기
    num = []
    
    # 반복문을 돌면서 입력받은 갯수만큼 내용 크롤링하기
    while (count != cnt) :
        
        full_html = driver.page_source
        soup = BeautifulSoup(full_html, 'html.parser')
        try :
            blog_lists = soup.find('ul', 'lst_total').find_all('li', 'bx')
        except AttributeError :
            try :
                blog_lists = soup.find('ul', 'timeline_list').find_all('div', '_svp_item')
            except AttributeError :
                print('*** 검색 결과가 없습니다. ***')
                search_result = False
                break
                
        for i in blog_lists :
            # 현재 크롤링하는 갯수 저장하기
            count +=1
            num.append(count)
            print('번호 : ', str(count))
          
            # 각 부분마다 try를 해주는 이유는 html 형식이 2가지가 존재하기 때문이다.
            # 블로그 주소 추출하기
            try :
                # addr = i.find('div', 'total_info').find('span', 'elss etc_dsc_inner').find('a').get_text()
                addr = i.find('span', 'elss etc_dsc_inner').find('a').get_text()
            except AttributeError :
                # addr = i.find('div', 'total_info').find('span', 'source_txt name').get_text()
                addr = i.find('span', 'source_txt name').get_text()
            finally :
                addr = addr.strip()
                addrs.append(addr)
                print('블로그 주소 : ',addr )

            # 작성한 날짜 추출하기
            try :
                date = i.find('span', 'sub_time sub_txt').get_text()
            except AttributeError :
                date = i.find('span', 'source_txt date').get_text()
            finally :
                date = date.strip()
                dates.append(date)
                print('작성한 날짜 : ', date)

            # 제목 추출하기
            try :
                title = i.find('a', 'api_txt_lines total_tit _cross_trigger').get_text()
            except AttributeError :
                title = i.find('a', 'api_txt_lines total_tit').get_text()
            finally :
                title = title.strip()
                titles.append(title)
                print('제목 : ', title)
            
            # 내용 부분 추출하기
            content = i.find('div','total_group').find('div', 'total_dsc_wrap')
            content = content.find('a', 'total_dsc').get_text()
            content = content.strip()
            contents.append(content)
            print('내용 : ', content)

            # 태그 추출하기
            try :
                tags_list = i.find('div', 'total_tag_area').find_all('a')
            except AttributeError :
                show_tags = '태그 없음'
                tags.append(['없음'])
            else :
                tag = []
                for t in tags_list :
                    tag.append(t.get_text())
                show_tags = " ".join(tag)
                show_tags = show_tags.strip()
                tags.append(tag) 
            finally :
                print('태그 :', show_tags)
            print('\n')
            
            time.sleep(0.5)
            
            if(count == cnt) :
                return num, titles, contents, addrs, dates, tags, search_result
            
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)
        print('==== 스크롤 내려가는중 ===== ')

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
    return num, titles, contents, addrs, dates, tags, search_result

# 입력한 경로에 폴더가 존재하는지 확인하고 없으면 생성해주기
def check_path_exists(path) :
    if(os.path.isdir(path)) : # 파일이 존재한다면 입력받은 경로에 저장
        print('입력하신 경로가 존재하여 %s 폴더에 저장하겠습니다.' %path)
    else : # 파일이 존재하지 않는다면 폴더를 생성 후 저장
        os.makedirs(path)
        print('입력하신 경로가 존재하지 않아 %s 폴더를 만들어 저장하겠습니다' %path)
        
        
# 파일 경로 입력받는 함수
def input_path() :
    path = 'C:\\crawlling\\happy\\'
    while True :
        try :
            new_path = input('저장될 기본 경로는 C:\\crawlling\\happy\\ 입니다.\n다른 경로로 입력하시겠습니까?(Y, N) -> ')
        except Exception as e :
            print('에러발생')
            print('원인 :', e)
            continue
        else :
            if(new_path.upper() == 'Y') :
                try :
                    path = input('\n저장할 경로를 입력해주세요.')
                except Exception as e :
                    print('에러발생')
                    print('원인 : ', e)
                    print('*** 기본 경로로 저장됩니다. ***')
                    break
                else :
                    last_str_index = len(path)-1
                    if(path[last_str_index] != '\\') :
                        print('*** 파일 경로 마지막에는 \\를 꼭 붙여줘야합니다. ***')
                        path = path+'\\'
                    check_path_exists(path)
                    break
                        
            elif(new_path.upper() == 'N') :
                print('{}에 파일이 저장됩니다.'.format(path))
                break
            else :
                print('*** Y와 N중에 입력해주세요. ***')
                continue
        finally :
            print('\n')

    return path
                 

# 텍스트 파일이름 입력받는 함수 생성
def input_txt_name(path) :
    while True :
        try :
            f_name = input("txt 파일의 이름을 지정해주세요.(경로 X, 확장자 X) > ")
        except Exception as e :
            print('에러발생')
            print('원인 : ', e)
            continue
        else :
            if( '.txt' in f_name) :
                print('*** 파일의 이름만 입력해주세요 ***')
                continue
            else :
                if( f_name == "") :
                    print('*** 아무것도 입력되지 않았습니다. ***')
                    print('*** 다시 입력해주세요. ***')
                    continue
                else :
                    break
        finally :
            print('\n')
                
    f_name = path+f_name+'.txt'
    return f_name

# cvs 파일이름 입력받는 함수 생성
def input_csv_name(path) :
    while True :
        try :
            fc_name = input("csv 파일의 이름을 지정해주세요.(경로 X, 확장자 X) > ")
        except Exception as e :
            print('에러발생')
            print('원인 : ', e)
            continue
        else :
            if( '.csv' in fc_name) :
                print('파일의 이름만 입력해주세요')
                continue
            else :
                if( fc_name == "") :
                    print('아무것도 입력되지 않았습니다.')
                    print('다시 입력해주세요.')
                    continue
                else :
                    break
        finally :
            print('\n')
                
    fc_name = path+fc_name+'.csv'
    return fc_name


# xls 파일이름 입력받는 함수 생성
def input_xls_name(path) :
    while True :
        try :
            fx_name = input("xls 파일의 이름을 지정해주세요.(경로 X, 확장자 X) > ")
        except Exception as e :
            print('에러발생')
            print('원인 : ', e)
            continue
        else :
            if( '.xls' in fx_name) :
                print('*** 파일의 이름만 입력해주세요 ***')
                continue
            else :
                if( fx_name == "") :
                    print('*** 아무것도 입력되지 않았습니다. ***')
                    print('*** 다시 입력해주세요. ***')
                    continue
                else :
                    break
        finally :
            print('\n')
                
    fx_name = path+fx_name+'.xls'
    return fx_name

# 텍스트 형태로 파일에 저장하기 위한 함수
def write_txt(txt_path, num, t1itles, contents, addrs, dates, tags):
    f = open(txt_path, 'a', encoding='UTF-8')
    time.sleep(1)
    
    for i in range(0,len(num)) :
        f.write('번호 : ' + str(num[i]).strip() + '\n')
        f.write('제목 : ' + str(titles[i]).strip() + '\n')
        f.write('내용 : ' + str(contents[i]).strip() + '\n')
        f.write('출처 : ' + str(addrs[i]).strip() + '\n')
        f.write('작성일 : ' + str(dates[i]).strip() + '\n')
        tag =" ".join(tags[i])
        f.write('태그 : ' + str(tag).strip() + '\n')
        f.write('\n')
        
    f.close()
    print('txt 파일 저장 경로 : %s' %txt_path)

    print("요청하신 데이터 수집 작업이 정상적으로 완료되었습니다.")

# 엑셀 형태로 파일에 저장하기 위한 함수
def write_xls(xls_path, num, titles, contents, addrs, dates, tags) :

    blog_content = pd.DataFrame()
    blog_content['번호'] = num
    blog_content['제목'] = titles
    blog_content['내용'] = contents
    blog_content['출처'] = addrs
    blog_content['작성한 날짜'] = dates
    blog_content['태그'] = tags
    
    # 엑셀 형태로 저장하기
    blog_content.to_excel(xls_path , index=False)
    print('xls 파일 저장 경로 : %s' %xls_path)

    print("요청하신 데이터 수집 작업이 정상적으로 완료되었습니다.")

    
    
# csv 형태로 파일에 저장하기 위한 함수
def write_csv(csv_path, num, titles, contents, addrs, dates, tags) :
    
    blog_content = pd.DataFrame()
    blog_content['번호'] = num
    blog_content['제목'] = titles
    blog_content['내용'] = contents
    blog_content['출처'] = addrs
    blog_content['작성한 날짜'] = dates
    blog_content['태그'] = tags
    
    # csv 형태로 저장하기
    blog_content.to_csv(csv_path,encoding="utf-8-sig" , index=False)
    print('csv 파일 저장 경로 : %s' %csv_path)

    print("요청하신 데이터 수집 작업이 정상적으로 완료되었습니다.")
    

# 처음 크롤링을 시작할지 여부를 묻는 함수 생성 -> O
def show_crawlling_start_menu() :
    start = True
    while True :
        try :
            print()
            crawlling_start_menu = int(input('네이버 블로그 크롤링을 시작하시겠습니까?\n1.네  0.아니요 > '))
        except ValueError :
            print('숫자를 입력해주세요') # 문자나 엔터를 입력했을 시 예외처리
            continue
        else :
            if( crawlling_start_menu == 0 ) :
                start = False
                break
            elif (crawlling_start_menu == 1) :
                start = True
                break
            else :
                print('*** 1과 0중에 입력해주세요. ***')
                continue
    return start


# 크롤링한 내용을 저장할지 묻고 실행하는 함수 생성
def want_to_save_crawlling_content() :
     while True :
        try :
            store = int(input("크롤링한 내용을 저장하시겠습니까? 1.네 2.아니요 > "))
        except ValueError :
            print('문자 말고 1과 2중 숫자를 입력해주세요.')
            continue
        else :
            if( store == 1) :
                path = input_path() # 파일이 저장될 경로 입력 받기
            elif( store == 2) :
                break
            else :
                print('1또는 2 숫자 중에 입력해주세요.')
                continue
        finally :
            print('\n')
            
        try :
            save = int(input('메뉴 번호를 입력해주세요.\n1.txt 2.csv 3.xls  0.상위 메뉴로 이동 > '))
        except Exception as e :
            print('1,2,3.0 중에 입력하지 않아 에러 발생')
            print('원인 : ',e)
            print('크롤링 저장 여부로 이동합니다.')
            continue
        else :
            if (save == 1) : # txt형식으로 저장한다고 했을 경우 함수 호출해서 저장
                file = input_txt_name(path)
                write_txt(file, num, titles, contents, addrs, dates, tags)
                continue
            elif (save == 2) : # csv 형식으로 저장한다고 했을 경우 함수 호출해서 저장
                file = input_csv_name(path)
                write_csv(file, num, titles, contents, addrs, dates, tags)
                continue
            elif(save == 3) : # 엑셀 형식으로 저장한다고 했을 경우 함수 호출해서 저장
                file = input_xls_name(path)
                write_xls(file, num, titles, contents, addrs, dates, tags)
                continue
            elif (save == 0) : # 0을 입력했을때 다시 크롤링할지 묻기
                print(' ========== 상위 메뉴로 이동합니다. ========== ')
                break
            else : # 그 외의 숫자를 입력했을 경우 다시 입력받게 하기
                print('*** 제시된 숫자를 입력해주세요 ***')
                print('크롤링 저장 여부로 이동합니다.')
                continue
        finally :
            print('\n')

            
            
# 프로그램 실행 코드
while True :    
    start = show_crawlling_start_menu()
    print()
    if(start == True) :
        keyword, cnt = query_input()
        
        driver = naver_webdriver_exe() # 네이버 원격으로 열기
        naver_keyword_search(driver, keyword) # 네이버에서 키워드 입력한 후 이동하기
        blog_area_click() # 키워드 입력 후 블로그 부분 클릭하기
        num, titles, contents, addrs, dates, tags, search_result = blog_crawlling(driver, cnt) # 추출한 내용 반환받기
        
        if( search_result == True ) : # 검색 결과가 존재할 때 만 저장할지 묻기 위한 조건문 생성
            time.sleep(0.5)
            want_to_save_crawlling_content() # 크롤링한 내용 저장할지 묻는 함수 호출
            
    else :
        print('종료합니다.')
        driver.close()
        break