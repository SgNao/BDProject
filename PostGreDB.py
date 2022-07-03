from flask import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered
from sqlalchemy import *
import psycopg2
import configdb
import sys
from werkzeug.security import generate_password_hash

# da riempire con dati corretti per far partire con Postgres

# Manca per ora la parte di creazione del database: lasciamo il file sql presente su drive per comodità o provo a scrivere qui quel file?

def load_data(data_file):
        # legge le righe e inserisce le in una lista
        raw_lines = []
        with open(data_file) as f:
                raw_lines = [line.strip() for line in f]
    
        # per ogni entry della lista (= riga csv), separa head (tabella) da tail (valori da inserire)
        data = []
        for line in raw_lines[1:]:
                values = line.split(",")
                data.append(values)
        
        # le colonne vuote si possono eliminare utiilizzando la stringa vuota
        for line in data:
                n = line.count("")
                for i in range(n):
                        line.remove("")
        return data

def cambiaCaratteri(word):
    word = [w.replace(';', ',') for w in word]
    word = [w.replace(':', "'") for w in word]
    s = "".join(word)
    return s

def cambiaVirgola(word):
    for letter in word:
        if letter == ';':
            word = word.replace(letter,',')
    return word

def cambiaApostrofo(word):
    for letter in word:
        if letter == ':':
            word = word.replace(letter,"'")
    return word

