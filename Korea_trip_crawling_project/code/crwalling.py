from bs4 import BeautifulSoup
from django import views
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import math
import os
import urllib
from datetime import datetime # 날짜 및 시간 조작하기 위한 모듈
from crwalling_input_data import query_txt, cnt, page_cnt

class Crawlling() :

    count = 0 # 번호 변수 생성
    num = []
    titles = [] # 제목을 저장할 리스트 생성
    dates = [] # 수정일를 저장할 리스트 생성
    regions = [] # 지역을 저장할 리스트 생성
    views = [] # 조회수를 저장할 리스트 생성
    contents = [] # 내용을 저장할 리스트 생성
    web_url = 'https://korean.visitkorea.or.kr/search/search_list.do?keyword={}'.format(query_txt)
    
    def open_chrome(self) :
        path = "C:/web_driver/chromedriver_0509.exe"
        driver = webdriver.Chrome(path)
        driver.maximize_window() # 창 최대화
        driver.get("https://korean.visitkorea.or.kr/")

        time.sleep(2)

        element = driver.find_element_by_id('inp_search')
        element.send_keys(query_txt)
        driver.find_element_by_class_name('btn_search').click()

        time.sleep(25)

        return driver

    def page_seach(self, driver) :
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
            print("프로그램을 종료합니다.")
            return 0,0
        else :
            print('\n')
            print('='*80)
            print('요청하신 검색 건수는 %s 건 이었고, ' %cnt)
            print("해강 키워드로 실제 검색된 글의 건수가 총 %s 건이라서," %search_cnt_2)
            print('실제 검색 건수는 %s 건으로 재설정하고,' %cnt2)
            print('총 %s 페이지의 게시글 수집을 진행하겠습니다.' %real_page_cnt)
        
        return real_page_cnt, cnt2

    def scroll_down(self, driver):
        #scrollHeight = 창사이즈, 0에서부터 창사이즈까지 내림
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")#스크립트를 실행 
        time.sleep(1)


    def crawling(self, real_page_cnt, cnt2, driver) :

        for page_num in range(1, real_page_cnt+1) :
    
            driver.implicitly_wait(3)
            if(page_num>=1 and page_num <=5) :
                driver.get(self.web_url)
                driver.implicitly_wait(5)
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
                # print('--------  ',page_count,'  --------')
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


                time.sleep(3)
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
                self.count+=1
                self.num.append(self.count)
                print('번호 :', self.count)
                #f.write(str(count) + '\n')

                time.sleep(3)

                # 제목 추출 id='topTitle'
                title = element.find('h2').get_text()
                self.titles.append(title)
                print('제목 :', title)
                #f.write(str(title) + '\n')

                time.sleep(3)

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


                self.regions.append(region)
                print('지역 :', region)


                date = date.replace('수정일 : ', "")
                self.dates.append(date)
                print('수정일 :', date)
                #f.write(str(date) + '\n')

                # 조회수 출력
                view = element.find('div', 'post_area').find('span', 'num_view').find('span', 'num').get_text()
                if( 'K' in view) :
                    s = view.replace('K',' 1000')
                    s = s.split(' ')
                    result = float(s[0])*int(s[1])
                    view = int(result)
                self.views.append(view)
                print('조회수 :',view)

                # print('-------------------- 내용 수집중 --------------------')
                con = ""
                for txt in contents_list :
                    content = txt.get_text().strip()
                    if ('      ' in content) :
                        content = content.replace('     ', ' ')
                    # print(content)
                    con = con+content+'\n'
                    # print('\n')
                self.contents.append(con)
                # print('-------------------- 내용 수집 끝 --------------------')

                print('------------------ 사진 저장 시작 -------------')
                if (len(img_src) == 0) :
                    print('이미지 존재하지 않음')
                else :
                    self.save_img(title, driver, img_src)
                print('------------------ 사진 저장 끝 ---------------')

                page_count+=1
                print('\n')

                # 10으로 나눴을 때 나머지가 있었을 때 다 출력하지 않고 빠져나간다.
                if(self.count == cnt2) :
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
        return self.count, self.num, self.titles, self.dates, self.regions, self.views, self.contents; 

    def save_img(self, title, driver, img_src) :
    
        today = datetime.today().strftime('%Y_%m_%d')
        path = 'C:\\Korea_trip_crawling_project\\img\\{}\\'.format(today)
        file_name = query_txt+'_'+str(cnt)
        print('사진이 저장되는 경로는 {}입니다.'.format(path))

        title = title.replace(':' , ' ')
        title = title.replace('\\' , ' ')
        title = title.replace('|' , '')
        title = title.replace('*' , '')
        title = title.replace('"' , '')
        title = title.replace('/' , ' ')
        title = title.replace('<' , ' ')
        title = title.replace('>' , ' ')
        title = title.replace('?' , '')
        result_path = path+file_name+'\\'+title+'\\'
    

        if(not os.path.isdir(result_path)) :
            os.makedirs(result_path)
            print('{}경로가 존재하지 않아 폴더를 생성했습니다.\n'.format(path))

        os.chdir(result_path) #폴더이동
                
        print('현재 웹 주소 : ', driver.current_url)
        current = driver.current_url
        driver.get(str(current))
        time.sleep(3)
        
        self.scroll_down(driver)
        
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
    
cr = Crawlling()
driver = cr.open_chrome()
real_page_cnt, cnt2 = cr.page_seach(driver)
count, num, titles, dates, regions, views, contents = cr.crawling(real_page_cnt, cnt2, driver)