
def onMouseDown(event):
    print("有鼠标键按下", event.x, event.y)

def onMouseRelease(event):
    print("有鼠标键抬起")

def onKeyDown(event):
    print("有按键按下:", event.keysym,
          event.char, event.keycode)


import tkinter
root = tkinter.Tk()
root.bind('<Button-1>', onMouseDown)  # 绑定左键
root.bind('<ButtonRelease>', onMouseRelease)

root.bind('<Key>', onKeyDown)

root.mainloop()


