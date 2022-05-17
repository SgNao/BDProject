from flask import *
from flask_login import *
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
        head, *tail = values
        data.append([head, tail])
    return data

# genero stringhe per sql
dataset = "songdb.csv"
data = load_data(dataset)

#popolo db
engine = create_engine('sqlite:///database.db', echo = True)
conn = engine.connect()
for c in data:
    match c[0]:
        case "Utenti":
                ins = "INSERT INTO Utenti VALUES (?,?,?,?,?,?,?)"
                head, *tail = c[1]
                # None per avere un Integer con autoincremento
                # Mettere gli autoincrement per primi per poter estrarre i None
                if (c[1])[0] == "None":
                    conn.execute(ins, [None]+tail)
                # se non inseriamo None in autoincrement per un qualche motivo, sbloccare ramo else
                #else:
                    #conn.execute(ins, c[1])
        case _:
            print("Something went wrong")
        #Inserire tutti gli altri casi e modificare il numero di ?, oltre che execute statement se c'è None
"""
        case "Artisti":
                ins = "INSERT INTO Artisti VALUES (?,?,?,?,?,?,?)"
                #conn.execute(ins, tail)
        case "Playlist":
                ins = "INSERT INTO Playlist VALUES (?,?,?,?,?,?,?)"
                #conn.execute(ins, tail)
        case "Canzoni":
                ins = "INSERT INTO Canzoni VALUES (?,?,?,?,?,?,?)"
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