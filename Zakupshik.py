from tkinter import * 
from tkinter import ttk 
import sqlite3
from sqlite3 import Error 
import tkinter as tk
from tkinter.ttk import Combobox 

conn = sqlite3.connect('magazin.db')
cur = conn.cursor()
    
def view(tree):
    cur.execute('''SELECT Tovari.nazvanie, Tovari.kolvo, Tovari.sertificat, Tovari.cena, Tovari.SrokGodnos, Tovari.Proizv FROM Tovari''')
    [tree.delete(i) for i in tree.get_children()]
    [tree.insert('', 'end', values = row) for row in cur.fetchall()]

def view2(tree2):
    cur.execute('''SELECT Postavki.id_postavki, Postavshiki.nazvanie, Postavki.dataZAKAZA
    FROM Postavki
    LEFT JOIN Postavshiki
    ON Postavki.id_postavshika=Postavshiki.id_postavshika
    ''')
    [tree2.delete(i) for i in tree2.get_children()]
    [tree2.insert('', 'end', values = row) for row in cur.fetchall()]

def view3(tree3):
    cur.execute('''SELECT Zakaz.id_zakaza, Personal.familiya, Pokupateli.familiya, Oplata.bankovskie_recv, Zakaz.data_zakaza, Zakaz.data_vidachi, Zakaz.gotovnost
    FROM Zakaz
    LEFT JOIN Personal
    ON Zakaz.id_rabotnika=Personal.id_rabotnika
    LEFT JOIN Pokupateli
    ON Zakaz.id_klienta=Pokupateli.id_klienta
    LEFT JOIN Oplata
    ON Zakaz.id_oplati=Oplata.id_oplati
    ''')
    [tree3.delete(i) for i in tree3.get_children()]
    [tree3.insert('', 'end', values = row) for row in cur.fetchall()]
    
def view4(tree4):
    cur.execute('''SELECT * FROM Postavshiki''')
    [tree4.delete(i) for i in tree4.get_children()]
    [tree4.insert('', 'end', values = row) for row in cur.fetchall()]
    
def view5(tree5):
    cur.execute('''SELECT Zayavki.id_zayavki, Zayavki.tovar, Zayavki.kolvo, Zayavki.SrokGodns, Zayavki.proizv, Zayavki.sertificat, Zayavki.cena 
    FROM Zayavki WHERE Zayavki.id_postavki IS NULL''')
    [tree5.delete(i) for i in tree5.get_children()]
    [tree5.insert('', 'end', values = row) for row in cur.fetchall()]
    
def view6(tree6,a):
    cur.execute('''SELECT Zayavki.tovar, Zayavki.kolvo, Zayavki.SrokGodns, Zayavki.proizv, Zayavki.sertificat, Zayavki.cena 
    FROM Zayavki WHERE Zayavki.id_postavki=?''', (a,))
    [tree6.delete(i) for i in tree6.get_children()]
    [tree6.insert('', 'end', values = row) for row in cur.fetchall()]
   
def view7(tree7,a):    
    cur.execute('''SELECT Tovari.nazvanie, Korzina.kolvo, Korzina.cena 
    FROM Korzina
    LEFT JOIN Tovari
    ON Korzina.id_tovara=Tovari.id_tovara
    WHERE Korzina.id_zakaza=?''', (a,))
    [tree7.delete(i) for i in tree7.get_children()]
    [tree7.insert('', 'end', values = row) for row in cur.fetchall()]
   
def change(tree3, b):
    cur.execute('''UPDATE Zakaz SET gotovnost=? WHERE id_zakaza=?''',
    ( b, tree3.set(tree3.selection()[0], '#1')))
    conn.commit()   
    view3(tree3)

def dobavl(tree4, a, b, c):
    cur.execute("""INSERT INTO Postavshiki(nazvanie, ur_adres, fiz_adres) VALUES (?, ?, ?)""", (a, b, c))
    conn.commit()
    view4(tree4)

def izm1(tree4, a, b, c):
    cur.execute('''UPDATE Postavshiki SET nazvanie=?, ur_adres=?, fiz_adres=? WHERE id_postavshika=?''',
    ( a, b, c, tree4.set(tree4.selection()[0], '#1')))
    conn.commit()   
    view4(tree4)

