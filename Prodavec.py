from tkinter import * 
from tkinter import ttk 
import sqlite3
from sqlite3 import Error 
import tkinter as tk
from datetime import date
from tkinter.ttk import Combobox 

conn = sqlite3.connect('magazin.db')
cur = conn.cursor()

def view(tree):
    cur.execute('''SELECT Tovari.nazvanie, Tovari.kolvo, Tovari.sertificat, Tovari.cena, Tovari.SrokGodnos, Tovari.Proizv FROM Tovari''')
    [tree.delete(i) for i in tree.get_children()]
    [tree.insert('', 'end', values = row) for row in cur.fetchall()]

def view2(tree2):
    cur.execute('''SELECT Zakaz.id_zakaza, Personal.familiya, Pokupateli.familiya, Oplata.bankovskie_recv, Zakaz.data_zakaza, Zakaz.data_vidachi, Zakaz.gotovnost
    FROM Zakaz
    LEFT JOIN Personal
    ON Zakaz.id_rabotnika=Personal.id_rabotnika
    LEFT JOIN Pokupateli
    ON Zakaz.id_klienta=Pokupateli.id_klienta
    LEFT JOIN Oplata
    ON Zakaz.id_oplati=Oplata.id_oplati
    ''')
    [tree2.delete(i) for i in tree2.get_children()]
    [tree2.insert('', 'end', values = row) for row in cur.fetchall()]

def view3(tree3):
    cur.execute('''SELECT * FROM Pokupateli''')
    [tree3.delete(i) for i in tree3.get_children()]
    [tree3.insert('', 'end', values = row) for row in cur.fetchall()]
 
def view6(tree6,a):    
    cur.execute('''SELECT Tovari.nazvanie, Korzina.kolvo, Korzina.cena 
    FROM Korzina
    LEFT JOIN Tovari
    ON Korzina.id_tovara=Tovari.id_tovara
    WHERE Korzina.id_zakaza=?''', (a,))
    [tree6.delete(i) for i in tree6.get_children()]
    [tree6.insert('', 'end', values = row) for row in cur.fetchall()]
 
def ud(tree3):
    cur.execute('''DELETE FROM Pokupateli WHERE id_klienta=?''', (tree3.set(tree3.selection()[0], '#1')))
    conn.commit()   
    view3(tree3)
    
def izmenenie(tree2, h):
    current_date = date.today()
    cur.execute('''UPDATE Zakaz SET id_rabotnika=?, data_vidachi=?, gotovnost=? WHERE id_zakaza=?''', ( h[0][0], current_date, "выдан", tree2.set(tree2.selection()[0], '#1')))
    conn.commit()
    view2(tree2)

def dobavl(tree3, a, b, c, d):
    cur.execute("""INSERT INTO Pokupateli(imya, familiya, telefon, mail) VALUES (?, ?, ?, ?)""", (a, b, c, d))
    conn.commit()
    view3(tree3) 

