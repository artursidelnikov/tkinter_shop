from tkinter import * 
from tkinter import ttk 
import sqlite3
from sqlite3 import Error
from tkinter import messagebox 
import tkinter as tk
from datetime import date
from tkinter.ttk import Combobox 

conn = sqlite3.connect('magazin.db')
cur = conn.cursor()

def vihod(windowPRO):
    windowPRO.destroy()
    import main

def view(tree):
    cur.execute('''SELECT Tovari.id_tovara, Tovari.nazvanie, Tovari.kolvo, Tovari.sertificat, Tovari.cena, Tovari.SrokGodnos, Tovari.Proizv FROM Tovari''')
    [tree.delete(i) for i in tree.get_children()]
    [tree.insert('', 'end', values = row) for row in cur.fetchall()]

def pod(h):
    windowDBP = Tk()
    windowDBP.title("Итоговая цена")
    windowDBP.geometry('250x40')
    windowDBP.resizable(width=False, height = False)
    cur.execute('''SELECT cena FROM Korzina WHERE Korzina.id_zakaza IS NULL AND Korzina.id_klienta=?''', (h[0][0],))
    a = cur.fetchall()
    cen=0
    for i in a:
        cen = cen + i[0]
    #
    lbl1 = Label(windowDBP, text=cen, font=("Times New Roman", 20))
    lbl1.grid(column=1, row=0)
    lbl1 = Label(windowDBP, text="Итоговая цена:", font=("Times New Roman", 20))
    lbl1.grid(column=0, row=0) 

def view2(tree2,h):
    cur.execute('''SELECT Korzina.id_korziny, Pokupateli.familiya, Tovari.nazvanie, Korzina.kolvo, Korzina.cena
    FROM Korzina
    LEFT JOIN Pokupateli
    ON Korzina.id_klienta=Pokupateli.id_klienta
    LEFT JOIN Tovari
    ON Korzina.id_tovara=Tovari.id_tovara
    WHERE Korzina.id_zakaza IS NULL AND Korzina.id_klienta=?''', (h[0][0],))
    [tree2.delete(i) for i in tree2.get_children()]
    [tree2.insert('', 'end', values = row) for row in cur.fetchall()]
        
def view3(tree3, h):
    cur.execute('''SELECT Zakaz.id_zakaza, Pokupateli.familiya, Oplata.bankovskie_recv, Zakaz.data_zakaza, Zakaz.gotovnost 
    FROM Zakaz
    LEFT JOIN Pokupateli
    ON Zakaz.id_klienta=Pokupateli.id_klienta
    LEFT JOIN Oplata
    ON Zakaz.id_oplati=Oplata.id_oplati
    WHERE Zakaz.id_klienta=?''', (h[0][0],))
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

def psk(tree,a):
    a = ('%' + a + '%',)
    cur.execute('''SELECT * FROM Tovari WHERE nazvanie LIKE ?''',a)
    [tree.delete(i) for i in tree.get_children()]
    [tree.insert('', 'end', values = row) for row in cur.fetchall()]   
       
def dobavl(tree, a, b):
    cur.execute("SELECT * FROM Tovari;")
    inf_tovari = cur.fetchall()
    chet=0
    for infa in inf_tovari:
        if (infa[0] == int(a)):
            kolv=infa[2]-int(b)
            cur.execute('''UPDATE Tovari SET kolvo=? WHERE id_tovara=?''', (kolv, chet+1))
            conn.commit()
            view(tree) 
            cur.execute("""INSERT INTO Korzina(id_tovara, kolvo, cena) VALUES (?, ?, ?)""", (a, b, infa[5]))
            conn.commit() 
            break
        chet=chet+1
   
def dobv(tree, ID, tree2): 
    cur.execute('''SELECT id_klienta FROM Pokupateli WHERE id_parol=?''',(ID,))
    h=cur.fetchall() 
    a = tree.set(tree.selection()[0], '#1')
    cur.execute('''SELECT * FROM Tovari WHERE id_tovara=?''',(a,))
    k=cur.fetchall()  
    v = k[0]
    cur.execute("""INSERT INTO Korzina(id_klienta, id_tovara, kolvo, cena) VALUES (?, ?, ?, ?)""", (h[0][0], v[0], "1", v[4]))
    cur.execute('''UPDATE Tovari SET kolvo=? WHERE id_tovara=?''',( v[2]-1, tree.set(tree.selection()[0], '#1')))
    conn.commit()
    view(tree)
    view2(tree2, h)

def change(tree2, b, a, tree,h):
    cur.execute('''SELECT id_tovara, kolvo, cena FROM Korzina WHERE id_korziny=?''',(a,))
    v=cur.fetchall()
    kol = int(b) - v[0][1]
    cur.execute('''SELECT kolvo FROM Tovari WHERE id_tovara=?''', (v[0][0],))
    k=cur.fetchall()
    if int(b) == 0:
        klv = k[0][0] + v[0][1]
        cur.execute('''UPDATE Tovari SET kolvo=? WHERE id_tovara=?''',(klv, v[0][0]))
        cur.execute('''DELETE FROM Korzina WHERE id_korziny=?''', (a,))
        conn.commit() 
        view(tree)        
        view2(tree2,h)
    if k[0][0] > kol:
        cen = int(b) * v[0][2]
        cur.execute('''UPDATE Korzina SET kolvo=?, cena=? WHERE id_korziny=?''',(int(b), cen, a))
        kolv = k[0][0] - kol
        cur.execute('''UPDATE Tovari SET kolvo=? WHERE id_tovara=?''',(kolv, v[0][0]))
        conn.commit() 
        view(tree)        
        view2(tree2,h)
    if k[0][0] < kol:
        messagebox.showerror("Ошибка!", "На данный момент нет столько товара!")
     