def dobav2(tree2, a, b, c, d, e, f, g, h):
    cur.execute("""INSERT INTO Postavki(id_postavshika, kolvo, dataZAKAZA, cena, SrokGodn, proizv, sertificat, tovar) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (a, b, c, d, e, f, g, h))
    conn.commit()
    view2(tree2)
    
def dobav(tree4):
    windowDBV = Tk()
    windowDBV.title("Добавление поставщика")
    windowDBV.geometry('300x170')
    windowDBV.resizable(width=False, height = False)
    lbl1 = Label(windowDBV, text="Название",font=("Times New Roman", 20))
    lbl1.grid(column=0, row=1)
    txt1 = Entry(windowDBV, width=10,background="#d7d8e0", font=("Times New Roman", 20))
    txt1.grid(column=1, row=1)
    lbl2 = Label(windowDBV, text="Юр. адрес", font=("Times New Roman", 20))
    lbl2.grid(column=0, row=2)
    txt2 = Entry(windowDBV, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt2.grid(column=1, row=2)
    lbl3 = Label(windowDBV, text="Физ. адрес", font=("Times New Roman", 20))
    lbl3.grid(column=0, row=3)
    txt3 = Entry(windowDBV, width=10,background="#d7d8e0", font=("Times New Roman", 20))
    txt3.grid(column=1, row=3)
    btn1 = Button(windowDBV, text="Добавить", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:dobavl(tree4,txt1.get(), txt2.get(), txt3.get()))
    btn1.grid(column=1, row=4)
    btn2 = Button(windowDBV, text="Выйти", background="#d7d8e0", font=("Times New Roman", 20), command=windowDBV.destroy)
    btn2.grid(column=0, row=4)
    windowDBV.mainloop()
    
def dobavPOS(tree2):
    windowDBP = Tk()
    windowDBP.title("Добавление поставки")
    windowDBP.geometry('350x360')
    windowDBP.resizable(width=False, height = False)
    lbl1 = Label(windowDBP, text="Поставщик", font=("Times New Roman", 20))
    lbl1.grid(column=0, row=1)
    txt1 = Entry(windowDBP, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt1.grid(column=1, row=1)
    lbl2 = Label(windowDBP, text="Количество", font=("Times New Roman", 20))
    lbl2.grid(column=0, row=2)
    txt2 = Entry(windowDBP, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt2.grid(column=1, row=2)
    lbl3 = Label(windowDBP, text="Дата заказа", font=("Times New Roman", 20))
    lbl3.grid(column=0, row=3)
    txt3 = Entry(windowDBP, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt3.grid(column=1, row=3)
    lbl4 = Label(windowDBP, text="Цена", font=("Times New Roman", 20))
    lbl4.grid(column=0, row=4)
    txt4 = Entry(windowDBP, width=10,background="#d7d8e0", font=("Times New Roman", 20))
    txt4.grid(column=1, row=4)
    lbl5 = Label(windowDBP, text="Срок годности", font=("Times New Roman", 20))
    lbl5.grid(column=0, row=5)
    txt5 = Entry(windowDBP, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt5.grid(column=1, row=5)
    lbl5 = Label(windowDBP, text="Производитель", font=("Times New Roman", 20))
    lbl5.grid(column=0, row=6)
    txt6 = Entry(windowDBP, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt6.grid(column=1, row=6)
    lbl5 = Label(windowDBP, text="Сертификат", font=("Times New Roman", 20))
    lbl5.grid(column=0, row=7)
    txt7 = Entry(windowDBP, width=10,background="#d7d8e0", font=("Times New Roman", 20))
    txt7.grid(column=1, row=7)
    lbl5 = Label(windowDBP, text="Товар", font=("Times New Roman", 20))
    lbl5.grid(column=0, row=8)
    txt8 = Entry(windowDBP, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt8.grid(column=1, row=8)
    btn1 = Button(windowDBP, text="Добавить", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:dobav2(tree2,txt1.get(), txt2.get(), txt3.get(), txt4.get(), txt5.get(), txt6.get(), txt7.get(), txt8.get(),))
    btn1.grid(column=0, row=9)
    btn2 = Button(windowDBP, text="Выйти", background="#d7d8e0", font=("Times New Roman", 20), command=windowDBP.destroy)
    btn2.grid(column=1, row=9)
    windowDBP.mainloop()

def izm(tree4):
    windowIZM = Tk()
    windowIZM.title("Изменение поставщика")
    windowIZM.geometry('300x170')
    windowIZM.resizable(width=False, height = False)
    lbl1 = Label(windowIZM, text="Название",font=("Times New Roman", 20))
    lbl1.grid(column=0, row=1)
    txt1 = Entry(windowIZM, width=10,background="#d7d8e0", font=("Times New Roman", 20))
    txt1.grid(column=1, row=1)
    lbl2 = Label(windowIZM, text="Юр. адрес", font=("Times New Roman", 20))
    lbl2.grid(column=0, row=2)
    txt2 = Entry(windowIZM, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt2.grid(column=1, row=2)
    lbl3 = Label(windowIZM, text="Физ. адрес", font=("Times New Roman", 20))
    lbl3.grid(column=0, row=3)
    txt3 = Entry(windowIZM, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt3.grid(column=1, row=3)
    btn1 = Button(windowIZM, text="Изменить", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:izm1(tree4,txt1.get(), txt2.get(), txt3.get()))
    btn1.grid(column=0, row=4)
    btn2 = Button(windowIZM, text="Выйти", background="#d7d8e0", font=("Times New Roman", 20), command=windowIZM.destroy)
    btn2.grid(column=1, row=4)
    windowIZM.mainloop()
    
def izmenenie(tree3):
    cur.execute('''UPDATE Zakaz SET gotovnost=? WHERE id_zakaza=?''', ("заказан", tree3.set(tree3.selection()[0], '#1')))
    conn.commit()
    view3(tree3)
  
def vihod(windowZK):
    windowZK.destroy()
    import main
   
def ud(tree3):
    cur.execute('''DELETE FROM Zakaz WHERE id_zakaza=?''', (tree3.set(tree3.selection()[0], '#1')))
    conn.commit()   
    view3(tree3)
 
def sozdanieDOB(tree2,a, b):
    cur.execute('''SELECT id_postavshika FROM Postavshiki WHERE nazvanie=?''', (a,))
    l = cur.fetchall()
    cur.execute("""INSERT INTO Postavki(id_postavshika, dataZAKAZA) VALUES (?, ?)""", (l[0][0], b))
    conn.commit()
    view2(tree2)
 
def sozdaniePOS(tree5, tree2):
    windowDBP = Tk()
    windowDBP.title("Добавление")
    windowDBP.geometry('300x150')
    windowDBP.resizable(width=False, height = False)
    lbl1 = Label(windowDBP, text="Поставщик", font=("Times New Roman", 20))
    lbl1.grid(column=0, row=1)
    combo = Combobox(windowDBP, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    cur.execute("SELECT nazvanie FROM Postavshiki;")
    inf_klient = cur.fetchall()
    spisok = []
    for srtanaZ in inf_klient:
        if srtanaZ not in spisok:
            spisok.append(srtanaZ)
    combo['values'] =  spisok
    combo.grid(column=1, row=1)
    lbl2 = Label(windowDBP, text="Дата заказа", font=("Times New Roman", 20))
    lbl2.grid(column=0, row=2)
    txt2 = Entry(windowDBP, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt2.grid(column=1, row=2)
    btn1 = Button(windowDBP, text="Добавить", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:sozdanieDOB(tree2,combo.get(), txt2.get()))
    btn1.grid(column=0, row=3)
    btn2 = Button(windowDBP, text="Выйти", background="#d7d8e0", font=("Times New Roman", 20), command=windowDBP.destroy)
    btn2.grid(column=1, row=3)
    windowDBP.mainloop()
    
def dobavVPOS2(tree5, tree2, a):
    cur.execute('''UPDATE Zayavki SET id_postavki=? WHERE id_zayavki=?''',
    (tree2.set(tree2.selection()[0], '#1'), a))
    conn.commit()   
    view2(tree2)
    view5(tree5)
    
def dobavVPOS(tree5):
    windowDBP = Tk()
    windowDBP.title("Добавление")
    windowDBP.geometry('950x280')
    windowDBP.resizable(width=False, height = False)
    a = tree5.set(tree5.selection()[0], '#1')
    tree2 = ttk.Treeview(windowDBP, columns=('id_postavki', 'id_postavshika', 'dataZAKAZA'),show ='headings')
    tree2.column('id_postavki',width=300, anchor = tk.CENTER)
    tree2.column('id_postavshika',width=300, anchor = tk.CENTER)
    tree2.column('dataZAKAZA',width=300, anchor = tk.CENTER)
    #
    tree2.heading('id_postavki', text='Номер')
    tree2.heading('id_postavshika', text='Поставщик')
    tree2.heading('dataZAKAZA', text='Дата заказа')
    tree2.pack()
    view2(tree2)
    bt5 = Button(windowDBP, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:windowDBP.destroy())
    bt5.pack(side=RIGHT, padx=5,pady=5)
    bt2 = Button(windowDBP, text="Добавить", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:dobavVPOS2(tree5, tree2, a))
    bt2.pack(side=RIGHT, padx=5,pady=5)
    bt2 = Button(windowDBP, text="Создать поставку", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:sozdaniePOS(tree5, tree2))
    bt2.pack(side=RIGHT, padx=5,pady=5)
    
def podrob(tree2):
    windowDBP = Tk()
    windowDBP.title("Добавление поставки")
    windowDBP.geometry('950x270')
    windowDBP.resizable(width=False, height = False)
    a = tree2.set(tree2.selection()[0], '#1')
    tree6 = ttk.Treeview(windowDBP, columns=('tovar', 'kolvo', 'SrokGodns','proizv', 'sertificat', 'cena'),show ='headings')
    tree6.column('tovar',width=155, anchor = tk.CENTER)
    tree6.column('kolvo',width=155, anchor = tk.CENTER)
    tree6.column('SrokGodns',width=155, anchor = tk.CENTER)
    tree6.column('proizv',width=155, anchor = tk.CENTER)
    tree6.column('sertificat',width=155, anchor = tk.CENTER)
    tree6.column('cena',width=155, anchor = tk.CENTER)
    #
    tree6.heading('tovar', text='Товар')
    tree6.heading('kolvo', text='Количество')
    tree6.heading('SrokGodns', text='Срок годности')
    tree6.heading('proizv', text='Производитель')
    tree6.heading('sertificat', text='Сертификат')
    tree6.heading('cena', text='Цена')
    tree6.pack()
    view6(tree6,a)
    bt8 = Button(windowDBP, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:windowDBP.destroy())
    bt8.pack(side=RIGHT, padx=5,pady=5)
 
def dobavINF2(tree5, a, b, c, d):
    cur.execute('''UPDATE Zayavki SET SrokGodns=?, proizv=?, sertificat=?, cena=? WHERE id_zayavki=?''',
    ( a, b, c, d, tree5.set(tree5.selection()[0], '#1')))
    conn.commit()   
    view5(tree5)
 
def dobavINF(tree5):
    windowIZM = Tk()
    windowIZM.title("Изменение заказа")
    windowIZM.geometry('340x260')
    windowIZM.resizable(width=False, height = False)
    lbl1 = Label(windowIZM, text="Срок годности", font=("Times New Roman", 20))
    lbl1.grid(column=0, row=1)
    txt1 = Entry(windowIZM, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt1.grid(column=1, row=1)
    lbl2 = Label(windowIZM, text="Производитель", font=("Times New Roman", 20))
    lbl2.grid(column=0, row=2)
    txt2 = Entry(windowIZM, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt2.grid(column=1, row=2)
    lbl3 = Label(windowIZM, text="Сертификат", font=("Times New Roman", 20))
    lbl3.grid(column=0, row=3)
    txt3 = Entry(windowIZM, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt3.grid(column=1, row=3)
    lbl4 = Label(windowIZM, text="Цена", font=("Times New Roman", 20))
    lbl4.grid(column=0, row=4)
    txt4 = Entry(windowIZM, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt4.grid(column=1, row=4)
    btn1 = Button(windowIZM, text="Добавить", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:dobavINF2(tree5,txt1.get(),txt2.get(),txt3.get(),txt4.get()))
    btn1.grid(column=0, row=5)
    btn2 = Button(windowIZM, text="Выйти", background="#d7d8e0", font=("Times New Roman", 20), command=windowIZM.destroy)
    btn2.grid(column=1, row=5)
    windowIZM.mainloop()

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

def podr(tree3):
    windowDBP = Tk()
    windowDBP.title("Подробнее о заказе")
    windowDBP.geometry('900x270')
    windowDBP.resizable(width=False, height = False)
    a = tree3.set(tree3.selection()[0], '#1')
    tree7 = ttk.Treeview(windowDBP, columns=('tovar', 'kolvo','cena'),show ='headings')
    tree7.column('tovar',width=300, anchor = tk.CENTER)
    tree7.column('kolvo',width=300, anchor = tk.CENTER)
    tree7.column('cena',width=300, anchor = tk.CENTER)
    #
    tree7.heading('tovar', text='Товар')
    tree7.heading('kolvo', text='Количество')
    tree7.heading('cena', text='Цена')
    tree7.pack()
    view7(tree7,a)
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
    windowZK = Tk()
    windowZK.title("Закупщик")
    windowZK.geometry('950x300')
    windowZK.resizable(width=False, height = False)
    ########----------------########
    tab_control = ttk.Notebook(windowZK) 
    tab1 = ttk.Frame(tab_control)  
    tab2 = ttk.Frame(tab_control) 
    tab3 = ttk.Frame(tab_control)
    tab4 = ttk.Frame(tab_control)
    tab5 = ttk.Frame(tab_control)
    ########----------------########
    tab_control.add(tab1, text='Товары')  
    tab_control.add(tab2, text='Поставки') 
    tab_control.add(tab3, text='Заказы')
    tab_control.add(tab4, text='Поставщики')  
    tab_control.add(tab5, text='Заявки')
    ########-----ТОВАРЫ-----########
    tree = ttk.Treeview(tab1, columns=('nazvanie', 'kolvo', 'sertificat', 'cena', 'SrokGodnos', 'Proizv',),show ='headings')
    tree.column('nazvanie',width=150, anchor = tk.CENTER)
    tree.column('kolvo',width=150, anchor = tk.CENTER)
    tree.column('sertificat',width=150, anchor = tk.CENTER)
    tree.column('cena',width=150, anchor = tk.CENTER)
    tree.column('SrokGodnos',width=150, anchor = tk.CENTER)
    tree.column('Proizv',width=150, anchor = tk.CENTER)
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
    bt4 = Button(tab1, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:vihod(windowZK))
    bt4.pack(side=RIGHT, padx=5,pady=5)
    bt3 = Button(tab1, text="Поиск", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:poisk(tree))
    bt3.pack(side=RIGHT, padx=5,pady=5)
    ########-----ПОСТАВКИ-----########
    tree2 = ttk.Treeview(tab2, columns=('id_postavki', 'id_postavshika', 'dataZAKAZA'),show ='headings')
    tree2.column('id_postavki',width=300, anchor = tk.CENTER)
    tree2.column('id_postavshika',width=300, anchor = tk.CENTER)
    tree2.column('dataZAKAZA',width=300, anchor = tk.CENTER)
    #
    tree2.heading('id_postavki', text='Номер')
    tree2.heading('id_postavshika', text='Поставщик')
    tree2.heading('dataZAKAZA', text='Дата заказа')
    tree2.pack()
    view2(tree2)
    #
    bt5 = Button(tab2, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:vihod(windowZK))
    bt5.pack(side=RIGHT, padx=5,pady=5)
    bt2 = Button(tab2, text="Добавить", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:sozdaniePOS(tree5, tree2))
    bt2.pack(side=RIGHT, padx=5,pady=5)
    bt90 = Button(tab2, text="Подробнее", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:podrob(tree2))
    bt90.pack(side=RIGHT, padx=5,pady=5)
    bt90 = Button(tab2, text="Обновить", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:view2(tree2))
    bt90.pack(side=RIGHT, padx=5,pady=5)
    ########-----ЗАКАЗЫ-----########
    tree3 = ttk.Treeview(tab3, columns=('id_zakaza', 'id_rabotnika', 'id_klienta', 'id_oplati', 'data_zakaza', 'data_vidachi', 'gotovnost'),show ='headings')
    tree3.column('id_zakaza', width=135, anchor = tk.CENTER)
    tree3.column('id_rabotnika',width=135, anchor = tk.CENTER)
    tree3.column('id_klienta',width=135, anchor = tk.CENTER)
    tree3.column('id_oplati',width=135, anchor = tk.CENTER)
    tree3.column('data_zakaza', width=135, anchor = tk.CENTER)
    tree3.column('data_vidachi', width=135, anchor = tk.CENTER)
    tree3.column('gotovnost', width=135, anchor = tk.CENTER)
    #
    tree3.heading('id_zakaza', text='ID')
    tree3.heading('id_rabotnika', text='Работник')
    tree3.heading('id_klienta', text='Клиент')
    tree3.heading('id_oplati', text='Оплата')
    tree3.heading('data_zakaza', text='Дата заказа')
    tree3.heading('data_vidachi', text='Дата выдачи')
    tree3.heading('gotovnost', text='Стадия')
    tree3.pack()
    view3(tree3)
    bt6 = Button(tab3, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:vihod(windowZK))
    bt6.pack(side=RIGHT, padx=5,pady=5)
    bt7 = Button(tab3, text="Изменить", background="#d7d8e0", font=("Times New Roman", 20),command=lambda:izmenenie(tree3))
    bt7.pack(side=RIGHT, padx=5,pady=5) 
    bt3 = Button(tab3, text="Подробнее", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:podr(tree3))
    bt3.pack(side=RIGHT, padx=10,pady=5)
    ########-----ПОСТАВЩИКИ-----########
    tree4 = ttk.Treeview(tab4, columns=('id_postavshika', 'nazvanie', 'ur_adres', 'fiz_adres'), show ='headings')
    tree4.column('id_postavshika',width=230, anchor = tk.CENTER)
    tree4.column('nazvanie',width=230, anchor = tk.CENTER)
    tree4.column('ur_adres',width=230, anchor = tk.CENTER)
    tree4.column('fiz_adres',width=230, anchor = tk.CENTER)
    #
    tree4.heading('id_postavshika', text='ID')
    tree4.heading('nazvanie', text='Название')
    tree4.heading('ur_adres', text='Юр. адрес')
    tree4.heading('fiz_adres', text='Физ. адрес')
    tree4.pack()
    view4(tree4)
    bt4 = Button(tab4, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:vihod(windowZK))
    bt4.pack(side=RIGHT, padx=5,pady=5)
    bt2 = Button(tab4, text="Изменить", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:izm(tree4))
    bt2.pack(side=RIGHT, padx=5,pady=5)
    bt = Button(tab4, text="Добавить", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:dobav(tree4))
    bt.pack(side=RIGHT, padx=5,pady=5)
    ########-----ЗАЯВКИ-----########
    tree5 = ttk.Treeview(tab5, columns=('id_zayavki', 'tovar', 'kolvo','SrokGodn','proizv','sertificat','cena'),show ='headings')
    tree5.column('id_zayavki', width=100, anchor = tk.CENTER)
    tree5.column('tovar',width=200, anchor = tk.CENTER)
    tree5.column('kolvo',width=150, anchor = tk.CENTER)
    tree5.column('SrokGodn',width=100, anchor = tk.CENTER)
    tree5.column('proizv',width=100, anchor = tk.CENTER)
    tree5.column('sertificat',width=100, anchor = tk.CENTER)
    tree5.column('cena',width=150, anchor = tk.CENTER)
    ##################
    tree5.heading('id_zayavki', text='Номер заявки')
    tree5.heading('tovar', text='Товар')
    tree5.heading('kolvo', text='Количество')
    tree5.heading('SrokGodn', text='Срок годности')
    tree5.heading('proizv', text='Производитель')
    tree5.heading('sertificat', text='Сертификат')
    tree5.heading('cena', text='Цена')
    tree5.pack()
    view5(tree5)
    ##################
    bt8 = Button(tab5, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:vihod(windowZK))
    bt8.pack(side=RIGHT, padx=5,pady=5)
    bt9 = Button(tab5, text="Добавить в поставку", background="#d7d8e0", font=("Times New Roman", 20),command=lambda:dobavVPOS(tree5))
    bt9.pack(side=RIGHT, padx=5,pady=5) 
    bt9 = Button(tab5, text="Добавить информацию", background="#d7d8e0", font=("Times New Roman", 20),command=lambda:dobavINF(tree5))
    bt9.pack(side=RIGHT, padx=5,pady=5) 
    ##################
    tab_control.pack(expand=1, fill='both')  
    windowZK.mainloop()
    