def dobav(tree3):
    windowDBV = Tk()
    windowDBV.title("Добавление клиента")
    windowDBV.geometry('280x220')
    windowDBV.resizable(width=False, height = False)
    lbl1 = Label(windowDBV, text="Имя",font=("Times New Roman", 20))
    lbl1.grid(column=0, row=1)
    txt1 = Entry(windowDBV, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt1.grid(column=1, row=1)
    lbl2 = Label(windowDBV, text="Фамилия",font=("Times New Roman", 20))
    lbl2.grid(column=0, row=2)
    txt2 = Entry(windowDBV, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt2.grid(column=1, row=2)
    lbl3 = Label(windowDBV, text="Телефон",font=("Times New Roman", 20))
    lbl3.grid(column=0, row=3)
    txt3 = Entry(windowDBV, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt3.grid(column=1, row=3)
    lbl4 = Label(windowDBV, text="Mail",font=("Times New Roman", 20))
    lbl4.grid(column=0, row=4)
    txt4 = Entry(windowDBV, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt4.grid(column=1, row=4)
    btn1 = Button(windowDBV, text="Добавить", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:dobavl(tree3,txt1.get(), txt2.get(), txt3.get(), txt4.get()))
    btn1.grid(column=0, row=5)
    btn2 = Button(windowDBV, text="Выйти", background="#d7d8e0", font=("Times New Roman", 20), command=windowDBV.destroy)
    btn2.grid(column=1, row=5)
    windowDBV.mainloop()

def izm1(tree3, a, b, c, d):
    cur.execute('''UPDATE Pokupateli SET imya=?, familiya=?, telefon=?, mail=? WHERE id_klienta=?''',
    ( a, b, c, d, tree3.set(tree3.selection()[0], '#1')))
    conn.commit()   
    view3(tree3)

def izm(tree3):
    windowIZM = Tk()
    windowIZM.title("Изменение покуптаеля")
    windowIZM.geometry('290x220')
    windowIZM.resizable(width=False, height = False)
    lbl1 = Label(windowIZM, text="Имя",font=("Times New Roman", 20))
    lbl1.grid(column=0, row=1)
    txt1 = Entry(windowIZM, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt1.grid(column=1, row=1)
    lbl2 = Label(windowIZM, text="Фамилия",font=("Times New Roman", 20))
    lbl2.grid(column=0, row=2)
    txt2 = Entry(windowIZM, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt2.grid(column=1, row=2)
    lbl3 = Label(windowIZM, text="Телефон",font=("Times New Roman", 20))
    lbl3.grid(column=0, row=3)
    txt3 = Entry(windowIZM, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt3.grid(column=1, row=3)
    lbl4 = Label(windowIZM, text="Mail",font=("Times New Roman", 20))
    lbl4.grid(column=0, row=4)
    txt4 = Entry(windowIZM, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt4.grid(column=1, row=4)
    btn1 = Button(windowIZM, text="Изменить", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:izm1(tree3,txt1.get(), txt2.get(), txt3.get(), txt4.get()))
    btn1.grid(column=0, row=5)
    btn2 = Button(windowIZM, text="Выйти", background="#d7d8e0", font=("Times New Roman", 20), command=windowIZM.destroy)
    btn2.grid(column=1, row=5)
    windowIZM.mainloop()

def vihod(windowPRO):
    windowPRO.destroy()
    import main

def psk(tree, a):
    a = ('%' + a + '%',)
    cur.execute('''SELECT Tovari.nazvanie, Tovari.kolvo, Tovari.sertificat, Tovari.cena, Tovari.SrokGodnos, Tovari.Proizv FROM Tovari WHERE Tovari.nazvanie LIKE ?''',a)
    [tree.delete(i) for i in tree.get_children()]
    [tree.insert('', 'end', values = row) for row in cur.fetchall()]

def poisk(tree):
    windowpoi = Tk()
    windowpoi.title("Поиск")
    windowpoi.geometry('280x100')
    windowpoi.resizable(width=False, height = False)
    lbl1 = Label(windowpoi, text="Товар:", font=("Times New Roman", 20))
    lbl1.grid(column=0, row=0)
    combo = Combobox(windowpoi, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    cur.execute("SELECT nazvanie FROM Tovari;")
    inf = cur.fetchall()
    spisok = []
    for s in inf:
        if s not in spisok:
            spisok.append(s)
    combo['values'] =  spisok
    combo.grid(column=1, row=0)
    bt3 = Button(windowpoi, text="Найти",background="#d7d8e0", font=("Times New Roman", 20), command=lambda:psk(tree, combo.get()))
    bt3.grid(column=1, row=1)
    btn2 = Button(windowpoi, text="Выйти", background="#d7d8e0", font=("Times New Roman", 20), command=windowpoi.destroy)
    btn2.grid(column=0, row=1)

def podr(tree2):
    windowDBP = Tk()
    windowDBP.title("Подробнее о заказе")
    windowDBP.geometry('900x270')
    windowDBP.resizable(width=False, height = False)
    a = tree2.set(tree2.selection()[0], '#1')
    tree6 = ttk.Treeview(windowDBP, columns=('tovar', 'kolvo','cena'),show ='headings')
    tree6.column('tovar',width=300, anchor = tk.CENTER)
    tree6.column('kolvo',width=300, anchor = tk.CENTER)
    tree6.column('cena',width=300, anchor = tk.CENTER)
    #
    tree6.heading('tovar', text='Товар')
    tree6.heading('kolvo', text='Количество')
    tree6.heading('cena', text='Цена')
    tree6.pack()
    view6(tree6,a)
    cur.execute('''SELECT cena FROM Korzina WHERE id_zakaza=?''', (a,))
    a = cur.fetchall()
    cen=0
    for i in a:
        cen = cen + i[0]
    bt8 = Button(windowDBP, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:windowDBP.destroy())
    bt8.pack(side=RIGHT, padx=5,pady=5) 
    lbl1 = Label(windowDBP, text=cen, font=("Times New Roman", 20))
    lbl1.pack(side=RIGHT, padx=5,pady=5) 
    lbl1 = Label(windowDBP, text="Итоговая цена:", font=("Times New Roman", 20))
    lbl1.pack(side=RIGHT, padx=5,pady=5)

def zapusk(ID):
    windowPRO = Tk()
    windowPRO.title("Продавец")
    windowPRO.geometry('950x300')
    windowPRO.resizable(width=False, height = False)
    ########----------------########
    cur.execute('''SELECT id_rabotnika FROM Personal WHERE id_parol=?''',(ID,))
    h=cur.fetchall() 
    tab_control = ttk.Notebook(windowPRO) 
    tab1 = ttk.Frame(tab_control)  
    tab2 = ttk.Frame(tab_control) 
    tab3 = ttk.Frame(tab_control)
    ########----------------########
    tab_control.add(tab1, text='Товары')  
    tab_control.add(tab2, text='Заказы')
    tab_control.add(tab3, text='Покупатели')  
    ########-----ТОВАРЫ-----########
    tree = ttk.Treeview(tab1, columns=('nazvanie', 'kolvo', 'sertificat', 'cena', 'SrokGodnos', 'Proizv',),show ='headings')
    tree.column('nazvanie',width=155, anchor = tk.CENTER)
    tree.column('kolvo',width=155, anchor = tk.CENTER)
    tree.column('sertificat',width=155, anchor = tk.CENTER)
    tree.column('cena',width=155, anchor = tk.CENTER)
    tree.column('SrokGodnos',width=155, anchor = tk.CENTER)
    tree.column('Proizv',width=155, anchor = tk.CENTER)
    #
    tree.heading('nazvanie', text='Название')
    tree.heading('kolvo', text='Количество')
    tree.heading('sertificat', text='Сертификат')
    tree.heading('cena', text='Цена')
    tree.heading('SrokGodnos', text='Срок Годности')
    tree.heading('Proizv', text='Производитель')
    tree.pack()
    view(tree)
    #
    scroll = tk.Scrollbar(command=tree.yview)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scroll.set)
    #
    bt3 = Button(tab1, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:vihod(windowPRO))
    bt3.pack(side=RIGHT, padx=5,pady=5)
    bt3 = Button(tab1, text="Поиск", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:poisk(tree))
    bt3.pack(side=RIGHT, padx=5,pady=5)
    ########-----ЗАКАЗЫ-----########
    tree2 = ttk.Treeview(tab2, columns=('id_zakaza', 'id_rabotnika', 'id_klienta', 'id_oplati', 'data_zakaza', 'data_vidachi', 'gotovnost'),show ='headings')
    tree2.column('id_zakaza', width=135, anchor = tk.CENTER)
    tree2.column('id_rabotnika',width=135, anchor = tk.CENTER)
    tree2.column('id_klienta',width=135, anchor = tk.CENTER)
    tree2.column('id_oplati',width=135, anchor = tk.CENTER)
    tree2.column('data_zakaza', width=135, anchor = tk.CENTER)
    tree2.column('data_vidachi', width=135, anchor = tk.CENTER)
    tree2.column('gotovnost', width=135, anchor = tk.CENTER)
    #
    tree2.heading('id_zakaza', text='ID')
    tree2.heading('id_rabotnika', text='Работник')
    tree2.heading('id_klienta', text='Клиент')
    tree2.heading('id_oplati', text='Оплата')
    tree2.heading('data_zakaza', text='Дата заказа')
    tree2.heading('data_vidachi', text='Дата выдачи')
    tree2.heading('gotovnost', text='Стадия')
    tree2.pack()
    view2(tree2)
    bt6 = Button(tab2, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:vihod(windowPRO))
    bt6.pack(side=RIGHT, padx=5,pady=5)
    bt7 = Button(tab2, text="Изменить", background="#d7d8e0", font=("Times New Roman", 20),command=lambda:izmenenie(tree2, h))
    bt7.pack(side=RIGHT, padx=5,pady=5) 
    bt3 = Button(tab2, text="Подробнее", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:podr(tree2))
    bt3.pack(side=RIGHT, padx=10,pady=5)
    ########-----ПОКУПАТЕЛИ-----########
    tree3 = ttk.Treeview(tab3, columns=('id_klienta', 'imya', 'familiya', 'telefon', 'mail'), show ='headings')
    tree3.column('id_klienta',width=185, anchor = tk.CENTER)
    tree3.column('imya',width=185, anchor = tk.CENTER)
    tree3.column('familiya',width=185, anchor = tk.CENTER)
    tree3.column('telefon',width=185, anchor = tk.CENTER)
    tree3.column('mail',width=185, anchor = tk.CENTER)
    #
    tree3.heading('id_klienta', text='ID')
    tree3.heading('imya', text='Имя')
    tree3.heading('familiya', text='Фамилия')
    tree3.heading('telefon', text='Телефон')
    tree3.heading('mail', text='Mail')
    tree3.pack()
    view3(tree3)
    bt2 = Button(tab3, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:vihod(windowPRO))
    bt2.pack(side=RIGHT, padx=5,pady=5)
    bt10 = Button(tab3, text="Удаление", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:ud(tree3))
    bt10.pack(side=RIGHT, padx=5,pady=5)
    bt3 = Button(tab3, text="Изменить", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:izm(tree3))
    bt3.pack(side=RIGHT, padx=5,pady=5)
    bt = Button(tab3, text="Добавить", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:dobav(tree3))
    bt.pack(side=RIGHT, padx=5,pady=5)
    #
    tab_control.pack(expand=1, fill='both')  
    windowPRO.mainloop()