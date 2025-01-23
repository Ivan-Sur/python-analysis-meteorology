import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import matplotlib.pyplot as plt
import json
import numpy as np
from matplotlib.ticker import FixedLocator, FixedFormatter

device_box = []
data_box = []
type_box = []
color_box = []

def To_min(d, start_d):   #2022-11-28 00:00:01
    a = ((int(d[8:10])-int(start_d[8:10]))*24 + int(d[11:13])-int(start_d[11:13]))*60 + int(d[14:16])-int(start_d[14:16])
    return a
def reduce(An, Bn):
    i = 0
    A = []
    B = []
    n = 1
    while(i < len(An)):
        if(An[i] not in A):
            A.append(An[i])
            B.append(Bn[i])
            if(i!=0): B[-2]/=n
            n = 1
        else:
            n+=1
            B[-1]+=Bn[i]
        i+=1
    B[-1]/=n
    return A, B
def data_day(dict, st_d, end_d, d_d):
    A = []
    B = []
    for k in dict:
        if (k > end_d): break
        if (k < st_d): continue
        A.append(To_min(k, st_d)//(24*60))
        B.append(dict[k][d_d])
    return reduce(A, B)
def data_3h(dict, st_d, end_d, d_d):
    A = []
    B = []
    for k in dict:
        if (k > end_d): break
        if (k < st_d): continue
        A.append(To_min(k, st_d)//(3*60))
        B.append(dict[k][d_d])
    return reduce(A, B)
def data_1h(dict, st_d, end_d, d_d):
    A = []
    B = []
    for k in dict:
        if (k > end_d): break
        if (k < st_d): continue
        A.append(To_min(k, st_d)//60)
        B.append(dict[k][d_d])
    return reduce(A, B)
def data_min(dict, st_d, end_d, d_d):
    A = []
    B = []
    for k in dict:
        if (k > end_d): break
        if (k < st_d): continue
        A.append(To_min(k, st_d))
        B.append(dict[k][d_d])
    return reduce(A, B)
def max_min(dict, st_d, end_d, d_d):
    A = []
    B = []
    C = []
    for k in dict:
        if (k > end_d): break
        if (k < st_d): continue
        date = To_min(k, st_d) // (24 * 60)
        if(date in A):
            B[-1] = max(dict[k][d_d], B[-1])
            C[-1] = min(dict[k][d_d], C[-1])
        else:
            A.append(date)
            B.append(dict[k][d_d])
            C.append(dict[k][d_d])
    return A, B, C

def inputerror():
    messagebox.showerror("Внимание!", "Ошибка ввода, для получния помощи нажмите кнопку \"Инструкция\"")
    sys.exit()
def check_input():
    count = int(CT.get())
    for i in range(count):
        if(device_box[i].get() in ['Опорный барометр', "Паскаль"] and data_box[i].get() in ["Влажность", "Эффективная температура"]): inputerror()
    return
def check_const(a, b):
    if(len(a) == len(b) == 19):
        for i in [a, b]:
            if not (i[:4].isdigit() and i[5:7].isdigit() and i[8:10].isdigit() and i[11:13].isdigit() and i[14:16].isdigit() and i[17:].isdigit()): inputerror()
            if not (i[:4] == '2022' and i[5:7] == '12' and 1 <= int(i[8:10]) <=14 and 0 <= int(i[11:13]) <= 23 and 0 <= int(i[14:16]) <= 59 and 0 <= int(i[17:]) <= 59): inputerror()
            if not (i[4] == i[7] == '-' and i[10] == ' ' and i[13] == i[16] == ':'): inputerror()
        return
    inputerror()

def confirm_():
    check_input()
    global device_box
    global data_box
    global type_box
    global color_box
    request = []
    count = int(CT.get())
    Start_Date = SD.get()
    End_Date = ED.get()
    ever = EV.get()
    data_dict = {'Температура': "temp", "Давление": "pressure", "Влажность": "humidity", "Эффективная температура": "ef_temp"}
    color_dict = {"Красный": "red", "Синий": "blue", "Зеленый": "green", "Фиолетовый": "#7C00CE"}
    color_dict1 = {"Красный": "maroon", "Синий": "darkblue", "Зеленый": "darkgreen", "Фиолетовый": "indigo"}
    for i in range(count): request.append([device_box[i].get(), data_box[i].get(), type_box[i].get(), color_box[i].get()])
    fig, ax = plt.subplots()
    ax.set_xlabel(f'{ever if (ever != "макс/мин за день") else "Дни"}')
    for i in range(count):
        with open(request[i][0] + '.json') as f:
            dict = json.load(f)
        if (ever == 'День'): A, B = data_day(dict, Start_Date, End_Date, data_dict[request[i][1]])
        if (ever == '1 минута'): A, B = data_min(dict, Start_Date, End_Date, data_dict[request[i][1]])
        if (ever == '1 час'): A, B = data_1h(dict, Start_Date, End_Date, data_dict[request[i][1]])
        if (ever == '3 часа'): A, B = data_3h(dict, Start_Date, End_Date, data_dict[request[i][1]])
        if (ever == 'макс/мин за день'):
            A, B, C = max_min(dict, Start_Date, End_Date, data_dict[request[i][1]])
            if (request[i][2] == 'Линейный'):
                ax.plot(A, B, c=color_dict[request[i][3]], marker='.', label=f"{request[i][0]}->{request[i][1]}->max")
                ax.plot(A, C, c=color_dict1[request[i][3]], marker='.', label=f"{request[i][0]}->{request[i][1]}->min")
            if (request[i][2] == 'Столбчатый'):
                w = 0.8
                ax.bar(A, B, color=color_dict[request[i][3]], width=w, label=f"{request[i][0]}->{request[i][1]}->max")
                ax.bar(A, C, color=color_dict1[request[i][3]], width=w, label=f"{request[i][0]}->{request[i][1]}->min")
            if (request[i][2] == 'Гистограмма'):
                ax.hist(np.array(B) + 0.1, color=color_dict[request[i][3]], width=0.1, label=f"{request[i][0]}->{request[i][1]}->max")
                ax.hist(np.array(C) - 0.1, color=color_dict1[request[i][3]], width=0.1, label=f"{request[i][0]}->{request[i][1]}->min")
        else:
            if (request[i][2] == 'Линейный'): ax.plot(A, B, c=color_dict[request[i][3]], marker='.', label=f"{request[i][0]}->{request[i][1]}")
            if (request[i][2] == 'Столбчатый'): ax.bar(A, B, color=color_dict[request[i][3]], label=f"{request[i][0]}->{request[i][1]}")
            if (request[i][2] == 'Гистограмма'): ax.hist(B, color=color_dict[request[i][3]], width=0.1, label=f"{request[i][0]}->{request[i][1]}")
        if (request[i][1] == 'Давление' and request[i][2] == 'Столбчатый'): plt.ylim(730, 775)
        if (request[i][1] == 'Эффективная температура' and request[i][2] != "Гистограмма"):
            ax.axhline(y=12, color='grey', ls='--', lw=1.5)
            ax.axhline(y=18, color='grey', ls='--', lw=1.5)
            ax.axhline(y=24, color='grey', ls='--', lw=1.5)
            ax.yaxis.set_major_locator(FixedLocator(np.arange(12, 25, 2)))
            ax.yaxis.set_major_formatter(FixedFormatter([12, 14, 'Умеренно\nтепло', 18, 20, 'Теплло', 24]))

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.25, box.width, box.height * 0.75])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15))

    ax.grid(which="major", axis='x', color='#DAD8D7', alpha=0.5, zorder=1)
    ax.grid(which="major", axis='y', color='#DAD8D7', alpha=0.5, zorder=1)
    ax.set_title(f'Графики с {Start_Date} до {End_Date}', fontsize=12, fontweight='bold', pad=20)
    plt.show()

