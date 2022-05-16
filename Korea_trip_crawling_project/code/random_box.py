import tkinter
from tkinter import *
import random

# class Random_area :
#     def rand_choice(self, canvas, canvas_img) :
#         r_img = random.choice(self.img_list)
#         canvas.itemconfig(canvas_img, image=r_img)
    
#     def exe(self) :
#         window = Tk()
#         window.title("랜덤 추첨")
#         window.config(padx=10, pady=10, bg="lightblue")

#         canvas = Canvas(window, height=680, width=680, bg="ivory")
#         canvas.pack()

#         img_main = PhotoImage(file="area/gift.png")
#         canvas_img = canvas.create_image(340, 340, image=img_main)
#         canvas.create_text(340, 30, text="랜덤박스", fill="brown", \
#             font=("나눔바른펜", 30, "bold"))


#         self.img_list = []
#         for i in range(8) :
#             img = PhotoImage(file=f"images/img{i}.png")
#             self.img_list.append(img)

#         button = Button(window, text="랜덤 뽑기", bg="white", fg="hotpink", \
#             font=("나눔바른펜", 20, "bold"), \
#             command=self.rand_choice(canvas, canvas_img))

#         button.place(x=550, y=0)


#         window.mainloop()

# rand = Random_area()
# rand.exe()

def rand_choice() :
    r_img = random.choice(img_list)
    canvas.itemconfig(canvas_img, image=r_img)

window = Tk()
window.title("랜덤 추첨")
window.config(padx=10, pady=10, bg="ivory")

canvas = Canvas(window, height=600, width=600, bg="ivory")
canvas.pack()

img_main = tkinter.PhotoImage(file="images/gift.png", master=window)
canvas_img = canvas.create_image(300, 300, image=img_main)
# canvas.create_text(340, 30, text="랜덤박스", fill="brown", \
#    font=("나눔바른펜", 30, "bold"))


img_list = []
for i in range(6) :
    img = tkinter.PhotoImage(file=f"images/img{i}.png", master=window)
    img_list.append(img)

button = Button(window, text="여행지 뽑기", bg="white", fg="orange", \
    font=("나눔바른펜", 17, "bold"), \
    command=rand_choice)

button.place(x=470, y=0)


window.mainloop()