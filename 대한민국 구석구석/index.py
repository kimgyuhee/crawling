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
3. 준비중 (기능추가 예정)
번호 입력 >  '''
        menu2_input = input(menu2_sub_print)
        if not menu2_input.isdecimal() :
            print('*** 1 또는 2 숫자 중에 입력해주세요.\n')
        else :
            menu2_input = int(menu2_input)
            if(menu2_input == 1) :
                return_dir = self.output_xlsx_list1(self.default_path)
                if return_dir != "":
                    name, path = self.output_xlsx_list2(self.default_path, return_dir)
                    sorted_by_value = self.open_xlsx(path, name)
                    contents = self.noun_extraction(sorted_by_value)
                    self.print_top10(contents)
                    self.write_txt(name)
            elif(menu2_input == 2 ):
                import visualization
            else :
                print('\n*** 현재는 1번 2번 기능만 제공됩니다.')

    # xlsx 리스트 목록을 보여주기 위한 함수1
    def output_xlsx_list1(self, default_path) :
        # print('='*37)
        xlsx_list = []
        if not os.path.isdir(default_path) :
            print('*** 정보를 검색하기 위한 데이터가 존재하지 않습니다.')
            return ''
        
        files = os.listdir(default_path)

        for i in files :
            if not ('.' in i) :
                xlsx_list.append(i)

        text = '--'*37
        for i in range(len(xlsx_list)) :
            if i%3 == 0 :
                text = text +'\n'
            text = text + str(i) + '. '+xlsx_list[i]+' \t\t'

        text = text+'\n'+'--'*37+'\n'
        # print('='*37)

        print(text)

        while True :
            choice_dir = input('원하는 폴더를 선택해주세요 > ')
            if not choice_dir.isdecimal() :
                print('*** 범위 내의 숫자를 입력해주세요\n')
                continue
            else :
                choice_dir = int(choice_dir)
                if(choice_dir > len(xlsx_list)-1) :
                    print('*** 범위 내의 숫자를 입력해주세요\n')
                    continue
                else :
                    self.file_name = xlsx_list[choice_dir]
                    break
        
        return self.file_name
        # return text, xlsx_list


    # xlsx 리스트 목록을 보여주기 위한 함수2
    def output_xlsx_list2(self, default_path, return_dir) :
        # print('='*37)
        dir_path = default_path +'\\'+return_dir
        xlsx_list = []
        files = os.listdir(dir_path)

        for i in files :
            if ('.xlsx' in i) or ('.xls' in i) :
                value = i.split('.')[0]
                xlsx_list.append(value)

        text = '--'*37
        for i in range(len(xlsx_list)) :
            if i%3 == 0 :
                text = text +'\n'
            text = text + str(i) + '. '+xlsx_list[i]+' \t\t'

        text = text+'\n'+'--'*37+'\n'
        # print('='*37)
        print(text)

        while True :
            choice_xlsx_file = input('원하는 폴더를 선택해주세요 > ')
            if not choice_xlsx_file.isdecimal() :
                print('*** 범위 내의 숫자를 입력해주세요\n')
                continue
            else :
                choice_xlsx_file = int(choice_xlsx_file)
                if(choice_xlsx_file > len(xlsx_list)-1) :
                    print('*** 범위 내의 숫자를 입력해주세요\n')
                    continue
                else :
                    xlsx_name = xlsx_list[choice_xlsx_file]
                    break
        
        path = dir_path + '\\' + xlsx_name
        return xlsx_name, path
        # return xlsx_list
    

    def open_xlsx(self, path, name) :
        print(path)
        df = pd.read_excel(path+'.xlsx')
        sent_count = len(df.index)
        dict = {}
        mystr = ''

        try :
            w = df['지역']
            like = df['조회수']
            content = df['내용']
            contents = ""
            # print(content, type(content))
        except KeyError :
            print('xlsx 파일의 내용이 현 프로그램과 관련이 없습니다.')
            return mystr, 'no'
        else :
            for i in tqdm(range(len(w))):
                if (type(content[i]) == str ) :
                    contents +=content[i]+'\n'
                if (dict.get(w[i]) == None) :
                    dict[w[i]] = 1
                else :
                    dict[w[i]] +=1
                
        # sorted_by_value = sorted(dict.items(), key=lambda x: x[1], reverse=True)
        # return contents, sorted_by_value
        # return sorted_by_value
        # print(contents)
        return contents

                                    # 새로운 txt 파일에 형태소 분석 후 명사만 담아줄 함수
    def noun_extraction(self, contents):  # text: 말뭉치가 담긴 text 파일(읽기모드), txt_file: 파일경로와 파일명을 담고있는 함수
        okt = Okt()                   # 형태소 분석기인 Okt를 okt 변수에 담음 
        self.noun = okt.nouns(contents)   # text 변수로 불러온 데이터에서 명사만 추출 text: 말뭉치가 담긴 text 파일(읽기모드)
        dict={}
        for i in self.noun:               # noun: 명사 정보만 담고있는 변수 
            if len(i) > 1 : # 글의 길이가 1자 이하 단어는 생략
                if (dict.get(i) == None) :
                    dict[i] = 1
                else :
                    dict[i] +=1
        
        # print(self.noun)
        print('명사 추출이 완료되었습니다.')
        # print('\n명사 추출이 완료되었으며 파일이 정상적으로 저장되었습니다.\n')
        self.sorted_by_value2 = sorted(dict.items(), key=lambda x: x[1], reverse=True)

        # for i in self.sorted_by_value2 :
        #     print(i)
        # print(self.sorted_by_value2)
        return self.sorted_by_value2

    def write_txt(self, name) :
        today = datetime.today().strftime('%Y_%m_%d')
        check_path = 'C:\\Korea_trip_crawling_project\\txt\\{}'.format(today)
        path = 'C:\\Korea_trip_crawling_project\\txt\\{}\\{}.txt'.format(today,name)
        
        # print("-"*37)
        # print('\n저장될 경로는 {}입니다.'.format(path))

        if(not os.path.isdir(check_path)) :
            os.makedirs(check_path)
            # print('저장될 경로가 존재하지 않아 {} 폴더를 생성합니다.'.format(path))

        with open(path,'w',encoding='UTF-8') as f:
            for name in self.sorted_by_value2:
                if(name[1] != 1) :
                    f.write(name[0]+'\n')

        # print('txt 파일이 정상적으로 저장되었습니다.')

    def print_top10(self, top_10) :
        top_10 = self.sorted_by_value2
        print('=====================')
        print('많이 언급된 인기 단어 TOP10')
        count = 1
        for i in top_10 :
            if(count > 10) :
                break
            # print(i)
            print(str(count),'.' ,i[0])
            count+=1
        print('=====================')


program_start = Main()
program_start.main_menu()
print('*** 프로그램을 종료합니다.\n')