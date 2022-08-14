import random
from sqlalchemy import *
import sys
from werkzeug.security import generate_password_hash

# da riempire con dati corretti per far partire con Postgres

# Manca per ora la parte di creazione del database: lasciamo il file sql presente su drive per comodità o provo a
# scrivere qui quel file?


def load_data(data_file):
    # legge le righe e inserisce le in una lista
    with open(data_file) as f:
        raw_lines = [line.strip() for line in f]
    # per ogni entry della lista (= riga csv), separa head (tabella) da tail (valori da inserire)
    raw_data = []
    for line in raw_lines[1:]:
        raw_values = line.split(",")
        raw_data.append(raw_values)
    return raw_data


def change_characters(word):
    word = [w.replace(';', ',') for w in word]
    word = [w.replace(':', "'") for w in word]
    s = "".join(word)
    return s


def insert_data(data, connection):
    if sys.version_info[0] >= 3 or sys.version_info[1] >= 10:
        for c in data:
            head, *tail = c
            match head:
                case "Utenti":
                    ins = "INSERT INTO unive_music.utenti (email, nome, cognome, nickname, bio, data_nascita, " \
                          "password, ruolo, premium) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                    tail[1] = change_characters(tail[1])
                    tail[2] = change_characters(tail[2])
                    tail[3] = change_characters(tail[3])
                    tail[4] = change_characters(tail[4])
                    tail[6] = generate_password_hash(tail[6])
                    if tail[4] == "void":
                        tail[4] = ""
                    connection.execute(ins, tail)
                case "Artisti":
                    ins = "INSERT INTO unive_music.artisti (id_utente, debutto) VALUES (%s,%s)"
                    connection.execute(ins, tail)
                case "Playlist":
                    ins = "INSERT INTO unive_music.playlist (id_utente, nome, descrizione, n_canzoni) VALUES (%s,%s," \
                          "%s,%s) "
                    tail[1] = change_characters(tail[1])
                    tail[2] = change_characters(tail[2])
                    if tail[2] == "void":
                        tail[2] = ""
                    connection.execute(ins, tail)
                case "Canzoni":
                    ins = "INSERT INTO unive_music.canzoni (titolo, rilascio, durata, colore, id_artista) VALUES (%s," \
                          "%s,%s,%s,%s) "
                    tail[0] = change_characters(tail[0])
                    connection.execute(ins, tail)
                case "Album":
                    ins = "INSERT INTO unive_music.album (titolo, rilascio, colore, n_canzoni, id_artista) VALUES (" \
                          "%s,%s,%s,%s,%s) "
                    tail[0] = change_characters(tail[0])
                    connection.execute(ins, tail)
                case "Statistiche":
                    ins = "INSERT INTO unive_music.statistiche (_13_19, _20_29, _30_39, _40_49, _50_65, _65piu," \
                          "n_riproduzioni_totali, n_riproduzioni_settimanali) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) "
                    tail.append(random.randint(1, 1000001))
                    tail.append(random.randint(1, 1000001))
                    connection.execute(ins, tail)
                case "Tag":
                    ins = "INSERT INTO unive_music.tag (tag) VALUES (%s)"
                    tail[0] = change_characters(tail[0])
                    connection.execute(ins, tail)
                case "Raccolte":
                    ins = "INSERT INTO unive_music.raccolte (id_playlist, id_canzone) VALUES (%s,%s)"
                    connection.execute(ins, tail)
                case "Contenuto":
                    ins = "INSERT INTO unive_music.contenuto (id_album, id_canzone) VALUES (%s,%s)"
                    connection.execute(ins, tail)
                case "AttributoCanzone":
                    ins = "INSERT INTO unive_music.attributo_canzone (id_tag, id_canzone) VALUES (%s,%s)"
                    tail[0] = change_characters(tail[0])
                    connection.execute(ins, tail)
                case "AttributoAlbum":
                    ins = "INSERT INTO unive_music.attributo_album (id_tag, id_album) VALUES (%s,%s)"
                    tail[0] = change_characters(tail[0])
                    connection.execute(ins, tail)
                case "StatCanzoni":
                    ins = "INSERT INTO unive_music.statistiche_canzoni (id_statistica, id_canzone) VALUES (%s,%s)"
                    connection.execute(ins, tail)
                case _:
                    print("Something went wrong")
    else:
        for c in data:
            head, *tail = c
            if head == "Utenti":
                ins = "INSERT INTO unive_music.utenti (email, nome, cognome, nickname, bio, data_nascita, password, " \
                      "ruolo, premium) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,5s) "
                tail[1] = change_characters(tail[1])
                tail[2] = change_characters(tail[2])
                tail[3] = change_characters(tail[3])
                tail[4] = change_characters(tail[4])
                tail[6] = generate_password_hash(tail[6])
                if tail[4] == "void":
                    tail[4] = ""
                connection.execute(ins, tail)
            elif head == "Artisti":
                ins = "INSERT INTO unive_music.artisti (id_utente, debutto) VALUES (%s,%s)"
                connection.execute(ins, tail)
            elif head == "Playlist":
                ins = "INSERT INTO unive_music.playlist (id_utente, nome, descrizione, n_canzoni) VALUES (%s,%s,%s, %s)"
                tail[1] = change_characters(tail[1])
                tail[2] = change_characters(tail[2])
                if tail[2] == "void":
                    tail[2] = ""
                connection.execute(ins, tail)
            elif head == "Canzoni":
                ins = "INSERT INTO unive_music.canzoni (titolo, rilascio, durata, colore, id_artista) VALUES (%s,%s," \
                      "%s,%s,%s) "
                tail[0] = change_characters(tail[0])
                connection.execute(ins, tail)
            elif head == "Album":
                ins = "INSERT INTO unive_music.album (titolo, rilascio, colore, n_canzoni, id_artista) VALUES (%s,%s," \
                      "%s,%s,%s) "
                tail[0] = change_characters(tail[0])
                connection.execute(ins, tail)
            elif head == "Statistiche":
                ins = "INSERT INTO unive_music.statistiche (_13_19, _20_29, _30_39, _40_49, _50_65, _65piu, " \
                      "n_riproduzioni_totali, n_riproduzioni_settimanali) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) "
                tail.append(random.randint(1, 1000001))
                tail.append(random.randint(1, 1000001))
                connection.execute(ins, tail)
            elif head == "Tag":
                ins = "INSERT INTO unive_music.tag (tag) VALUES (%s)"
                tail[0] = change_characters(tail[0])
                connection.execute(ins, tail)
            elif head == "Raccolte":
                ins = "INSERT INTO unive_music.raccolte (id_playlist, id_canzone) VALUES (%s,%s)"
                connection.execute(ins, tail)
            elif head == "Contenuto":
                ins = "INSERT INTO unive_music.contenuto (id_album, id_canzone) VALUES (%s,%s)"
                connection.execute(ins, tail)
            elif head == "AttributoCanzone":
                ins = "INSERT INTO unive_music.attributo_canzone (id_tag, id_canzone) VALUES (%s,%s)"
                tail[0] = change_characters(tail[0])
                connection.execute(ins, tail)
            elif head == "AttributoAlbum":
                ins = "INSERT INTO unive_music.attributo_album (id_tag, id_album) VALUES (%s,%s)"
                tail[0] = change_characters(tail[0])
                connection.execute(ins, tail)
            elif head == "StatCanzoni":
                ins = "INSERT INTO unive_music.statistiche_canzoni (id_statistica, id_canzone) VALUES (%s,%s)"
                connection.execute(ins, tail)
            else:
                print("Something went wrong else else")


engine = create_engine('postgresql://postgres:BDProject2022@localhost:5432/BDProject')
conn = engine.connect()

csv_list = ["PopDB - Utenti.csv", "PopDB - Artisti.csv", "PopDB - Playlist.csv", "PopDB - Canzoni.csv",
            "PopDB - Album.csv", "PopDB - Statistiche.csv", "PopDB - Tag.csv", "PopDB - Raccolte.csv",
            "PopDB - Contenuto.csv", "PopDB - AttributoCanzone.csv", "PopDB - AttributoAlbum.csv",
            "PopDB - StatCanzoni.csv"]

for csvFile in csv_list:
    csv_data = load_data("csvFiles/" + csvFile)
    insert_data(csv_data, conn)

conn.close()
