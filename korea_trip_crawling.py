from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#vhfrom webdriver_manager.chrome import ChromeDriverManager
import time
import sys
import os # 폴더 집어 넣기 위해
import math
import pandas as pd
import re # 정규 표현식을 사용하기 위한 모듈 선언

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
        


# 텍스트 파일이름 입력받는 함수 생성
def input_txt_name(path, txt) :
    while True :
        try :
            f_name = input("txt 파일의 이름을 지정해주세요.(경로 X, 확장자 X) > ")
        except Exception as e :
            print('에러발생')
            print('원인 : ', e)
            continue
        else :
            if( '.txt' in f_name) :
                print('파일의 이름만 입력해주세요')
                continue
            else :
                if( f_name == "") :
                    print('아무것도 입력되지 않았습니다.')
                    print('다시 입력해주세요.')
                    continue
                else :
                    break
                
    f_name = path+f_name+txt
    return f_name

# cvs 파일이름 입력받는 함수 생성
def input_csv_name(path, csv) :
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
                
    fc_name = path+fc_name+csv
    return fc_name


# xls 파일이름 입력받는 함수 생성
def input_xls_name(path, xls) :
    while True :
        try :
            fx_name = input("xls 파일의 이름을 지정해주세요.(경로 X, 확장자 X) > ")
        except Exception as e :
            print('에러발생')
            print('원인 : ', e)
            continue
        else :
            if( '.xls' in fx_name) :
                print('파일의 이름만 입력해주세요')
                continue
            else :
                if( fx_name == "") :
                    print('아무것도 입력되지 않았습니다.')
                    print('다시 입력해주세요.')
                    continue
                else :
                    break
                
    fx_name = path+fx_name+xls
    return fx_name

# 파일이름 입력받는 함수 생성
def input_files_name() :
    path = 'C:\\python_temp\\happy\\'
    txt = '.txt'
    csv = '.csv'
    xls = '.xls'

    # 저장할 파일의 이름을 입력받습니다.
    print("========== 파일들이 저장되는 경로는 C:\\python_temp\\data 입니다. ==========")
    f_name = input_txt_name(path, txt)

    fc_name = input_csv_name(path, csv)
    
    fx_name = input_xls_name(path, xls)
    
    return f_name, fc_name, fx_name


# 키워드 파일 이름들 입력받는 함수 호출해서 변수에 저장하기
query_txt, cnt = input_keyword()
f_name, fc_name, fx_name = input_files_name()


page_cnt = math.ceil(cnt/10) # 크롤링할 전체 페이지 수


s_time = time.time() # 시작 시간
driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
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

if cnt > int(search_cnt_2) : # 만약 내가 입력한 수가 더 클 경우
    cnt2 = int(search_cnt_2)
else :
    cnt2 = cnt
    
real_page_cnt = math.ceil(cnt2/10) # 실제 페이지 수

if(int(search_cnt_2) == 0 ) :
    print("해당하신 키워드의 글은 존재하지 않습니다.")
else :
    print('\n')
    print('='*80)
    print('요청하신 검색 건수는 %s 건 이었고, ' %cnt)
    print("해강 키워드로 실제 검색된 글의 건수가 총 %s 건이라서," %search_cnt_2)
    print('실제 검색 건수는 %s 건으로 재설정하고,' %cnt2)
    print('총 %s 페이지의 게시글 수집을 진행하겠습니다.' %real_page_cnt)
    
    
count = 0 # 번호 변수 생성
titles = [] # 제목을 저장할 리스트 생성
dates = [] # 수정일를 저장할 리스트 생성
regions = [] # 지역을 저장할 리스트 생성
views = [] # 조회수를 저장할 리스트 생성

for page_num in range(1, real_page_cnt+1) :

    # 현재의 페이지를 가져온다.
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find('ul', 'list_thumType type1').find_all('li')
    
    
    time.sleep(1)
    driver.find_element_by_link_text('%d' %page_num).send_keys(Keys.ENTER)
    time.sleep(1)
    
    link_n = 1 # 각 본문을 클릭하기위한 클릭 path
        
    print("{}페이지 내용 수집 시작합니다. ========================".format(page_num))
    print()
    
    f = open(f_name, 'a',encoding='UTF-8')
    
    
    for i in elements :
        try :
            element = i.find('div', 'area_txt')
        except Exception as e :
            link_n = link_n+1
            continue
        
        
        # 현재의 페이지를 가져온다.
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.find('ul', 'list_thumType type1').find_all('div', 'area_txt')
        
        time.sleep(1)
        
        
        
        try :
            xpath = '//*[@id="listBody"]/ul/li[{}]/div[2]/div[1]/a'.format(link_n)
            driver.find_element_by_xpath(xpath).send_keys(Keys.ENTER)
        except Exception :
            link_n = link_n+1
            continue 
        else :
            link_n = link_n+1
            time.sleep(1)
        
        
        
        # 해당 글을 클릭한 후 페이지 tit_cont
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.find('div', 'titleType1')
        
        
        # 번호 출력
        count+=1
        print('번호 :', count)
        f.write(str(count) + '\n')
        
        time.sleep(1)
        
        # 제목 추출 id='topTitle'
        title = element.find('h2').get_text()
        titles.append(title)
        print('제목 :', title)
        f.write(str(title) + '\n')
        
        try :
            region_date = element.find('div', 'area_address').find_all('span')
            print(region_date)
            
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
        f.write(str(region) + '\n')
            
        date = date.replace('수정일 : ', "")
        dates.append(date)
        print('수정일 :', date)
        f.write(str(date) + '\n')
        
        # 조회수 출력
        view = element.find('div', 'post_area').find('span', 'num_view').find('span', 'num').get_text()
        if( 'K' in view) :
            s = view.replace('K',' 1000')
            s = s.split(' ')
            result = float(s[0])*int(s[1])
            view = int(result)
        views.append(view)
        print('조회수 :',view)
        f.write(str(view) + '\n')
        f.write('\n')
        print('\n')
            
        # 10으로 나눴을 때 나머지가 있었을 때 다 출력하지 않고 빠져나간다.
        if(count == cnt2) :
            break
            
        time.sleep(1)
        driver.back()
            
        
        time.sleep(1)
    
        
    if (page_num%5 == 0) :
        driver.find_element_by_link_text('다음').click()
        time.sleep(1)
        # 현재의 페이지를 가져온다.
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.find('ul', 'list_thumType type1').find_all('div', 'area_txt')
        continue
        
    
print("======================================================")

f.close()


if(int(search_cnt_2) == 0 ) :
    pass
else :
    korea_trip = pd.DataFrame()
    korea_trip['제목']=pd.Series(titles)
    korea_trip['수정일']=pd.Series(dates)
    korea_trip['지역']=pd.Series(regions)
    korea_trip['조회수']=pd.Series(views)

    # csv 형태로 저장하기
    korea_trip.to_csv(fc_name,encoding="utf-8-sig" , index=False)

    # 엑셀 형태로 저장하기
    korea_trip.to_excel(fx_name , index=False)

    # Step 4. 요약 정보 보여주기
    e_time = time.time( )
    t_time = e_time - s_time

    print("\n") 
    print("=" *80)
    print("총 소요시간은 %s 초 입니다 " %round(t_time,1))
    print("파일 저장 완료: txt 파일명 : %s " %f_name)
    print("파일 저장 완료: csv 파일명 : %s " %fc_name)
    print("파일 저장 완료: xls 파일명 : %s " %fx_name)
    print("=" *80)

driver.close( )

