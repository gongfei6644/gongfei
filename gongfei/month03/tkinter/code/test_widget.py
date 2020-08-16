# widget 小部件，小控件

import tkinter
root = tkinter.Tk()

label = tkinter.Label(root, text="我是Label")
label.pack()

btn = tkinter.Button(root, text="我是Button")
btn.pack()

checkbox = tkinter.Checkbutton(root,
                               text="看书")
checkbox.pack()

entry = tkinter.Entry(root, text='请输入用户名')
entry.pack()

root.mainloop()