def izm(tree2, tree,h):
    windowIZM = Tk()
    windowIZM.title("Изменение количества")
    windowIZM.geometry('300x100')
    a = tree2.set(tree2.selection()[0], '#1')
    lbl1 = Label(windowIZM, text="Количество", font=("Times New Roman", 20))
    lbl1.grid(column=0, row=1)
    txt1 = Entry(windowIZM, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt1.grid(column=1, row=1)
    btn1 = Button(windowIZM, text="Изменить", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:change(tree2, txt1.get(), a, tree,h))
    btn1.grid(column=0, row=2)
    btn2 = Button(windowIZM, text="Выйти", background="#d7d8e0", font=("Times New Roman", 20), command=windowIZM.destroy)
    btn2.grid(column=1, row=2)
    windowIZM.mainloop()

def ud(tree2, tree, h):
    a = tree2.set(tree2.selection()[0], '#1')
    cur.execute('''SELECT id_tovara, kolvo FROM Korzina WHERE id_korziny=?''',(a,))
    v=cur.fetchall()
    cur.execute('''SELECT kolvo FROM Tovari WHERE id_tovara=?''', (v[0][0],))
    k=cur.fetchall()
    klv = k[0][0] + v[0][1]
    cur.execute('''UPDATE Tovari SET kolvo=? WHERE id_tovara=?''',(klv, v[0][0]))
    cur.execute('''DELETE FROM Korzina WHERE id_korziny=?''', (a,))
    conn.commit() 
    view(tree)        
    view2(tree2,h)

def oform2(tree2, a, h, tree3):
    current_date = date.today()
    cur.execute('''SELECT id_oplati FROM Oplata WHERE bankovskie_recv=?''', (a,))
    l = cur.fetchall()
    cur.execute("""INSERT INTO Zakaz(id_klienta, id_oplati, data_zakaza, gotovnost) VALUES (?, ?, ?, ?)""", (h[0][0], l[0][0], current_date, "оформлен"))    
    cur.execute("""SELECT id_zakaza FROM Zakaz ORDER BY id_zakaza DESC LIMIT 1;""")
    v=cur.fetchall()
    cur.execute('''SELECT Korzina.id_korziny, Pokupateli.familiya, Tovari.nazvanie, Korzina.kolvo, Korzina.cena
    FROM Korzina
    LEFT JOIN Pokupateli
    ON Korzina.id_klienta=Pokupateli.id_klienta
    LEFT JOIN Tovari
    ON Korzina.id_tovara=Tovari.id_tovara
    WHERE Korzina.id_zakaza IS NULL AND Korzina.id_klienta=?''', (h[0][0],))
    o=cur.fetchall()
    print(o)
    for i in o:
        cur.execute('''UPDATE Korzina SET id_zakaza=? WHERE id_korziny=?''', (v[0][0], i[0]))
        print(i)
        conn.commit()
        view2(tree2,h) 
        view3(tree3,h)
    
def oform(tree2, h, tree3):
    windowOF = Tk()
    windowOF.title("Терминал клиента")
    windowOF.geometry('330x100')
    windowOF.resizable(width=False, height = False)
    lbl1 = Label(windowOF, text="Оплата", font=("Times New Roman", 20))
    lbl1.grid(column=0, row=1)
    combo = Combobox(windowOF, width=10, background="#d7d8e0", font=("Times New Roman", 20))
    cur.execute("SELECT bankovskie_recv FROM Oplata;")
    inf_klient = cur.fetchall()
    spisok = []
    for srtanaZ in inf_klient:
        if srtanaZ not in spisok:
            spisok.append(srtanaZ)
    combo['values'] =  spisok
    combo.grid(column=1, row=1)
    bt3 = Button(windowOF, text="Оформить", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:oform2(tree2,combo.get(), h, tree3))
    bt3.grid(column=0, row=2)
    bt3 = Button(windowOF, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:windowOF.destroy)
    bt3.grid(column=1, row=2)
    windowOF.mainloop() 

def psk(tree, a):
    a = ('%' + a + '%',)
    cur.execute('''SELECT * FROM Tovari WHERE nazvanie LIKE ?''',a)
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
    windowKL = Tk()
    windowKL.title("Терминал клиента")
    windowKL.geometry('950x300')
    windowKL.resizable(width=False, height = False)
    ########----------------########
    cur.execute('''SELECT id_klienta FROM Pokupateli WHERE id_parol=?''',(ID,))
    h=cur.fetchall() 
    tab_control = ttk.Notebook(windowKL) 
    tab1 = ttk.Frame(tab_control)  
    tab2 = ttk.Frame(tab_control) 
    tab3 = ttk.Frame(tab_control)  
    ########----------------########
    tab_control.add(tab1, text='Товары')  
    tab_control.add(tab2, text='Корзина') 
    tab_control.add(tab3, text='Заказы')
    ########-----ТОВАРЫ-----########
    tree = ttk.Treeview(tab1, columns=('id_tovara', 'nazvanie', 'kolvo', 'sertificat', 'cena', 'SrokGodnos', 'Proizv',),show ='headings')
    tree.column('id_tovara',width=105, anchor = tk.CENTER)
    tree.column('nazvanie',width=130, anchor = tk.CENTER)
    tree.column('kolvo',width=110, anchor = tk.CENTER)
    tree.column('sertificat',width=150, anchor = tk.CENTER)
    tree.column('cena',width=150, anchor = tk.CENTER)
    tree.column('SrokGodnos',width=150, anchor = tk.CENTER)
    tree.column('Proizv',width=150, anchor = tk.CENTER)
    #
    tree.heading('id_tovara',text='ID')
    tree.heading('nazvanie', text='Название')
    tree.heading('kolvo', text='Количество')
    tree.heading('sertificat', text='Сертификат')
    tree.heading('cena', text='Цена')
    tree.heading('SrokGodnos', text='Срок Годности')
    tree.heading('Proizv', text='Производитель')
    tree.pack()
    view(tree)
    scroll = tk.Scrollbar(command=tree.yview)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scroll.set)
    view(tree)
    bt25 = Button(tab1, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:vihod(windowKL))
    bt25.pack(side=RIGHT, padx=10,pady=5)
    bt3 = Button(tab1, text="Поиск", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:poisk(tree))
    bt3.pack(side=RIGHT, padx=10,pady=5)
    bt30 = Button(tab1, text="Добавить корзину", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:dobv(tree, ID, tree2))
    bt30.pack(side=RIGHT, padx=10,pady=5)
    ########-----КОРЗИНА-----########
    tree2 = ttk.Treeview(tab2, columns=('id_korziny', 'id_klienta', 'id_tovara', 'kolvo', 'cena'),show ='headings')
    tree2.column('id_korziny',width=145, anchor = tk.CENTER)
    tree2.column('id_klienta',width=200, anchor = tk.CENTER)
    tree2.column('id_tovara',width=200, anchor = tk.CENTER)
    tree2.column('kolvo',width=200, anchor = tk.CENTER)
    tree2.column('cena',width=200, anchor = tk.CENTER)
    #
    tree2.heading('id_korziny', text='ID')
    tree2.heading('id_klienta', text='Клиент')
    tree2.heading('id_tovara', text='Товар')
    tree2.heading('kolvo', text='Количество')
    tree2.heading('cena', text='Цена')
    tree2.pack()
    view2(tree2, h)
    bt3 = Button(tab2, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:vihod(windowKL))
    bt3.pack(side=RIGHT, padx=5,pady=5)
    bt3 = Button(tab2, text="Удаление", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:ud(tree2, tree, h))
    bt3.pack(side=RIGHT, padx=5,pady=5)
    bt3 = Button(tab2, text="Изменить количество", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:izm(tree2, tree, h))
    bt3.pack(side=RIGHT, padx=5,pady=5)
    bt3 = Button(tab2, text="Оформить заказ", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:oform(tree2, h, tree3))
    bt3.pack(side=RIGHT, padx=5,pady=5)
    bt3 = Button(tab2, text="Цена", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:pod(h))
    bt3.pack(side=RIGHT, padx=5,pady=5)
    ########-----ЗАКАЗЫ-----########
    tree3 = ttk.Treeview(tab3, columns=('id_zakaza', 'id_klienta', 'id_oplati', 'data_zakaza', 'gotovnost'),show ='headings')
    tree3.column('id_zakaza',width=186, anchor = tk.CENTER)
    tree3.column('id_klienta',width=186, anchor = tk.CENTER)
    tree3.column('id_oplati',width=186, anchor = tk.CENTER)
    tree3.column('data_zakaza',width=186, anchor = tk.CENTER)
    tree3.column('gotovnost',width=186, anchor = tk.CENTER)
    #
    tree3.heading('id_zakaza', text='ID')
    tree3.heading('id_klienta', text='Клиент')
    tree3.heading('id_oplati', text='Способ оплаты')
    tree3.heading('data_zakaza', text='Дата оформления')
    tree3.heading('gotovnost', text='Стадия')
    tree3.pack()
    view3(tree3, h)
    bt3 = Button(tab3, text="Выход", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:vihod(windowKL))
    bt3.pack(side=RIGHT, padx=10,pady=5)
    bt3 = Button(tab3, text="Обновить", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:view3(tree3, h))
    bt3.pack(side=RIGHT, padx=10,pady=5)
    bt3 = Button(tab3, text="Подробнее", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:podr(tree3))
    bt3.pack(side=RIGHT, padx=10,pady=5)
    tab_control.pack(expand=1, fill='both')  
    windowKL.mainloop()