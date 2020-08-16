
import tkinter

root = tkinter.Tk()

label = tkinter.Label(root,
                      text="这是文字",
                      bg='red',
                      width=10,  # 英文字符宽度
                      height=3,   # 3行高
                      font=('黑体', 30)
                      )
label.pack()

# 用mypic.gif文件创建一个PhotoImage对象
img = tkinter.PhotoImage(file="mypic.gif")

label2 = tkinter.Label(root, image=img)
label2.pack()


root.mainloop()


