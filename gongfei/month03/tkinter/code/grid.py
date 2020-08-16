import tkinter

root = tkinter.Tk()

label1 = tkinter.Label(root, text='aaaaa',
                       bg='red',height=3)
label1.grid(row=0, column=0)

label2 = tkinter.Label(root, text='bbbb',
                       bg='blue')
label2.grid(row=1, column=1)

label3 = tkinter.Label(root, text='ccccc',
                       bg='green')
label3.grid(row=2, column=2)

label4 = tkinter.Label(root, text='dddd',
                       bg='orange')
label4.grid(row=0, column=1, columnspan=2,
            stick=tkinter.E)


root.mainloop()