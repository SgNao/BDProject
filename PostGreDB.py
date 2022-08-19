import random
from sqlalchemy import *
import sys
from werkzeug.security import generate_password_hash


def load_data(data_file):
    with open(data_file) as f:
        raw_lines = [line.strip() for line in f]
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


def insert_data(data, conn):
    if sys.version_info[0] >= 3 or sys.version_info[1] >= 10:
        for c in data:
            head, *tail = c
            match head:
                case "Utenti":
                    tail[1] = change_characters(tail[1])
                    tail[2] = change_characters(tail[2])
                    tail[3] = change_characters(tail[3])
                    tail[4] = change_characters(tail[4])
                    tail[6] = generate_password_hash(tail[6])
                    if tail[4] == "void":
                        tail[4] = ""
                    conn.execute('INSERT INTO unive_music.utenti (email, nome, cognome, nickname, bio, data_nascita, '
                                 'password, ruolo, premium) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)', tail) 
                case "Artisti":
                    conn.execute('INSERT INTO unive_music.artisti (id_utente, debutto) VALUES (%s,%s)', tail)
                case "Playlist":
                    tail[1] = change_characters(tail[1])
                    tail[2] = change_characters(tail[2])
                    if tail[2] == "void":
                        tail[2] = ""
                    conn.execute('INSERT INTO unive_music.playlist (id_utente, nome, descrizione, n_canzoni) VALUES ('
                                 '%s,%s,%s,%s)', tail) 
                case "Canzoni":
                    tail[0] = change_characters(tail[0])
                    conn.execute('INSERT INTO unive_music.canzoni (titolo, rilascio, durata, colore, id_artista) '
                                 'VALUES (%s,%s,%s,%s,%s)', tail) 
                case "Album":
                    tail[0] = change_characters(tail[0])
                    conn.execute('INSERT INTO unive_music.album (titolo, rilascio, colore, n_canzoni, id_artista) '
                                 'VALUES (%s,%s,%s,%s,%s)', tail)
                case "Statistiche":
                    n = random.randint(1, 1000001)
                    m = random.randint(1, n)
                    tail.append(n)
                    tail.append(m)
                    conn.execute('INSERT INTO unive_music.statistiche (_13_19, _20_29, _30_39, _40_49, _50_65, '
                                 '_65piu, n_riproduzioni_totali, n_riproduzioni_settimanali) VALUES (%s,%s,%s,%s,%s,'
                                 '%s,%s,%s)', tail)
                case "Tag":
                    tail[0] = change_characters(tail[0])
                    conn.execute('INSERT INTO unive_music.tag (tag) VALUES (%s)', tail)
                case "Raccolte":
                    conn.execute('INSERT INTO unive_music.raccolte (id_playlist, id_canzone) VALUES (%s,%s)', tail)
                case "Contenuto":
                    conn.execute('INSERT INTO unive_music.contenuto (id_album, id_canzone) VALUES (%s,%s)', tail)
                case "AttributoCanzone":
                    tail[0] = change_characters(tail[0])
                    conn.execute('INSERT INTO unive_music.attributo_canzone (id_tag, id_canzone) VALUES (%s,%s)', tail)
                case "AttributoAlbum":
                    tail[0] = change_characters(tail[0])
                    conn.execute('INSERT INTO unive_music.attributo_album (id_tag, id_album) VALUES (%s,%s)', tail)
                case "StatCanzoni":
                    conn.execute('INSERT INTO unive_music.statistiche_canzoni (id_statistica, id_canzone) VALUES (%s,'
                                 '%s)', tail) 
                case _:
                    print("Something went wrong")
    else:
        for c in data:
            head, *tail = c
            if head == "Utenti":
                tail[1] = change_characters(tail[1])
                tail[2] = change_characters(tail[2])
                tail[3] = change_characters(tail[3])
                tail[4] = change_characters(tail[4])
                tail[6] = generate_password_hash(tail[6])
                if tail[4] == "void":
                    tail[4] = ""
                conn.execute('INSERT INTO unive_music.utenti (email, nome, cognome, nickname, bio, data_nascita, '
                             'password, ruolo, premium) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)', tail) 
            elif head == "Artisti":
                conn.execute('INSERT INTO unive_music.artisti (id_utente, debutto) VALUES (%s,%s)', tail)
            elif head == "Playlist":
                tail[1] = change_characters(tail[1])
                tail[2] = change_characters(tail[2])
                if tail[2] == "void":
                    tail[2] = ""
                conn.execute('INSERT INTO unive_music.playlist (id_utente, nome, descrizione, n_canzoni) VALUES (%s,'
                             '%s,%s, %s)', tail) 
            elif head == "Canzoni":
                tail[0] = change_characters(tail[0])
                conn.execute('INSERT INTO unive_music.canzoni (titolo, rilascio, durata, colore, id_artista) VALUES ('
                             '%s,%s,%s,%s,%s)', tail) 
            elif head == "Album":
                tail[0] = change_characters(tail[0])
                conn.execute('INSERT INTO unive_music.album (titolo, rilascio, colore, n_canzoni, id_artista) VALUES '
                             '(%s,%s,%s,%s,%s)', tail)
            elif head == "Statistiche":
                tail.append(random.randint(1, 1000001))
                tail.append(random.randint(1, 1000001))
                conn.execute('INSERT INTO unive_music.statistiche (_13_19, _20_29, _30_39, _40_49, _50_65, _65piu, '
                             'n_riproduzioni_totali, n_riproduzioni_settimanali) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                             tail)
            elif head == "Tag":
                tail[0] = change_characters(tail[0])
                conn.execute('INSERT INTO unive_music.tag (tag) VALUES (%s)', tail)
            elif head == "Raccolte":
                conn.execute('INSERT INTO unive_music.raccolte (id_playlist, id_canzone) VALUES (%s,%s)', tail)
            elif head == "Contenuto":
                conn.execute('INSERT INTO unive_music.contenuto (id_album, id_canzone) VALUES (%s,%s)', tail)
            elif head == "AttributoCanzone":
                tail[0] = change_characters(tail[0])
                conn.execute('INSERT INTO unive_music.attributo_canzone (id_tag, id_canzone) VALUES (%s,%s)', tail)
            elif head == "AttributoAlbum":
                tail[0] = change_characters(tail[0])
                conn.execute('INSERT INTO unive_music.attributo_album (id_tag, id_album) VALUES (%s,%s)', tail)
            elif head == "StatCanzoni":
                conn.execute('INSERT INTO unive_music.statistiche_canzoni (id_statistica, id_canzone) VALUES (%s,%s)',
                             tail)
            else:
                print("Something went wrong else else")


engine = create_engine('postgresql://postgres:BDProject2022@localhost:5432/BDProject')
connection = engine.connect()

csv_list = ["PopDB - Utenti.csv", "PopDB - Artisti.csv", "PopDB - Playlist.csv", "PopDB - Canzoni.csv",
            "PopDB - Album.csv", "PopDB - Statistiche.csv", "PopDB - Tag.csv", "PopDB - Raccolte.csv",
            "PopDB - Contenuto.csv", "PopDB - AttributoCanzone.csv", "PopDB - AttributoAlbum.csv",
            "PopDB - StatCanzoni.csv"]

for csvFile in csv_list:
    csv_data = load_data("csvFiles/" + csvFile)
    insert_data(csv_data, connection)

connection.close()
