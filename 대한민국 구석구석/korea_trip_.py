from multiprocessing.connection import wait
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
import os # 폴더 집어 넣기 위해
import math
import xlwt
import pandas as pd
import re # 정규 표현식을 사용하기 위한 모듈 선언
import urllib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 키워드 입력받는 함수 생성
def input_keyword() :
    while True :
        try :
            query_txt = input('크롤링할 키워드 : ')
        except Exception as e :
            print('에러발생')
            print('원인 : ', e)
            continue
        else :
            if(query_txt == "") :
                print('아무것도 입력되지 않았습니다.')
                print('다시 입력해주세요.')
                continue
            else :
                break

    while True :
        try :
            cnt = int(input('크롤링할 건수 : '))
        except ValueError:
            print("*** 숫자를 입력해주세요 ***")
            continue
        else :
            break
    return query_txt, cnt
       

# 크롤링한 내용을 저장할지 묻고 실행하는 함수 생성
def want_to_save_crawlling_content() :
     while True :
        try :
            store = int(input("크롤링한 내용을 저장하시겠습니까? 1.네 2.아니요(종료) > "))
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
            save = int(input('메뉴 번호를 입력해주세요.\n1.txt 2.csv 3.xls  0.종료 > '))
        except Exception as e :
            print('1,2,3.0 중에 입력하지 않아 에러 발생')
            print('원인 : ',e)
            print('크롤링 저장 여부로 이동합니다.')
            continue
        else :
            if (save == 1) : # txt형식으로 저장한다고 했을 경우 함수 호출해서 저장
                file = input_txt_name(path)
                write_txt(file, num, title, dates, regions, views, contents)
                continue
            elif (save == 2) : # csv 형식으로 저장한다고 했을 경우 함수 호출해서 저장
                file = input_csv_name(path)
                write_csv(file, num, title, dates, regions, views, contents)
                continue
            elif(save == 3) : # 엑셀 형식으로 저장한다고 했을 경우 함수 호출해서 저장
                file = input_xls_name(path)
                write_xls(file, num, title, dates, regions, views, contents)
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

# 입력한 경로에 폴더가 존재하는지 확인하고 없으면 생성해주기
def check_path_exists(path) :
    if(os.path.isdir(path)) : # 파일이 존재한다면 입력받은 경로에 저장
        print('입력하신 경로가 존재하여 %s 폴더에 저장하겠습니다.' %path)
    else : # 파일이 존재하지 않는다면 폴더를 생성 후 저장
        os.makedirs(path)
        print('입력하신 경로가 존재하지 않아 %s 폴더를 만들어 저장하겠습니다' %path)


# 파일 경로 입력받는 함수
def input_path() :
    path = 'C:\\python_temp\\happy\\'
    while True :
        try :
            new_path = input('저장될 기본 경로는 {} 입니다.\n다른 경로로 입력하시겠습니까?(Y, N) -> '.format(path))
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
def write_txt(txt_path, num, title, dates, regions, views, contents):
    f = open(txt_path, 'a', encoding='UTF-8')
    time.sleep(1)
    
    for i in range(0,len(num)) :
        f.write('번호 : ' + str(num[i]).strip() + '\n')
        f.write('제목 : ' + str(titles[i]).strip() + '\n')
        f.write('지역 : ' + str(regions[i]).strip() + '\n')
        f.write('작성일 : ' + str(dates[i]).strip() + '\n')
        f.write('조회수 : ' + str(views[i]).strip() + '\n')
        f.write('내용 : ' + str(contents[i]).strip() + '\n')
        f.write('\n')
        
    f.close()
    print('txt 파일 저장 경로 : %s' %txt_path)

    print("요청하신 데이터 수집 작업이 정상적으로 완료되었습니다.")

# 엑셀 형태로 파일에 저장하기 위한 함수
def write_xls(xls_path, num, title, dates, regions, views, contents) :

    korea_trip = pd.DataFrame()
    korea_trip['번호'] = num
    korea_trip['제목'] = titles
    korea_trip['작성한 날짜'] = dates
    korea_trip['지역'] = regions
    korea_trip['내용'] = contents
    korea_trip['조회수'] = views
    
    # 엑셀 형태로 저장하기
    korea_trip.to_excel(xls_path , index=False)
    print('xls 파일 저장 경로 : %s' %xls_path)

    print("요청하신 데이터 수집 작업이 정상적으로 완료되었습니다.")

    
    
# csv 형태로 파일에 저장하기 위한 함수
def write_csv(csv_path, num, title, dates, regions, views, contents) :
    
    korea_trip = pd.DataFrame()
    korea_trip['번호'] = num
    korea_trip['제목'] = titles
    korea_trip['작성한 날짜'] = dates
    korea_trip['지역'] = regions
    korea_trip['내용'] = contents
    korea_trip['조회수'] = views
    
    # csv 형태로 저장하기
    korea_trip.to_csv(csv_path,encoding="utf-8-sig" , index=False)
    print('csv 파일 저장 경로 : %s' %csv_path)

    print("요청하신 데이터 수집 작업이 정상적으로 완료되었습니다.")
    


