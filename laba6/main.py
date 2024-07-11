import math
from tkinter import messagebox

import numpy as np
import matplotlib.pyplot as plt
from tkinter import *

a_matrix = np.array([[2, 3], [1, 1]])
e_matrix = np.array([[1, 0], [0, 1]])
l1 = 1.5 - math.sqrt(13.0)/2.0
l2 = 1.5 + math.sqrt(13.0)/2.0
caef1 = (a_matrix - l2*e_matrix)/(l1-l2)
caef2 = (a_matrix - l1*e_matrix)/(l2-l1)
tyu = 0

def step_eyler(y1, y2, h):
    new_y1 = y1 + (2.0*y1 + 3.0*y2)*h
    new_y2 = y2 + (y1+y2)*h
    return np.array([new_y1, new_y2])


def step_lagranz(y10, y20, x):
    exp_matrix = math.exp(l1*x)*caef1 + math.exp(l2*x)*caef2
    fin_matrix = exp_matrix.dot(np.array([[y10],[y20]]))
    y1 = fin_matrix[0][0]
    y2 = fin_matrix[1][0]
    return np.array([y1, y2])


def bnt_click():
    plt.style.use('seaborn-v0_8-whitegrid')
    try:
        y10 = float(loginOfy10.get())
        y20 = float(loginOfy20.get())
        b = float(loginOfb.get())
        if abs(y10) == abs(math.inf) or abs(y20) == abs(math.inf) or b <= 0.001:
            raise ValueError
    except ValueError:
        messagebox.showerror(title='Ошибка типа данных', message='введите данные корректно')
        return
    array_of_x = np.linspace(0.0, b, num=10000)
    array_of_y1 = np.zeros((10000,), dtype=float)
    array_of_y2 = np.zeros((10000,), dtype=float)
    array_of_y1[0] = y10
    array_of_y2[0] = y20
    h = abs(array_of_x[1]-array_of_x[0])
    if var.get() == 1:
        try:
            for i in range(1,10000):
                array_of_y1[i] = step_eyler(array_of_y1[i-1], array_of_y2[i - 1], h)[0]
                array_of_y2[i] = step_eyler(array_of_y1[i - 1], array_of_y2[i - 1], h)[1]
        except ArithmeticError:
            messagebox.showerror(title='Некорректные начальные значения', message='попробуйте ввести другие данные')
            return
        except ValueError:
            messagebox.showerror(title='Переполнение типа данных', message='попробуйте вести данные поменьше')
            return
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.plot(array_of_x, array_of_y1)
        ax1.plot(array_of_x, array_of_y2)
    else:
        try:
            for i in range(len(array_of_x)):
                array_of_y1[i] = step_lagranz(y10, y20, array_of_x[i])[0]
                array_of_y2[i] = step_lagranz(y10, y20, array_of_x[i])[1]
        except ArithmeticError:
            messagebox.showerror(title='Некорректные начальные значения', message='попробуйте ввести другие данные')
            return
        except ValueError:
            messagebox.showerror(title='Переполнение типа данных', message='попробуйте вести данные поменьше')
            return
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.plot(array_of_x, array_of_y1)
        ax1.plot(array_of_x, array_of_y2)
    plt.show()
    return


root = Tk()
root.title('Erofeev 6')
root.geometry('400x400')

frame = Frame(root, bg='grey')
frame.place(relheight=1, relwidth=1)
title = Label(frame, text='y1(0)=', bg='gray', width=200)
loginOfy10 = Entry(frame, bg='white')
title2 = Label(frame, text='y2(0)=', bg='gray')
loginOfy20 = Entry(frame, bg='white')
title3 = Label(frame, text='b=', bg='gray')
loginOfb = Entry(frame, bg='white')

var = IntVar()
var.set(0)
lagranz = Radiobutton(text="Метод Лагранжа-Сильвестра", variable=var, value=0, bg='gray')
eyler = Radiobutton(text="Метод Эйлера", variable=var, value=1, bg='gray')


title.pack()
loginOfy10.pack()
title2.pack()
loginOfy20.pack()
title3.pack()
loginOfb.pack()
lagranz.pack(side=BOTTOM)
eyler.pack(side=BOTTOM)
bnt = Button(frame, text='Построить график', bg='gray', command=bnt_click)
# bnt2 = Button(frame, text='Построить график по точкам', bg='gray', command=btn2_click)

bnt.pack()
# bnt2.pack()

root.mainloop()
