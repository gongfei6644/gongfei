
import tkinter

root = tkinter.Tk()

# 创建一个布尔型变量
btn1_v = tkinter.BooleanVar(root, value=False)

def onCheckBtn1():
    print("读书状态:", btn1_v.get())
    if btn1_v.get():
        cbtn2.deselect()
    else:
        cbtn2.select()



cbtn1 = tkinter.Checkbutton(root, text='读书',
                            command=onCheckBtn1,
                            variable=btn1_v)

cbtn2 = tkinter.Checkbutton(root, text='看电影')

# cbtn2 = tkinter.Checkbutton(root, text='看电影',
#                             variable=btn1_v)
cbtn1.pack()
cbtn2.pack()

root.mainloop()
