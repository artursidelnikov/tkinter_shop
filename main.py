from tkinter import * 
from tkinter import messagebox
import sqlite3
from sqlite3 import Error 

global ID

def clicked_vhod():
    conn = sqlite3.connect('magazin.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Paroly;")
    inf_paroly = cur.fetchall()
    Kluch = 0
    schet0 = 0
    ID = 0
    for infa in inf_paroly:
        if (infa[1] == txt1.get() and infa[2] == txt2.get()):
            ID = infa[0]
            cur.execute("SELECT * FROM Personal;")
            inf_Personal = cur.fetchall()
            for infa_dop in inf_Personal:
                if (infa_dop[7] == infa[0]):
                    Kluch = infa_dop[4]
            if Kluch == 0:
                Kluch = 4
    if Kluch == 0:
        messagebox.showerror("Ошибка!", "Неверный логин или пароль!") 
    # Есть ключ
    if Kluch == 1:
        window.destroy()
        import Prodavec
        Prodavec.zapusk(ID)
    if Kluch == 2:
        window.destroy()
        import Zakupshik
        Zakupshik.zapusk(ID)
    if Kluch == 3:
        window.destroy()
        import Kladovshik
        Kladovshik.zapusk(ID)
    if Kluch == 4:
        window.destroy()
        import Pokupatel
        Pokupatel.zapusk(ID)
    
def dobavlenie_polzv(a,b,c,d,e,window2):
    conn = sqlite3.connect('magazin.db')
    cur = conn.cursor()
    if (a=="" or b=="" or c=="" or d=="" or e=="" or len(c) != 11):
        messagebox.showerror("Ошибка!", "Заполните все поля.")
    else:
        while True:
            try:
                cur.execute("""INSERT INTO Paroly(login, parol) VALUES (?, ?)""", (d,e))
                cur.execute("""SELECT id_parol FROM Paroly ORDER BY id_parol DESC LIMIT 1;""")
                new=cur.fetchall()
                cur.execute("""INSERT INTO Pokupateli(imya, familiya, telefon, id_parol) VALUES (?, ?, ?, ?)""", (a,b,c, new[0][0]))
                conn.commit()
                break
            except sqlite3.IntegrityError:
                messagebox.showerror("Ошибка!", "Учетная запись с таким логином уже существует.")
                break
    window2.destroy()

def clicked_registracia():
    window2 = Tk()
    window2.title("Регистрация")
    window2.resizable(width=False, height = False)
    window2.geometry('370x250')
    lbl3 = Label(window2, text="Имя", font=("Times New Roman", 20))
    lbl3.grid(column=0, row=1)
    txt3 = Entry(window2,width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt3.grid(column=1, row=1)
    lbl4 = Label(window2, text="Фамилия", font=("Times New Roman", 20))
    lbl4.grid(column=0, row=2)
    txt4 = Entry(window2,width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt4.grid(column=1, row=2)
    lbl5 = Label(window2, text="Телефон", font=("Times New Roman", 20))
    lbl5.grid(column=0, row=3)
    txt5 = Entry(window2,width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt5.grid(column=1, row=3)
    lbl6 = Label(window2, text="Логин", font=("Times New Roman", 20))
    lbl6.grid(column=0, row=4)
    txt6 = Entry(window2,width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt6.grid(column=1, row=4)
    lbl7 = Label(window2, text="Пароль", font=("Times New Roman", 20))
    lbl7.grid(column=0, row=5)
    txt7 = Entry(window2,width=10, background="#d7d8e0", font=("Times New Roman", 20))
    txt7.grid(column=1, row=5)
    btn3 = Button(window2, text="Зарегистрироваться", background="#d7d8e0", font=("Times New Roman", 20), command=lambda:dobavlenie_polzv(txt3.get(),txt4.get(),txt5.get(),txt6.get(),txt7.get(),window2))
    btn3.grid(column=1, row=6)
    btn4 = Button(window2, text="Назад", background="#d7d8e0", font=("Times New Roman", 20), command=window2.destroy)
    btn4.grid(column=0, row=6)
    window2.mainloop()

window = Tk()
window.resizable(width=False, height = False)
window.title("Авторизация")
window.geometry('310x170')
lbl1 = Label(window, text="Логин", font=("Times New Roman", 20))
lbl1.place(x=25, y=10)
txt1 = Entry(window,width=10, background="#d7d8e0", font=("Times New Roman", 20))
txt1.place(x=140, y=10)
lbl2 = Label(window, text="Пароль", font=("Times New Roman", 20))
lbl2.place(x=25, y=50)
txt2 = Entry(window,width=10,background="#d7d8e0", font=("Times New Roman", 20), show = '*')
txt2.place(x=140, y=50)
btn1 = Button(window, text="Войти", background="#d7d8e0", font=("Times New Roman", 20), command=clicked_vhod)
btn1.place(x=200, y=100)
btn2 = Button(window, text="Регистрация", background="#d7d8e0", font=("Times New Roman", 20), command=clicked_registracia)
btn2.place(x=20, y=100)
window.mainloop()

