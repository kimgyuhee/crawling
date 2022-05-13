import pandas as pd # xlsx 파일을 저장하기 위한 모듈
import os # 폴더 집어 넣기 위한 모듈
from datetime import datetime # 날짜 및 시간 조작하기 위한 모듈

# from crwalling_input_data import query_txt, cnt 
from crwalling import query_txt, cnt, count, num, titles, dates, regions, views, contents

class Store_xlsx() :
    # 크롤링한 내용을 저장할지 묻고 실행하는 함수 생성
    def want_to_save_crawlling_content(self) :
        while True :
            print("-"*37)
            store = input("크롤링한 내용을 xlsx 형태로 저장하시겠습니까? 1.네 2.아니요(종료) > ")
            if not store.isdigit() :
                print('*** 1 또는 2 숫자 중에 입력해주세요.\n')
            else :
                store = int(store)
                if( store == 1) :
                    path = self.specified_path() # 파일이 저장될 경로 입력 받기
                    self.specified_xlsx_name(path)
                    self.write_xlsx(num, titles, dates, regions, views, contents)
                    break
                elif( store == 2) :
                    break
                else :
                    print('*** 1 또는 2 숫자 중에 입력해주세요.\n')
                    continue


    # 저장될 경로 확인하는 함수
    def specified_path(self) :
        today = datetime.today().strftime('%Y_%m_%d')
        path = 'C:\\Korea_trip_crawling_project\\xlsx\\{}\\'.format(today)
        print("-"*37)
        print('\n저장될 경로는 {}입니다.'.format(path))

        if(not os.path.isdir(path)) :
            print('저장될 경로가 존재하지 않아 {} 폴더를 생성합니다.'.format(path))
            os.makedirs(path)

        return path


    # xlsx 파일 이름을 만드는 함수
    def specified_xlsx_name(self, path) :
        
        self.xlsx_name = '{}_{}'.format(query_txt, cnt)
        self.xlsx_path = path+'\\'+self.xlsx_name+'.xlsx'
        return self.xlsx_path


    # 엑셀 형태로 파일에 저장하기 위한 함수
    def write_xlsx(self, num, titles, dates, regions, views, contents) :

        korea_trip = pd.DataFrame()
        korea_trip['번호'] = num
        korea_trip['제목'] = titles
        korea_trip['작성한 날짜'] = dates
        korea_trip['지역'] = regions
        korea_trip['내용'] = contents
        korea_trip['조회수'] = views
        
        # 엑셀 형태로 저장하기
        korea_trip.to_excel(self.xlsx_path , index=False)
        print('xls 파일 저장 경로 : %s' %self.xlsx_path)

        print("요청하신 데이터 수집 작업이 정상적으로 완료되었습니다.")


stored = Store_xlsx()
if count != 0 :
    stored.want_to_save_crawlling_content()