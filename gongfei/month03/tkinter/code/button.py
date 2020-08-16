
import tkinter
root = tkinter.Tk()

times = 0  # 用来记录按钮接下的次数

def onBtnClick():
    print("正在点按钮")
    global times
    times += 1  # 次数加1
    s = "点我(%d)" % times
    btn.config(text=s)  # 改变全局变量btn的text属性



btn = tkinter.Button(root,
                     text='点我',
                     command=onBtnClick)
btn.pack()

root.mainloop()

