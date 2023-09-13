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
     JOIN Postavshiki
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
    cur.execute('''SELECT Zayavki.id_zayavki, Zayavki.tovar, Zayavki.kolvo FROM Zayavki WHERE Zayavki.id_postavki IS NULL''')
    [tree4.delete(i) for i in tree4.get_children()]
    [tree4.insert('', 'end', values = row) for row in cur.fetchall()]
  
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
   
def izmenenie(tree3):
    cur.execute('''UPDATE Zakaz SET gotovnost=? WHERE id_zakaza=?''', ("готов", tree3.set(tree3.selection()[0], '#1')))
    conn.commit()
    view3(tree3)

def dobavl(tree4, a, b):
    cur.execute("""INSERT INTO Zayavki(tovar, kolvo) VALUES (?, ?)""", (a, b))
    conn.commit()
    view4(tree4) 
    
def dobav(tree4):
    windowDBV = Tk()
    windowDBV.title("Добавление заявки")
    windowDBV.geometry('310x170')
    windowDBV.resizable(width=False, height = False)
    lbl1 = Label(windowDBV, text="Товар", font=("Times New Roman", 20))
    lbl1.grid(column=0, row=1)
    txt1 = Entry(windowDBV, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt1.grid(column=1, row=1)
    lbl2 = Label(windowDBV, text="Количество", font=("Times New Roman", 20))
    lbl2.grid(column=0, row=2)
    txt2 = Entry(windowDBV, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt2.grid(column=1, row=2)
    btn1 = Button(windowDBV, text="Добавить", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:dobavl(tree4,txt1.get(), txt2.get()))
    btn1.grid(column=0, row=3)
    btn2 = Button(windowDBV, text="Выйти", background="#d7d8e0", font=("Times New Roman", 20), command=windowDBV.destroy)
    btn2.grid(column=1, row=3)
    windowDBV.mainloop()   
    
def vihod(windowKL):
    windowKL.destroy()
    import main

def prinyl(tree, tree2, tree4):
    cur.execute('''SELECT * FROM Zayavki WHERE id_postavki=?''',(tree2.set(tree2.selection()[0], '#1'),))
    z=tree2.set(tree2.selection()[0], '#1')
    k=cur.fetchall()
    for s in k:
        g=s[0]
        a=s[1]
        b=s[2]
        c=s[3]
        d=s[4]
        e=s[5]
        f=s[6]
        cur.execute("SELECT * FROM Tovari;")
        inf_tovari = cur.fetchall()
        chet=0
        flag = True
        for infa in inf_tovari:
            if (infa[1] == a and infa[3] == e and infa[4] == f and infa[5] == c and infa[6] == d):       
                kolv=infa[2]+b
                cur.execute('''UPDATE Tovari SET kolvo=? WHERE id_tovara=?''', (kolv, chet+1))
                cur.execute('''DELETE FROM Zayavki WHERE id_zayavki=?''', (g,))
                cur.execute('''DELETE FROM Postavki WHERE id_postavki=?''', (z,))
                conn.commit()
                view(tree) 
                view2(tree2) 
                view4(tree4)
                flag = False
                break
            chet=chet+1
        if flag:
            cur.execute("""INSERT INTO Tovari(nazvanie, kolvo, sertificat, cena, SrokGodnos, Proizv) VALUES (?, ?, ?, ?, ?, ?)""",(a, b, e, f, c, d))
            cur.execute('''DELETE FROM Zayavki WHERE id_zayavki=?''',(g,))
            cur.execute('''DELETE FROM Postavki WHERE id_postavki=?''', (z,))
            conn.commit()
            view(tree)
            view2(tree2)
            view4(tree4)

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
    windowKL = Tk()
    windowKL.title("Кладовщик")
    windowKL.geometry('950x300')
    windowKL.resizable(width=False, height = False)
    ########----------------########
    tab_control = ttk.Notebook(windowKL) 
    tab1 = ttk.Frame(tab_control)  
    tab2 = ttk.Frame(tab_control) 
    tab3 = ttk.Frame(tab_control)  
    tab4 = ttk.Frame(tab_control) 
    ########----------------########
    tab_control.add(tab1, text='Товары')  
    tab_control.add(tab2, text='Поставки') 
    tab_control.add(tab3, text='Заказы') 
    tab_control.add(tab4, text='Заявки') 
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
    bt3 = Button(tab1, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:vihod(windowKL))
    bt3.pack(side=RIGHT, padx=5,pady=5)
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
    bt5 = Button(tab2, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:vihod(windowKL))
    bt5.pack(side=RIGHT, padx=5, pady=5)
    bt90 = Button(tab2, text="Подробнее", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:podrob(tree2))
    bt90.pack(side=RIGHT, padx=5, pady=5)
    bt5 = Button(tab2, text="Принял",background="#d7d8e0", font=("Times New Roman", 20), command=lambda:prinyl(tree, tree2,tree4))
    bt5.pack(side=RIGHT, padx=10, pady=5)
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
    bt6 = Button(tab3, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:vihod(windowKL))
    bt6.pack(side=RIGHT, padx=5,pady=5)
    bt7 = Button(tab3, text="Изменить", background="#d7d8e0", font=("Times New Roman", 20),command=lambda:izmenenie(tree3))
    bt7.pack(side=RIGHT, padx=5,pady=5) 
    bt3 = Button(tab3, text="Подробнее", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:podr(tree3))
    bt3.pack(side=RIGHT, padx=10,pady=5)
    ########-----ЗАЯВКИ-----########
    tree4 = ttk.Treeview(tab4, columns=('id_zayavki', 'tovar', 'kolvo'),show ='headings')
    tree4.column('id_zayavki', width=300, anchor = tk.CENTER)
    tree4.column('tovar',width=300, anchor = tk.CENTER)
    tree4.column('kolvo',width=300, anchor = tk.CENTER)
    #
    tree4.heading('id_zayavki', text='Номер заявки')
    tree4.heading('tovar', text='Товар')
    tree4.heading('kolvo', text='Количество')
    tree4.pack()
    view4(tree4)
    bt8 = Button(tab4, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:vihod(windowKL))
    bt8.pack(side=RIGHT, padx=5,pady=5)
    bt9 = Button(tab4, text="Добавить", background="#d7d8e0", font=("Times New Roman", 20),command=lambda:dobav(tree4))
    bt9.pack(side=RIGHT, padx=5,pady=5) 
    #
    tab_control.pack(expand=1, fill='both')  
    windowKL.mainloop()