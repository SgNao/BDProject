from flask import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered
from sqlalchemy import *

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
        for line in data:
                n = line.count("99999999")
                for i in range(n):
                        line.remove("99999999")
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
        match head:
                case "Utenti":
                        ins = "INSERT INTO Utenti VALUES (?,?,?,?,?,?,?)"
                        head2, *tail2 = tail
                        print(tail2)
                # None per avere un Integer con autoincremento
                # Mettere gli autoincrement per primi per poter estrarre i None
                        if head2 == "None":
                                conn.execute(ins, [None]+tail2)

                # se non inseriamo None in autoincrement per un qualche motivo, sbloccare ramo else
                #else:
                    #conn.execute(ins, c[1])
                case "Artisti":
                        ins = "INSERT INTO Artisti VALUES (?,?,?)"
                        conn.execute(ins, tail)
                case "Canzoni":
                        ins = "INSERT INTO Canzoni VALUES (?,?,?,?,?,?,?,?,?)"
                        head2, *tail2 = tail
                # None per avere un Integer con autoincremento
                # Mettere gli autoincrement per primi per poter estrarre i None
                        if head2 == "None":
                                conn.execute(ins, [None]+tail2)
                case _:
                        print("Something went wrong")
        #Inserire tutti gli altri casi e modificare il numero di ?, oltre che execute statement se c'è None
"""
        
        case "Playlist":
                ins = "INSERT INTO Playlist VALUES (?,?,?,?,?,?,?)"
                #conn.execute(ins, tail)
        
        case "Tag":
                ins = "INSERT INTO Tag VALUES (?,?,?,?,?,?,?)"
                #conn.execute(ins, tail)
        case "Raccolte":
                ins = "INSERT INTO Raccolte VALUES (?,?,?,?,?,?,?)"
                #conn.execute(ins, tail)
        case "AttributoCanzone":
                ins = "INSERT INTO AttributoCanzone VALUES (?,?,?,?,?,?,?)"
                #conn.execute(ins, tail)
        case "AttributoAlbum":
                ins = "INSERT INTO AttributoAlbum VALUES (?,?,?,?,?,?,?)"
                #conn.execute(ins, tail)
        case "AttributoPlaylist":
                ins = "INSERT INTO AttributoPlaylist VALUES (?,?,?,?,?,?,?)"
                #conn.execute(ins, tail)
"""

user_list = conn.execute("SELECT * FROM Utenti")
for u in user_list:
    print(u)