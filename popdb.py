from flask import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered
from sqlalchemy import *
import sys
from werkzeug.security import generate_password_hash

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

def cambiaVirgola(word):
    for letter in word:
        if letter == ";":
            word = word.replace(letter,",")
    return word

def cambiaApostrofo(word):
    for letter in word:
        if letter == ":":
            word = word.replace(letter,"'")
    return word

def insertData(data, connection):
        if(sys.version_info[0]>=3 or sys.version_info[1]>=10):
                for c in data:
                        head, *tail = c
                        match head:
                                case "Utenti":
                                        ins = "INSERT INTO Utenti VALUES (?,?,?,?,?,?,?,?,?)"
                                        # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                        tail[4] = generate_password_hash(tail[4])
                                        tail[5] = cambiaVirgola(tail[5])
                                        if (tail[5] == "void"):
                                                tail[5] = ""
                                        head2, *tail2 = tail
                                        if head2 == "None":
                                                connection.execute(ins, [None]+tail2)
                                        else:
                                                connection.execute(ins, tail)
                                case "Artisti":
                                        ins = "INSERT INTO Artisti VALUES (?,?)"
                                        connection.execute(ins, tail)
                                case "Playlist":
                                        ins = "INSERT INTO Playlist VALUES (?,?,?,?,?)"
                                        # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                        head2, *tail2 = tail
                                        if head2 == "None":
                                                connection.execute(ins, [None]+tail2)
                                        else:
                                                connection.execute(ins, tail)
                                case "Canzoni":
                                        ins = "INSERT INTO Canzoni VALUES (?,?,?,?,?,?,?)"
                                        # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                        tail[1] = cambiaApostrofo(tail[1])
                                        tail[1] = cambiaVirgola(tail[1])
                                        head2, *tail2 = tail
                                        if head2 == "None":
                                                connection.execute(ins, [None]+tail2)
                                        else:
                                                connection.execute(ins, tail)
                                case "Album":
                                        ins = "INSERT INTO Album VALUES (?,?,?,?,?,?,?)"
                                        # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                        head2, *tail2 = tail
                                        if head2 == "None":
                                                connection.execute(ins, [None]+tail2)
                                        else:
                                                connection.execute(ins, tail)
                                case "Statistiche":
                                        ins = "INSERT INTO Statistiche VALUES (?,?,?,?,?,?,?,?,?)"
                                        # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                        head2, *tail2 = tail
                                        if head2 == "None":
                                                connection.execute(ins, [None]+tail2)
                                        else:
                                                connection.execute(ins, tail)
                                case "Tag":
                                        ins = "INSERT INTO Tag VALUES (?)"
                                        connection.execute(ins, tail)
                                case "Raccolte":
                                        ins = "INSERT INTO Raccolte VALUES (?,?)"
                                        connection.execute(ins, tail)
                                case "Contenuto":
                                        ins = "INSERT INTO Contenuto VALUES (?,?)"
                                        connection.execute(ins, tail)
                                case "AttributoCanzone":
                                        ins = "INSERT INTO AttributoCanzone VALUES (?,?)"
                                        connection.execute(ins, tail)
                                case "AttributoAlbum":
                                        ins = "INSERT INTO AttributoAlbum VALUES (?,?)"
                                        connection.execute(ins, tail)
                                case "AttributoPlaylist":
                                        ins = "INSERT INTO AttributoPlaylist VALUES (?,?)"
                                        connection.execute(ins, tail)
                                case "StatCanzoni":
                                        ins = "INSERT INTO StatCanzoni VALUES (?,?)"
                                        connection.execute(ins, tail)
                                case _:
                                        print("Something went wrong")
        else:
                for c in data:
                        head, *tail = c
                        if(head == "Utenti"):
                                ins = "INSERT INTO Utenti VALUES (?,?,?,?,?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                tail[4] = generate_password_hash(tail[4])
                                tail[5] = cambiaVirgola(tail[5])
                                if (tail[5] == "void"):
                                        tail[5] = ""
                                head2, *tail2 = tail
                                if head2 == "None":
                                        connection.execute(ins, [None]+tail2)
                                else:
                                        connection.execute(ins, tail)
                        elif(head == "Artisti"):
                                ins = "INSERT INTO Artisti VALUES (?,?)"
                                connection.execute(ins, tail)
                        elif(head == "Playlist"):
                                ins = "INSERT INTO Playlist VALUES (?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                head2, *tail2 = tail
                                if head2 == "None":
                                        connection.execute(ins, [None]+tail2)
                                else:
                                        connection.execute(ins, tail)
                        elif(head == "Canzoni"):
                                ins = "INSERT INTO Canzoni VALUES (?,?,?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                tail[1] = cambiaApostrofo(tail[1])
                                tail[1] = cambiaVirgola(tail[1])
                                head2, *tail2 = tail
                                if head2 == "None":
                                        connection.execute(ins, [None]+tail2)
                                else:
                                        connection.execute(ins, tail)
                        elif(head == "Album"):
                                ins = "INSERT INTO Album VALUES (?,?,?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                head2, *tail2 = tail
                                if head2 == "None":
                                        connection.execute(ins, [None]+tail2)
                                else:
                                        connection.execute(ins, tail)
                        elif(head == "Statistiche"):
                                ins = "INSERT INTO Statistiche VALUES (?,?,?,?,?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                head2, *tail2 = tail
                                if head2 == "None":
                                        connection.execute(ins, [None]+tail2)
                                else:
                                        connection.execute(ins, tail)
                        elif(head == "Tag"):
                                ins = "INSERT INTO Tag VALUES (?)"
                                connection.execute(ins, tail)
                        elif(head == "Raccolte"):
                                ins = "INSERT INTO Raccolte VALUES (?,?)"
                                connection.execute(ins, tail)
                        elif(head == "Contenuto"):
                                ins = "INSERT INTO Contenuto VALUES (?,?)"
                                connection.execute(ins, tail)
                        elif(head == "AttributoCanzone"):
                                ins = "INSERT INTO AttributoCanzone VALUES (?,?)"
                                connection.execute(ins, tail)
                        elif(head == "AttributoAlbum"):
                                ins = "INSERT INTO AttributoAlbum VALUES (?,?)"
                                connection.execute(ins, tail)
                        elif(head == "AttributoPlaylist"):
                                ins = "INSERT INTO AttributoPlaylist VALUES (?,?)"
                                connection.execute(ins, tail)
                        elif(head == "StatCanzoni"):
                                ins = "INSERT INTO StatCanzoni VALUES (?,?)"
                                connection.execute(ins, tail)
                        else:
                                print("Something went wrong else else")

#popolo db
engine = create_engine('sqlite:///database.db', echo = True)
conn = engine.connect()

'''
csvList = ["PopDB - Utenti.csv", "PopDB - Artisti.csv", "PopDB - Playlist.csv", "PopDB - Canzoni.csv", "PopDB - Album.csv", "PopDB - Statistiche.csv", "PopDB - Tag.csv"
                "PopDB - Raccolte.csv", "PopDB - Contenuto.csv", "PopDB - AttributoCanzone.csv","PopDB - AttributoAlbum.csv","PopDB - AttributoPlaylist.csv",
                "PopDB - StatCanzoni.csv"]

for csvFile in csvList:
        data = load_data(csvFile)
        print(data)
        insertData(data)
        #ricordarsi di modificare parte di insert basata su python vecchio
'''
# genero stringhe per sql
dataset = "songdb.csv"
data = load_data(dataset)
print(data)
insertData(data, conn)