# 키워드 파일 이름들 입력받는 함수 호출해서 변수에 저장하기
query_txt, cnt = input_keyword()

page_cnt = math.ceil(cnt/10) # 크롤링할 전체 페이지 수


s_time = time.time() # 시작 시간
path = "C:/web_driver/chromedriver_0509.exe"
driver = webdriver.Chrome(path)
driver.maximize_window() # 창 최대화
driver.get("https://korean.visitkorea.or.kr/")

time.sleep(2)

element = driver.find_element_by_id('inp_search')
element.send_keys(query_txt)
driver.find_element_by_class_name('btn_search').click()

time.sleep(30)

cnt2 = 0 # 화면에 출력할 번호
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

search_cnt_1 = soup.find('div', 'total_check')
search_cnt_2 = search_cnt_1.find('strong').find('span').get_text()
search_cnt_2 = search_cnt_2.replace(',', '')


print('-----------------------')
print(search_cnt_2)
print('-----------------------')
if cnt > int(search_cnt_2) : # 만약 내가 입력한 수가 더 클 경우
    cnt2 = int(search_cnt_2)
else :
    cnt2 = cnt
    
real_page_cnt = math.ceil(cnt2/10) # 실제 페이지 수


if(int(search_cnt_2) == 0 ) :
    print("해당하신 키워드의 글은 존재하지 않습니다.")
    print("프로그램을 종료합니다.")
else :
    print('\n')
    print('='*80)
    print('요청하신 검색 건수는 %s 건 이었고, ' %cnt)
    print("해강 키워드로 실제 검색된 글의 건수가 총 %s 건이라서," %search_cnt_2)
    print('실제 검색 건수는 %s 건으로 재설정하고,' %cnt2)
    print('총 %s 페이지의 게시글 수집을 진행하겠습니다.' %real_page_cnt)


count = 0 # 번호 변수 생성
num = []
titles = [] # 제목을 저장할 리스트 생성
dates = [] # 수정일를 저장할 리스트 생성
regions = [] # 지역을 저장할 리스트 생성
views = [] # 조회수를 저장할 리스트 생성
contents = [] # 내용을 저장할 리스트 생성

# num, title, dates, regions, views, contents
def scroll_down(driver):
    #scrollHeight = 창사이즈, 0에서부터 창사이즈까지 내림
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")#스크립트를 실행 
    time.sleep(1)
    
def save_img(title, driver, img_src) :
    
    f_dir = 'C:\\python_temp\\happy\\img\\'
    title = title.replace(',' , ' ')
    title = title.replace('?' , '_')
    result_path = f_dir+title+'\\'
    
    print(result_path)
    print(os.path.isdir(result_path))
    if(os.path.isdir(result_path)) :
        print('입력하신 경로가 존재하여 %s 폴더에 저장하겠습니다.' %result_path)
    else : # 파일이 존재하지 않는다면 폴더를 생성 후 저장
        try :
            os.makedirs(result_path)
        except OSError :
            result_path = f_dir+title+'-'+query_txt
            os.makedirs(result_path)
        else :
            print('입력하신 경로가 존재하지 않아 %s 폴더를 만들어 저장하겠습니다' %result_path)
        finally :
            os.chdir(result_path) #폴더이동
            
    print('현재 웹 주소 : ', driver.current_url)
    current = driver.current_url
    driver.get(str(current))
    time.sleep(3)
    
    scroll_down(driver)
    
    #이미지를 추출하여 저장합니다.
    file_no = 0
    count = 1
    img_src2 = []

    for a in img_src:
        img_src1 = a['src']#src 속성만 가져와서 담고
        img_src2.append(img_src1)
        count += 1

    for b in range(0, len(img_src2)):#저장을 반복문으로 실행
        try:
            urllib.request.urlretrieve(img_src2[b],str(file_no)+'.jpg')
        except:
            continue
        file_no += 1
        time.sleep(0.5)
        print('%s 번째 이미지 저장중입니다.========='%file_no)  
        

web_url = 'https://korean.visitkorea.or.kr/search/search_list.do?keyword={}'.format(query_txt)

