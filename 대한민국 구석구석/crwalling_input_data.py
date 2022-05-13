import math

class Input_data :
    # 키워드 입력받는 함수 생성
    def __init__(self) :
        print('\n 크롤링을 시작합니다. \n')

    def input_keyword(self) :
        while True :
            self.query_txt = input('크롤링할 키워드 : ')
            
            if(self.query_txt == "") :
                print('*** 아무것도 입력되지 않았습니다.')
                print('*** 다시 입력해주세요.\n')
                continue
            else :
                break

        return self.query_txt.strip()

    # 건수 입력받는 함수
    def input_cnt(self) :
        while True :
            self.cnt = input('크롤링할 건수 [1~50] : ')
            if not self.cnt.isdecimal() :
                print("*** 1부터 50 사이의 숫자를 입력해주세요.\n")
                continue
            else :
                self.cnt = int(self.cnt)
                if (self.cnt>50 or self.cnt < 0 ) :
                    print("*** 1부터 50 사이의 숫자를 입력해주세요.\n")
                    continue
                break
        return self.cnt

    def page_cnt(self) :
        self.page_cnt = math.ceil(self.cnt/10) # 크롤링할 전체 페이지 수
        return self.page_cnt

data = Input_data()
query_txt = data.input_keyword()
cnt = data.input_cnt()
# page_cnt = Input_data.page_cnt
page_cnt = data.page_cnt()