def insertData(data, cursor):
        if(sys.version_info[0]>=3 or sys.version_info[1]>=10):
                for c in data:
                        head, *tail = c
                        match head:
                                case "Utenti":
                                        ins = "INSERT INTO unive_music.utenti (id_utente, email, nome, cognome, nickname, bio, data_nascita, password, ruolo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                        # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                        tail[2] = cambiaCaratteri(tail[2])
                                        tail[3] = cambiaCaratteri(tail[3])
                                        tail[4] = cambiaCaratteri(tail[4])
                                        tail[5] = cambiaCaratteri(tail[5])
                                        tail[7] = generate_password_hash(tail[7])
                                        if (tail[5] == "void"):
                                                tail[5] = ""
                                        head2, *tail2 = tail
                                        if head2 == "None":
                                                cursor.execute(ins, [None]+tail2)
                                        else:
                                                cursor.execute(ins, tail)
                                case "Artisti":
                                        ins = "INSERT INTO unive_music.artisti (id_utente, debutto) VALUES (%s,%s)"
                                        cursor.execute(ins, tail)
                                case "Playlist":
                                        ins = "INSERT INTO unive_music.playlist (id_playlist, id_utente, nome, descrizione, n_canzoni) VALUES (%s,%s,%s,%s,%s)"
                                        # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                        tail[2] = cambiaCaratteri(tail[2])
                                        tail[3] = cambiaCaratteri(tail[3])
                                        if(tail[3] == "void"):
                                            tail[3] = ""
                                        head2, *tail2 = tail
                                        if head2 == "None":
                                                cursor.execute(ins, [None]+tail2)
                                        else:
                                                cursor.execute(ins, tail)
                                case "Canzoni":
                                        ins = "INSERT INTO unive_music.canzoni (id_canzone, titolo, rilascio, durata, colore, id_artista) VALUES (%s,%s,%s,%s,%s,%s)"
                                        # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                        tail[1] = cambiaCaratteri(tail[1])
                                        head2, *tail2 = tail
                                        if head2 == "None":
                                                cursor.execute(ins, [None]+tail2)
                                        else:
                                                cursor.execute(ins, tail)
                                case "Album":
                                        ins = "INSERT INTO unive_music.album (id_album, titolo, rilascio, colore, n_canzoni, id_artista) VALUES (%s,%s,%s,%s,%s,%s)"
                                        # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                        tail[1] = cambiaCaratteri(tail[1])
                                        head2, *tail2 = tail
                                        if head2 == "None":
                                                cursor.execute(ins, [None]+tail2)
                                        else:
                                                cursor.execute(ins, tail)
                                case "Statistiche":
                                        ins = "INSERT INTO unive_music.statistiche (id_statistica, _13_19, _20_29, _30_39, _40_49, _50_65, _65piu, n_riproduzioni_totali, n_riproduzioni_settimanali) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                        # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                        head2, *tail2 = tail
                                        if head2 == "None":
                                                cursor.execute(ins, [None]+tail2)
                                        else:
                                                cursor.execute(ins, tail)
                                case "Tag":
                                        ins = "INSERT INTO unive_music.tag (tag) VALUES (%s)"
                                        tail[0] = cambiaCaratteri(tail[0])
                                        cursor.execute(ins, tail)
                                case "Raccolte":
                                        ins = "INSERT INTO unive_music.raccolte (id_playlist, id_canzone) VALUES (%s,%s)"
                                        cursor.execute(ins, tail)
                                case "Contenuto":
                                        ins = "INSERT INTO unive_music.contenuto (id_album, id_canzone) VALUES (%s,%s)"
                                        cursor.execute(ins, tail)
                                case "AttributoCanzone":
                                        ins = "INSERT INTO unive_music.attributo_canzone (id_tag, id_canzone) VALUES (%s,%s)"
                                        tail[0] = cambiaCaratteri(tail[0])
                                        cursor.execute(ins, tail)
                                case "AttributoAlbum":
                                        ins = "INSERT INTO unive_music.attributo_album (id_tag, id_album) VALUES (%s,%s)"
                                        tail[0] = cambiaCaratteri(tail[0])
                                        cursor.execute(ins, tail)
                                case "StatCanzoni":
                                        ins = "INSERT INTO unive_music.statistiche_canzoni (id_statistica, id_canzone) VALUES (%s,%s)"
                                        cursor.execute(ins, tail)
                                case _:
                                        print("Something went wrong")
        else:
                for c in data:
                        head, *tail = c
                        if(head == "Utenti"):
                                ins = "INSERT INTO unive_music.utenti (id_utente, email, nome, cognome, nickname, bio, data_nascita, password, ruolo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                tail[2] = cambiaCaratteri(tail[2])
                                tail[3] = cambiaCaratteri(tail[3])
                                tail[4] = cambiaCaratteri(tail[4])
                                tail[5] = cambiaCaratteri(tail[5])
                                tail[7] = generate_password_hash(tail[7])
                                if (tail[5] == "void"):
                                        tail[5] = ""
                                head2, *tail2 = tail
                                if head2 == "None":
                                        cursor.execute(ins, [None]+tail2)
                                else:
                                        cursor.execute(ins, tail)
                        elif(head == "Artisti"):
                                ins = "INSERT INTO unive_music.artisti (id_utente, debutto) VALUES (%s,%s)"
                                cursor.execute(ins, tail)
                        elif(head == "Playlist"):
                                ins = "INSERT INTO unive_music.playlist (id_playlist, id_utente, nome, descrizione, n_canzoni) VALUES (%s,%s,%s,%s,%s)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                tail[2] = cambiaCaratteri(tail[2])
                                tail[3] = cambiaCaratteri(tail[3])
                                if(tail[3] == "void"):
                                    tail[3] = ""
                                head2, *tail2 = tail
                                if head2 == "None":
                                        cursor.execute(ins, [None]+tail2)
                                else:
                                        cursor.execute(ins, tail)
                        elif(head == "Canzoni"):
                                ins = "INSERT INTO unive_music.canzoni (id_canzone, titolo, rilascio, durata, colore, id_artista) VALUES (%s,%s,%s,%s,%s,%s)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                tail[1] = cambiaCaratteri(tail[1])
                                head2, *tail2 = tail
                                if head2 == "None":
                                        cursor.execute(ins, [None]+tail2)
                                else:
                                        cursor.execute(ins, tail)
                        elif(head == "Album"):
                                ins = "INSERT INTO unive_music.album (id_album, titolo, rilascio, colore, n_canzoni, id_artista) VALUES (%s,%s,%s,%s,%s,%s)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                tail[1] = cambiaCaratteri(tail[1])
                                head2, *tail2 = tail
                                if head2 == "None":
                                        cursor.execute(ins, [None]+tail2)
                                else:
                                        cursor.execute(ins, tail)
                        elif(head == "Statistiche"):
                                ins = "INSERT INTO unive_music.statistiche (id_statistica, _13_19, _20_29, _30_39, _40_49, _50_65, _65piu, n_riproduzioni_totali, n_riproduzioni_settimanali) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                head2, *tail2 = tail
                                if head2 == "None":
                                        cursor.execute(ins, [None]+tail2)
                                else:
                                        cursor.execute(ins, tail)
                        elif(head == "Tag"):
                                ins = "INSERT INTO unive_music.tag (tag) VALUES (%s)"
                                tail[0] = cambiaCaratteri(tail[0])
                                cursor.execute(ins, tail)
                        elif(head == "Raccolte"):
                                ins = "INSERT INTO unive_music.raccolte (id_playlist, id_canzone) VALUES (%s,%s)"
                                cursor.execute(ins, tail)
                        elif(head == "Contenuto"):
                                ins = "INSERT INTO unive_music.contenuto (id_album, id_canzone) VALUES (%s,%s)"
                                cursor.execute(ins, tail)
                        elif(head == "AttributoCanzone"):
                                ins = "INSERT INTO unive_music.attributo_canzone (id_tag, id_canzone) VALUES (%s,%s)"
                                tail[0] = cambiaCaratteri(tail[0])
                                cursor.execute(ins, tail)
                        elif(head == "AttributoAlbum"):
                                ins = "INSERT INTO unive_music.attributo_album (id_tag, id_album) VALUES (%s,%s)"
                                tail[0] = cambiaCaratteri(tail[0])
                                cursor.execute(ins, tail)
                        elif(head == "StatCanzoni"):
                                ins = "INSERT INTO unive_music.statistiche_canzoni (id_statistica, id_canzone) VALUES (%s,%s)"
                                cursor.execute(ins, tail)
                        else:
                                print("Something went wrong else else")

#popolo db
conn = configdb.getConnection() 

csvList = ["PopDB - Utenti.csv", "PopDB - Artisti.csv", "PopDB - Playlist.csv", "PopDB - Canzoni.csv", "PopDB - Album.csv", "PopDB - Statistiche.csv", "PopDB - Tag.csv",
                "PopDB - Raccolte.csv", "PopDB - Contenuto.csv", "PopDB - AttributoCanzone.csv","PopDB - AttributoAlbum.csv", "PopDB - StatCanzoni.csv"]

for csvFile in csvList:
        data = load_data("csvFiles/" + csvFile)
        cur = conn.cursor()
        insertData(data, cur)
        conn.commit() #fare commit su connessione
        cur.close() #usare cursore per fare le query

conn.close()