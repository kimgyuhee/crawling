import pandas as pd
import os
from tensorboard import program
from tqdm import tqdm
from konlpy.tag import Okt #형태소 분석 후 명사만 추출하기 위해 
from datetime import datetime # 날짜 및 시간 조작하기 위한 모듈

class Main() :

    default_path = 'C:\\Korea_trip_crawling_project\\xlsx'
    def __init__(self) :
        print('='*37)
        print('     대한민국 구석구석 프로젝트')
        print('='*37)
        
    def main_menu(self) :
        main_menu_print=''' 
1. 원하는 정보 크롤링하기
2. 원하는 정보 찾아보기
번호 입력 > ''' 
        while True :
            main_menu_input = input(main_menu_print)

            if not main_menu_input.isdecimal() :
                print('*** 1 또는 2 숫자 중에 입력해주세요.\n')
            else :
                main_menu_input = int(main_menu_input)
                if(main_menu_input == 1) :
                    import crwalling_stored
                    break
                elif (main_menu_input == 2) :
                    self.menu2_sub()
                    break
                else :
                    print('*** 1 또는 2 숫자 중에 입력해주세요.\n')
                    
    def menu2_sub(self) :
        print('='*37)
        menu2_sub_print = '''
1. 가장 많이 언급된 단어 TOP10
2. 단어 워드클라우드
3. 여행지 랜덤 추천
번호 입력 >  '''
        while True :
            menu2_input = input(menu2_sub_print)
            if not menu2_input.isdecimal() :
                print('*** 1 또는 2 숫자 중에 입력해주세요.\n')
                continue
            else :
                menu2_input = int(menu2_input)
                if(menu2_input == 1) :
                    import word_frequency
                elif(menu2_input == 2 ):
                    import visualization
                elif(menu2_input == 3) :
                    import random_box
                else :
                    print('\n*** 1~3번 사이의 숫자를 입력해주세요.\n')
                    continue
            break

program_start = Main()
program_start.main_menu()
print('*** 프로그램을 종료합니다.\n')