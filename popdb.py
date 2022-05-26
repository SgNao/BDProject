from flask import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered
from sqlalchemy import *
import sys

# funzione per estrarre da file csv
def load_data(data_file):
        # legge le righe e inserisce le in una lista
        raw_lines = []
        with open(data_file) as f:
                raw_lines = [line.strip() for line in f]
    
        # per ogni entry della lista (= riga csv), separa head (tabella) da tail (valori da inserire)
        data = []
        for line in raw_lines:
                values = line.split(",")
                #head, *tail = values
                data.append(values)
        
        # le colonne vuote si possono eliminare utiilizzando la stringa vuota
        for line in data:
                n = line.count("")
                for i in range(n):
                        line.remove("")
        return data

# genero stringhe per sql
dataset = "songdb.csv"
data = load_data(dataset)
print(data)

#popolo db
engine = create_engine('sqlite:///database.db', echo = True)
conn = engine.connect()
for c in data:
        head, *tail = c
        if(sys.version_info[0]<3 or sys.version_info[1]<10):
                match head:
                        case "Utenti":
                                ins = "INSERT INTO Utenti VALUES (?,?,?,?,?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                head2, *tail2 = tail
                                if head2 == "None":
                                        conn.execute(ins, [None]+tail2)
                                else:
                                        conn.execute(ins, tail)
                        case "Artisti":
                                ins = "INSERT INTO Artisti VALUES (?,?)"
                                conn.execute(ins, tail)
                        case "Playlist":
                                ins = "INSERT INTO Playlist VALUES (?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                head2, *tail2 = tail
                                if head2 == "None":
                                        conn.execute(ins, [None]+tail2)
                                else:
                                        conn.execute(ins, tail)
                        case "Canzoni":
                                ins = "INSERT INTO Canzoni VALUES (?,?,?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                head2, *tail2 = tail
                                if head2 == "None":
                                        conn.execute(ins, [None]+tail2)
                                else:
                                        conn.execute(ins, tail)
                        case "Album":
                                ins = "INSERT INTO Album VALUES (?,?,?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                head2, *tail2 = tail
                                if head2 == "None":
                                        conn.execute(ins, [None]+tail2)
                                else:
                                        conn.execute(ins, tail)
                        case "Statistiche":
                                ins = "INSERT INTO Statistiche VALUES (?,?,?,?,?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                head2, *tail2 = tail
                                if head2 == "None":
                                        conn.execute(ins, [None]+tail2)
                                else:
                                        conn.execute(ins, tail)
                        case "Tag":
                                ins = "INSERT INTO Tag VALUES (?)"
                                conn.execute(ins, tail)
                        case "Raccolte":
                                ins = "INSERT INTO Raccolte VALUES (?,?)"
                                conn.execute(ins, tail)
                        case "Contenuto":
                                ins = "INSERT INTO Contenuto VALUES (?,?)"
                                conn.execute(ins, tail)
                        case "AttributoCanzone":
                                ins = "INSERT INTO AttributoCanzone VALUES (?,?)"
                                conn.execute(ins, tail)
                        case "AttributoAlbum":
                                ins = "INSERT INTO AttributoAlbum VALUES (?,?)"
                                conn.execute(ins, tail)
                        case "AttributoPlaylist":
                                ins = "INSERT INTO AttributoPlaylist VALUES (?,?)"
                                conn.execute(ins, tail)
                        case "StatCanzoni":
                                ins = "INSERT INTO StatCanzoni VALUES (?,?)"
                                conn.execute(ins, tail)
                        case _:
                                print("Something went wrong")
        else:
                if(head == "Utenti"):
                        ins = "INSERT INTO Utenti VALUES (?,?,?,?,?,?,?,?,?)"
                        # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                        head2, *tail2 = tail
                        if head2 == "None":
                                conn.execute(ins, [None]+tail2)
                        else:
                                conn.execute(ins, tail)
                        if(head == "Artisti"):
                                ins = "INSERT INTO Artisti VALUES (?,?)"
                                conn.execute(ins, tail)
                        elif(head == "Playlist"):
                                ins = "INSERT INTO Playlist VALUES (?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                head2, *tail2 = tail
                                if head2 == "None":
                                        conn.execute(ins, [None]+tail2)
                                else:
                                        conn.execute(ins, tail)
                        elif(head == "Canzoni"):
                                ins = "INSERT INTO Canzoni VALUES (?,?,?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                head2, *tail2 = tail
                                if head2 == "None":
                                        conn.execute(ins, [None]+tail2)
                                else:
                                        conn.execute(ins, tail)
                        elif(head == "Album"):
                                ins = "INSERT INTO Album VALUES (?,?,?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                head2, *tail2 = tail
                                if head2 == "None":
                                        conn.execute(ins, [None]+tail2)
                                else:
                                        conn.execute(ins, tail)
                        elif(head == "Statistiche"):
                                ins = "INSERT INTO Statistiche VALUES (?,?,?,?,?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                head2, *tail2 = tail
                                if head2 == "None":
                                        conn.execute(ins, [None]+tail2)
                                else:
                                        conn.execute(ins, tail)
                        elif(head == "Tag"):
                                ins = "INSERT INTO Tag VALUES (?)"
                                conn.execute(ins, tail)
                        elif(head == "Raccolte"):
                                ins = "INSERT INTO Raccolte VALUES (?,?)"
                                conn.execute(ins, tail)
                        elif(head == "Raccolte"):
                                ins = "INSERT INTO Contenuto VALUES (?,?)"
                                conn.execute(ins, tail)
                        elif(head == "AttributoCanzone"):
                                ins = "INSERT INTO AttributoCanzone VALUES (?,?)"
                                conn.execute(ins, tail)
                        elif(head == "AttributoAlbum"):
                                ins = "INSERT INTO AttributoAlbum VALUES (?,?)"
                                conn.execute(ins, tail)
                        elif(head == "AttributoPlaylist"):
                                ins = "INSERT INTO AttributoPlaylist VALUES (?,?)"
                                conn.execute(ins, tail)
                        elif(head == "StatCanzoni"):
                                ins = "INSERT INTO StatCanzoni VALUES (?,?)"
                                conn.execute(ins, tail)
                        else:
                                print("Something went wrong")