def confirm_const():
    check_const(SD.get(), ED.get())
    Start_Date = SD.get()
    End_Date = ED.get()
    ever = EV.get()
    count = int(CT.get())
    Confirm_const['bg'] = '#cccccc'
    Confirm_const['state'] = tk.DISABLED
    EV['state'] = tk.DISABLED
    SD['state'] = tk.DISABLED
    ED['state'] = tk.DISABLED
    CT['state'] = tk.DISABLED
    tk.Label(win, text='№ графика', font=8, bg='#cccccc').grid(row=2, column=0, stick='wens', padx=5, pady=5)
    tk.Label(win, text='Прибор', font=8, bg='#cccccc').grid(row=2, column=1, stick='wens', padx=5, pady=5)
    tk.Label(win, text='Данные', font=8, bg='#cccccc').grid(row=2, column=2, stick='wens', padx=5, pady=5)
    tk.Label(win, text='Тип графика', font=8, bg='#cccccc').grid(row=2, column=3, stick='wens', padx=5, pady=5)
    tk.Label(win, text='Цвет', font=8, bg='#cccccc').grid(row=2, column=4, stick='wens', padx=5, pady=5)
    device_list = ['Опорный барометр', 'Hydra-L', 'Паскаль', 'РОСА К-2', 'Тест воздуха', 'Тест Студии - broken']
    global device_box
    global data_box
    global type_box
    global color_box
    data_list = ['Температура', "Давление", "Влажность", "Эффективная температура"]
    type_list = ['Линейный', "Столбчатый", "Гистограмма"]
    color_list = ['Красный', "Синий", "Зеленый", "Фиолетовый"]
    for i in range(1, count+1):
        tk.Label(win, text=f'{i} график', font=8, bg='#cccccc').grid(row=i+2, column=0, stick='wens')
        device_box.append(ttk.Combobox(win, font=8, values=device_list, state="readonly", justify='center'))
        device_box[-1].current(i-1)
        device_box[-1].grid(row=i+2, column=1, stick='wens', padx=5, pady=5)
        data_box.append(ttk.Combobox(win, font=8, values=data_list, state="readonly", justify='center'))
        data_box[-1].current(0)
        data_box[-1].grid(row=i+2, column=2, stick='wens', padx=5, pady=5)
        type_box.append(ttk.Combobox(win, font=8, values=type_list, state="readonly", justify='center'))
        type_box[-1].current(0)
        type_box[-1].grid(row=i+2, column=3, stick='wens', padx=5, pady=5)
        color_box.append(ttk.Combobox(win, font=8, values=color_list, state="readonly", justify='center'))
        color_box[-1].current(i-1)
        color_box[-1].grid(row=i + 2, column=4, stick='wens', padx=5, pady=5)
    Confirm_ = tk.Button(win, text='Готово', font=8, command=confirm_, bd=5)
    Confirm_.grid(row=7, column=5, stick='wens', padx=5, pady=5)

