import tkinter
root = tkinter.Tk()

label = tkinter.Label(root, text="--")

label.pack()

value = 0

def onTimer():
    print("定时器函数已经调用 !")
    global timer_id
    timer_id = label.after(1000, onTimer)
    global value
    label['text'] = str(value)
    value += 1

def onStartTimer():
    global timer_id
    timer_id = label.after(1000, onTimer)

def onStopTimer():
    label.after_cancel(timer_id)

btn = tkinter.Button(root, text="开始",
                     command=onStartTimer)
btn.pack()

btn2 = tkinter.Button(root, text="取消定时器",
    command=onStopTimer)
btn2.pack()
root.mainloop()

