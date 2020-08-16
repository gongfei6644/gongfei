""" scale
"""


def resize(event=None):
    print(scale1.get())


import tkinter
root = tkinter.Tk()

scale1 = tkinter.Scale(root, from_=12, to=40,
                       orient=tkinter.HORIZONTAL,
                       command=resize)
scale1.set(20)
scale1.pack()

scale2 = tkinter.Scale(root, from_=12, to=40,
                       orient=tkinter.VERTICAL,
                       command=resize)

scale2.pack()
root.mainloop()
