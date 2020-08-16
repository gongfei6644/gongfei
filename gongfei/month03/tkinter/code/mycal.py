
import tkinter
root = tkinter.Tk()

entry1 = tkinter.Entry(root)  # 被加数
entry2 = tkinter.Entry(root)
label_plus = tkinter.Label(root,text='+')

def onCal():
    s1 = entry1.get()
    s2 = entry2.get()
    try:
        result = int(s1) + int(s2)
        s = str(result) # 转为字符串
        label_result.config(text=s)
    except:
        label_result.config(text="输入有错!")

btn = tkinter.Button(root, text='=',
                     command=onCal)
label_result = tkinter.Label(root)
entry1.pack()
label_plus.pack()
entry2.pack()
btn.pack()
label_result.pack()



root.mainloop()