def instruction():
    str = "1. Пожалуйста, вводите даты в формате YYYY-MM-DD HH:MM:SS\n" \
          "2. Обращаю Ваше внимание, что такие приборы, как 'Опорный барометр' и 'Паскаль' не имеют информации о влажности и эффективной температуре\n" \
          "3. Также не рекомендуется строить на одном полотне графики температуры или влажности и давления\n" \
          "4. Почти все данные прибора 'Тест студии' равны нулю выбирать этот датчик бесполезно\n" \
          "5. У графиков по оси Х 0 это выбранная начальная дата"
    messagebox.showinfo("Добро пожаловать в программу построения графиков!", str)

win = tk.Tk()
win.geometry(f"1205x500+100+200")
win.title("Исходные данные для графиков")
win.config(bg='#cccccc')
for i in range(9):
    win.grid_rowconfigure(i, minsize=60)
    win.grid_columnconfigure(i, minsize=175)


tk.Label(win, text='Начало от\n2022-12-01 00:00:00', font=8, bg='#cccccc').grid(row=0, column=1, stick='wens', padx=5, pady=5)
tk.Label(win, text='Конец до\n2022-12-14 23:59:59', font=8, bg='#cccccc').grid(row=0, column=2, stick='wens', padx=5, pady=5)
tk.Label(win, text='Шаг', font=8, bg='#cccccc').grid(row=0, column=3, stick='wens', padx=5, pady=5)
tk.Label(win, text='Количество\nграфиков', font=8, bg='#cccccc').grid(row=0, column=4, stick='wens', padx=5, pady=5)

SD = tk.Entry(win, font=8, bd=5, justify='center')
SD.insert(0, "2022-12-01 00:00:00")
SD.grid(row=1, column=1, stick='wens', padx=5, pady=5)

ED = tk.Entry(win, justify='center', font=8, bd=5)
ED.insert(0, "2022-12-14 23:59:59")
ED.grid(row=1, column=2, stick='wens', padx=5, pady=5)

everaging_list = ['День', "1 час", "3 часа", "1 минута", "макс/мин за день"]
EV = ttk.Combobox(win, font=8, values=everaging_list, state="readonly", justify='center')
EV.current(0)
EV.grid(row=1, column=3, stick='wens', padx=5, pady=5)


CT = ttk.Combobox(win, font=8, values=[1, 2, 3, 4], state="readonly", justify='center')
CT.current(0)
CT.grid(row=1, column=4, stick='wens', padx=5, pady=5)

Confirm_const = tk.Button(win, text='Подтвердить', font=8, command=confirm_const, bd=5)
Confirm_const.grid(row=1, column=5, stick='wens', padx=5, pady=5)

tk.Button(win, text='Инструкция', font=8, command=instruction, bd=5).grid(row=0, column=5, stick='wens', padx=5, pady=5)
win.mainloop()