for page_num in range(1, real_page_cnt+1) :
    
    time.sleep(3)
    if(page_num>=1 and page_num <=5) :
        driver.get(web_url)
        time.sleep(5)
        driver.find_element_by_link_text(str(page_num)).click()
        # print(html)
        time.sleep(5)
    else :
        next_num = (page_num-3)%5
        if (next_num == 0 ) :
            next_num = 5
        driver.page_source
        xpath = '/html/body/div[2]/div/div[1]/div[8]/div/a[{}]'.format(next_num)
        driver.find_element_by_xpath(xpath).click()
        print('넘어옴')

    # time.sleep(3)
    # driver.find_element_by_link_text('최신순')
    # time.sleep(5)
    # driver.find_element_by_link_text(str(page_num)).click()
    # # print(html)
    # time.sleep(5)

    print(driver.current_url)
    # 현재의 페이지를 가져온다.
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find('ul', 'list_thumType type1').find_all('li')
        
    print('-----------------------' ,page_num ,'---------------------')

    link_n = 1 # 각 본문을 클릭하기위한 클릭 path

    print("{}페이지 내용 수집 시작합니다. ========================".format(page_num))
    print()

    page_count = 0
    for i in elements :
        print('--------  ',page_count,'  --------')
        if(page_count == 10) :
            break

        try :
            element = i.find('div', 'area_txt')
        except Exception as e :
            print("예외발생")
            print(e)
            link_n = link_n+1
            continue

        elements = i.find('div', 'area_txt')
        time.sleep(1)

        try :
            xpath = '//*[@id="listBody"]/ul/li[{}]/div[2]/div[1]/a'.format(link_n)
            driver.find_element_by_xpath(xpath).send_keys(Keys.ENTER)
        except Exception :
            link_n = link_n+1
            continue 
        else :
            link_n = link_n+1
            time.sleep(1.4)


        time.sleep(2)
        # 해당 글을 클릭한 후 페이지 tit_cont
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.find('div', 'titleType1')
        contents_list = soup.find_all('div', 'txt_p')
        try :
            img_src = soup.find('div','box_txtPhoto').find_all('img')
        except AttributeError:
            img_src = []

        # 번호 출력
        count+=1
        num.append(count)
        print('번호 :', count)
        #f.write(str(count) + '\n')

        time.sleep(2)

        # 제목 추출 id='topTitle'
        title = element.find('h2').get_text()
        titles.append(title)
        print('제목 :', title)
        #f.write(str(title) + '\n')

        time.sleep(2)

        try :
            region_date = element.find('div', 'area_address').find_all('span')
            #print(region_date)
        except AttributeError :
            date = '정보없음'
            region = '정보없음'
        else :
            if(len(region_date) == 1) :
                if(any(chr.isdigit() for chr in region_date[0].get_text())) :
                    date = region_date[0].get_text()
                    region = '정보없음'
                else :
                    date = '정보없음'
                    region = region_date[0].get_text()
            else :
                if ('코스' in region_date[1].get_text()) :
                    date = '정보없음'
                    region = region_date[0].get_text()
                else :
                    date = region_date[1].get_text()
                    region = region_date[0].get_text()


        regions.append(region)
        print('지역 :', region)


        date = date.replace('수정일 : ', "")
        dates.append(date)
        print('수정일 :', date)
        #f.write(str(date) + '\n')

        # 조회수 출력
        view = element.find('div', 'post_area').find('span', 'num_view').find('span', 'num').get_text()
        if( 'K' in view) :
            s = view.replace('K',' 1000')
            s = s.split(' ')
            result = float(s[0])*int(s[1])
            view = int(result)
        views.append(view)
        print('조회수 :',view)

        print('-------------------- 내용 --------------------')
        con = ""
        for txt in contents_list :
            content = txt.get_text().strip()
            if ('      ' in content) :
                content = content.replace('     ', ' ')
            print(content)
            con = con+content+'\n'
            print('\n')
        contents.append(con)


        print('------------------ 사진 저장 시작 -------------')
        if (len(img_src) == 0) :
            print('이미지 존재하지 않음')
        else :
            print('no')
            # save_img(title, driver, img_src)
        print('------------------ 사진 저장 끝 ---------------')

        page_count+=1
        print('\n')

        # 10으로 나눴을 때 나머지가 있었을 때 다 출력하지 않고 빠져나간다.
        if(count == cnt2) :
            break

        time.sleep(1)
        driver.back()


    if (page_num%5 == 0) :
        time.sleep(3)
        xpath = '/html/body/div[2]/div/div[1]/div[8]/div/a[8]'
        try :
            driver.find_element_by_xpath(xpath).click()
        except Exception as e :
            xpath = '/html/body/div[2]/div/div[1]/div[8]/div/a[6]'
            driver.find_element_by_xpath(xpath).click()
        finally :
            continue
        
print("======================================================")


if(int(search_cnt_2) == 0 ) :
    pass
else :
    path = want_to_save_crawlling_content()

    e_time = time.time( )
    t_time = e_time - s_time
    print("\n") 
    print("=" *80)
    print("총 소요시간은 %s 초 입니다 " %round(t_time,1))
    print("=" *80)

driver.close( )
