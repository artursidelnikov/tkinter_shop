import sqlite3
from sqlite3 import Error

conn = sqlite3.connect('magazin.db')
cur = conn.cursor()

#Таблица 1 - Пароли (Paroly)
cur.execute("""PRAGMA foreign_keys=on;""")
cur.execute("""CREATE TABLE IF NOT EXISTS Paroly(
   id_parol INTEGER PRIMARY KEY AUTOINCREMENT,
   login TEXT NOT NULL,
   parol TEXT NOT NULL);
""")
#Таблица 2 - Должности (Dolzhnosty)
cur.execute("""CREATE TABLE IF NOT EXISTS Dolzhnosty(
   id_dolzhnost INTEGER PRIMARY KEY AUTOINCREMENT,
   nazvanie TEXT NOT NULL,
   opisanie TEXT NULL);
""")
#Таблица 3 - Персонал (Pesonal)
cur.execute("""CREATE TABLE IF NOT EXISTS Personal(
   id_rabotnika INTEGER PRIMARY KEY AUTOINCREMENT,
   imya TEXT NOT NULL,
   familiya TEXT NOT NULL,
   otchestvo TEXT NULL,
   id_dolzhnost INT NOT NULL,
   telefon TEXT NOT NULL,
   adres TEXT NOT NULL,
   id_parol INT NOT NULL, 
   FOREIGN KEY (id_parol) references Paroly(id_parol),
   FOREIGN KEY (id_dolzhnost) references Dolzhnosty(id_dolzhnost));
""")
#Таблица 4 - Поставщики (Postavshiki)
cur.execute("""CREATE TABLE IF NOT EXISTS Postavshiki(
   id_postavshika INTEGER PRIMARY KEY AUTOINCREMENT,
   nazvanie TEXT NOT NULL,
   ur_adres TEXT NOT NULL,
   fiz_adres TEXT NOT NULL);
""")
#Таблица 5 - Поставки (Postavki)
cur.execute("""CREATE TABLE IF NOT EXISTS Postavki(
   id_postavki INTEGER PRIMARY KEY AUTOINCREMENT,
   id_postavshika INT NOT NULL,
   dataZAKAZA INT NOT NULL,
   FOREIGN KEY (id_postavshika) references Postavshiki(id_postavshika),
   FOREIGN KEY (id_tovara) references Tovari(id_tovara));
""")
#Таблица 6 - Клиенты (Pokupateli)
cur.execute("""CREATE TABLE IF NOT EXISTS Pokupateli(
   id_klienta INTEGER PRIMARY KEY AUTOINCREMENT,
   imya TEXT NOT NULL,
   familiya TEXT NOT NULL,
   telefon TEXT NOT NULL,
   mail TEXT NULL,
   id_parol INT NULL,
   FOREIGN KEY (id_parol) references Paroly(id_parol));
""")
#Таблица 7 - Товары (Tovari)
cur.execute("""CREATE TABLE IF NOT EXISTS Tovari(
   id_tovara INTEGER PRIMARY KEY AUTOINCREMENT,
   nazvanie TEXT NOT NULL,
   kolvo INT NOT NULL,
   sertificat TEXT NULL,
   cena INT NOT NULL,
   SrokGodnos DATE NOT NULL,
   Proizv TEXT NULL,
   id_postavki INT);
""")
#Таблица 8 - Оплата (Oplata)
cur.execute("""CREATE TABLE IF NOT EXISTS Oplata(
   id_oplati INTEGER PRIMARY KEY AUTOINCREMENT,
   bankovskie_recv TEXT NOT NULL);
""")
#Таблица 9 - Корзина (Korzina)
cur.execute("""CREATE TABLE IF NOT EXISTS Korzina(
   id_korziny INTEGER PRIMARY KEY AUTOINCREMENT,
   id_klienta INT NOT NULL,
   id_tovara INT NOT NULL,
   kolvo INT NOT NULL,
   cena INT NOT NULL,
   id_zakaza INT NULL,
   FOREIGN KEY (id_klienta) references Pokupateli(id_klienta),
   FOREIGN KEY (id_oplati) references Oplata(id_oplati),
   FOREIGN KEY (id_tovara) references Tovari(id_tovara));
""")
#Таблица 10 - Заказ (Zakaz)
cur.execute("""CREATE TABLE IF NOT EXISTS Zakaz(
   id_zakaza INTEGER PRIMARY KEY AUTOINCREMENT,
   id_rabotnika INT NOT NULL,
   id_klienta INT NOT NULL,
   id_oplati INT NOT NULL,
   data_zakaza INT NOT NULL,
   data_vidachi INT NOT NULL,
   gotovnost TEXT NOT NULL,
   FOREIGN KEY (id_rabotnika) references Personal(id_rabotnika),
   FOREIGN KEY (id_klienta) references Pokupateli(id_klienta),
   FOREIGN KEY (id_oplati) references Oplata(id_oplati),
   FOREIGN KEY (id_tovara) references Tovari(id_tovara));
""")

cur.execute("""CREATE TABLE IF NOT EXISTS Zayavki(
   id_zayavki INTEGER PRIMARY KEY AUTOINCREMENT,
   tovar TEXT NOT NULL,
   kolvo INT NOT NULL,
   SrokGodns DATE NOT NULL,
   proizv TEXT NOT NULL,
   sertificat TEXT NOT NULL,
   cena INT NOT NULL,
   id_postavshika INT NULL);
""")
conn.commit()