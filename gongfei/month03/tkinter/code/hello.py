
# 导入tkinter包
import tkinter

# 创建顶层窗口
root = tkinter.Tk()

# 创建Label
label = tkinter.Label(root,
                      text="Hello world",
                      bg='#FF0000')

label.pack()  # 把label 放在窗口上

# 进入主事件循环
root.mainloop()


print("程序退出")
