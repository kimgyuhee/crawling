from tkinter import font
from sympy import content
from wordcloud import WordCloud  # 워드 클라우드로 이미지 표현을 위함 
import matplotlib.pyplot as plt  # 시각화 기능 사용을 위함 
import numpy as np               # 이미지 데이터를 다루기 위함 
from PIL import Image            # 이미지를 위한 라이브러리
import os
from datetime import datetime # 날짜 및 시간 조작하기 위한 모듈
from wordcloud import WordCloud

class Visualization():

    default_path = 'C:\\Korea_trip_crawling_project\\txt'
    def __init__(self) :
        print('\n 시각화를 시작합니다. \n')

    # txt 리스트 목록을 보여주기 위한 함수1
    def output_txt_list1(self, default_path) :
        # print('='*37)
        txt_list = []
        if not os.path.isdir(default_path) :
            print('*** 정보를 검색하기 위한 데이터가 존재하지 않습니다.')
            return ''
        
        files = os.listdir(default_path)

        for i in files :
            if not ('.' in i) :
                txt_list.append(i)

        text = '--'*37
        for i in range(len(txt_list)) :
            if i%3 == 0 :
                text = text +'\n'
            text = text + str(i) + '. '+txt_list[i]+' \t\t'

        text = text+'\n'+'--'*37+'\n'
        # print('='*37)

        print(text)

        while True :
            choice_dir = input('원하는 폴더를 선택해주세요 > ')
            print()
            if not choice_dir.isdecimal() :
                print('*** 범위 내의 숫자를 입력해주세요\n')
                continue
            else :
                choice_dir = int(choice_dir)
                if(choice_dir > len(txt_list)-1) :
                    print('*** 범위 내의 숫자를 입력해주세요\n')
                    continue
                else :
                    self.file_name = txt_list[choice_dir]
                    break


    # xlsx 리스트 목록을 보여주기 위한 함수2
    def output_xlsx_list2(self, default_path, return_dir) :
        # print('='*37)
        dir_path = default_path +'\\'+return_dir
        txt_list = []
        files = os.listdir(dir_path)

        for i in files :
            if ('.txt' in i) :
                value = i.split('.')[0]
                txt_list.append(value)

        text = '--'*37
        for i in range(len(txt_list)) :
            if i%3 == 0 :
                text = text +'\n'
            text = text + str(i) + '. '+txt_list[i]+' \t\t'

        text = text+'\n'+'--'*37+'\n'
        # print('='*37)
        print(text)

        while True :
            choice_txt_file = input('원하는 폴더를 선택해주세요 > ')
            print()
            if not choice_txt_file.isdecimal() :
                print('*** 범위 내의 숫자를 입력해주세요\n')
                continue
            else :
                choice_txt_file = int(choice_txt_file)
                if(choice_txt_file > len(txt_list)-1) :
                    print('*** 범위 내의 숫자를 입력해주세요\n')
                    continue
                else :
                    self.txt_name = txt_list[choice_txt_file]
                    break
        
        path = dir_path + '\\' + self.txt_name
        return self.txt_name, path
    
    def open_txt(self, path) :
        path = path +'.txt'
        f = open(path , 'r', encoding='UTF-8')
        line = f.read()
        # print(type(line))
        # print(line)
        
        return line

    def worldcould(self, path, contents) :
        icon = Image.open('./images/mask_img.png')
        mask = Image.new("RGB", icon.size, (255,255,255))
        mask.paste(icon,icon)
        mask_img = np.array(mask)
        
        wc = WordCloud(font_path='malgun',background_color="white", max_words=20000, max_font_size=300, mask=mask_img)
        # wc.generate_from_frequencies(dict(contents))
        wc.generate(contents)
        now_date = datetime.today().strftime('%Y_%m_%d')
        base_path = 'C:\\Korea_trip_crawling_project\\png\\{}'.format(now_date)
        path = 'C:\\Korea_trip_crawling_project\\png\\{}\\{}.png'.format(now_date, self.txt_name)
        if not os.path.isdir(base_path) :
            os.makedirs(base_path)

        wc.to_file(path)
        
        # 워드 클라우드 화면으로 보여주는 코드
        plt.figure(figsize=(10,8))
        plt.imshow(wc)
        plt.axis('off')
        plt.show()

    def exe(self) :
        self.output_txt_list1(self.default_path)
        txt_name, path = self.output_xlsx_list2(self.default_path, self.file_name)
        contents = self.open_txt(path)
        self.worldcould(path, contents)

v = Visualization()
v.exe()