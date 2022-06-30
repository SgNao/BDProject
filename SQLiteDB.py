from email.policy import default
from flask import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered
from sqlalchemy import *
import sys
from werkzeug.security import generate_password_hash

engine = create_engine('sqlite:///database.db', echo = True)
metadata = MetaData()

users = Table('utenti', metadata, 
        Column('id_utente', Integer, nullable=False, autoincrement=True),
        Column('email', String, nullable=False),
        Column('nome', String, nullable=False), 
        Column('cognome', String, nullable=False),
        Column('nickname', String, nullable=True, unique=True),
        Column('bio', String, nullable=True),
        Column('data_nascita', Date, nullable=False),
        Column('password', String, nullable=False),
        Column('ruolo', Integer, nullable=False),
        CheckConstraint('ruolo>0 AND ruolo<4', name='check_ruolo'),
        UniqueConstraint('email', name='key_email'),
        UniqueConstraint('nickname', name='key_nickname'),
        PrimaryKeyConstraint('id_utente', name='pk_id_utente')
        )

artist = Table('artisti', metadata,
        Column('id_utente', Integer, ForeignKey("utenti.id_utente", onupdate="CASCADE", ondelete="CASCADE", name='fk_utenti'), nullable=False),
        Column('debutto', Date, nullable=True), # Data prima canzone
        PrimaryKeyConstraint('id_utente', name='pk_id_artista')
        )

playlist = Table('playlist', metadata,
        Column('id_playlist', Integer, nullable=False, autoincrement=True),
        Column('id_utente', Integer, ForeignKey("utenti.id_utente", onupdate="CASCADE", ondelete="CASCADE", name='fk_utenti'), nullable=False),
        Column('nome', String, nullable=False),
        Column('descrizione', String, nullable=True),
        Column('n_canzoni', Integer, nullable=False, default=0),
        PrimaryKeyConstraint('id_playlist', name='pk_playlist'),
        CheckConstraint('n_canzoni>=0', name='check_n_canzoni')
        )

canzoni = Table('canzoni', metadata,
        Column('id_canzone', Integer, nullable=False, autoincrement=True),
        Column('titolo', String, nullable=False),
        Column('rilascio', Date, nullable=False),
        Column('durata', Integer, nullable=False),
        Column('colore', String, nullable=False),
        Column('id_artista', Integer, ForeignKey('artisti.id_utente', onupdate='CASCADE', ondelete='CASCADE', name='fk_artista'), nullable=False),
        UniqueConstraint('titolo', 'rilascio', 'id_artista', name='key_canzone'),
        PrimaryKeyConstraint('id_canzone', name='pk_id_canzone')
        )

album = Table('album', metadata,
        Column('id_album', Integer, nullable=False, autoincrement=True),
        Column('titolo', String, nullable=False),
        Column('rilascio', Date, nullable=False),
        Column('colore', String, nullable=False),
        Column('n_canzoni', Integer, nullable=False, default=0),
        Column('id_artista', Integer, ForeignKey('artisti.id_utente', onupdate='CASCADE', ondelete='CASCADE', name='fk_artista'), nullable=False),
        UniqueConstraint('titolo', 'rilascio', 'id_artista', name='key_album'),
        PrimaryKeyConstraint('id_album', name='pk_id_album'),
        CheckConstraint('n_canzoni>=0', name='check_n_canzoni_album')
        )

Statistiche = Table('statistiche', metadata,
        Column('id_statistica', Integer, nullable=False, autoincrement = True),
        Column('_13_19', Integer, nullable=False, default=0),
        Column('_20_29', Integer, nullable=False, default=0),
        Column('_30_39', Integer, nullable=False, default=0),
        Column('_40_49', Integer, nullable=False, default=0),
        Column('_50_65', Integer, nullable=False, default=0),
        Column('_65piu', Integer, nullable=False, default=0),
        Column('n_riproduzioni_totali', Integer, nullable=False),
        Column('n_riproduzioni_settimanali', Integer, nullable=False),
        PrimaryKeyConstraint('id_statistica', name='pk_id_statistica')
        )

tag = Table('tag', metadata,
        Column('tag', String, primary_key=True, nullable=False),
        )

raccolte = Table('raccolte', metadata,
        Column('id_playlist', Integer, ForeignKey('playlist.id_playlist', onupdate='CASCADE', ondelete='CASCADE', name='fk_playlist'), nullable=False),
        Column('id_canzone', Integer, ForeignKey('canzoni.id_canzone', onupdate='CASCADE', ondelete='CASCADE', name='fk_canzone'), nullable=False),
        PrimaryKeyConstraint('id_playlist', 'id_canzone', name='pk_raccolte')
        )

contenuto = Table('contenuto', metadata,
        Column('id_album', Integer, ForeignKey('album.id_album', onupdate='CASCADE', ondelete='CASCADE', name='fk_album'), nullable=False),
        Column('id_canzone', Integer, ForeignKey('canzoni.id_canzone', onupdate='CASCADE', ondelete='CASCADE', name='fk_canzone'), nullable=False),
        PrimaryKeyConstraint('id_album', 'id_canzone', name='pk_contenuto')
        )

attCanzone = Table('attributo_canzone', metadata,
        Column('id_tag', String, ForeignKey('tag.tag', onupdate='CASCADE', ondelete='CASCADE', name='fk_tag'), nullable=False),
        Column('id_canzone', Integer, ForeignKey('canzoni.id_canzone', onupdate='CASCADE', ondelete='CASCADE', name='fk_canzone'), nullable=False),
        PrimaryKeyConstraint('id_tag', 'id_canzone', name='pk_attributo_canzone')
        )

attAlbum = Table('attributo_album', metadata,
        Column('id_tag', String, ForeignKey('tag.tag', onupdate='CASCADE', ondelete='CASCADE', name='fk_tag'), nullable=False),
        Column('id_album', Integer, ForeignKey('album.id_album', onupdate='CASCADE', ondelete='CASCADE', name='fk_album'), nullable=False),
        PrimaryKeyConstraint('id_tag', 'id_album', name='pk_attributo_album')
        )

AttPlaylist = Table('attributo_playlist', metadata,
        Column('id_tag', String, ForeignKey('tag.tag', onupdate='CASCADE', ondelete='CASCADE', name='fk_tag'), nullable=False),
        Column('id_playlist', Integer, ForeignKey('playlist.id_playlist', onupdate='CASCADE', ondelete='CASCADE', name='fk_playlist'), nullable=False),
        PrimaryKeyConstraint('id_tag', 'id_playlist', name='pk_attributo_playlist')
        )

StatCanzoni = Table('statistiche_canzoni', metadata,
        Column('id_statistica', Integer, ForeignKey('statistiche.id_statistica', onupdate='CASCADE', ondelete='CASCADE', name='fk_statistica'), nullable=False),
        Column('id_canzone', Integer, ForeignKey('canzoni.id_canzone', onupdate='CASCADE', ondelete='CASCADE', name='fk_canzone'), nullable=False),
        PrimaryKeyConstraint('id_statistica', 'id_canzone', name='pk_statistiche_canzoni')
        )

metadata.create_all(engine)

# funzione per estrarre da file csv
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

def insertData(data, connection):
        if(sys.version_info[0]>=3 or sys.version_info[1]>=10):
                for c in data:
                        head, *tail = c
                        match head:
                                case "Utenti":
                                        ins = "INSERT INTO utenti VALUES (?,?,?,?,?,?,?,?,?)"
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
                                                connection.execute(ins, [None]+tail2)
                                        else:
                                                connection.execute(ins, tail)
                                case "Artisti":
                                        ins = "INSERT INTO artisti VALUES (?,?)"
                                        connection.execute(ins, tail)
                                case "Playlist":
                                        ins = "INSERT INTO playlist VALUES (?,?,?,?,?)"
                                        # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                        tail[2] = cambiaCaratteri(tail[2])
                                        tail[3] = cambiaCaratteri(tail[3])
                                        if(tail[3] == "void"):
                                            tail[3] = ""
                                        head2, *tail2 = tail
                                        if head2 == "None":
                                                connection.execute(ins, [None]+tail2)
                                        else:
                                                connection.execute(ins, tail)
                                case "Canzoni":
                                        ins = "INSERT INTO canzoni VALUES (?,?,?,?,?,?)"
                                        # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                        tail[1] = cambiaCaratteri(tail[1])
                                        head2, *tail2 = tail
                                        if head2 == "None":
                                                connection.execute(ins, [None]+tail2)
                                        else:
                                                connection.execute(ins, tail)
                                case "Album":
                                        ins = "INSERT INTO album VALUES (?,?,?,?,?,?)"
                                        # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                        tail[1] = cambiaCaratteri(tail[1])
                                        head2, *tail2 = tail
                                        if head2 == "None":
                                                connection.execute(ins, [None]+tail2)
                                        else:
                                                connection.execute(ins, tail)
                                case "Statistiche":
                                        ins = "INSERT INTO statistiche VALUES (?,?,?,?,?,?,?,?,?)"
                                        # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                        head2, *tail2 = tail
                                        if head2 == "None":
                                                connection.execute(ins, [None]+tail2)
                                        else:
                                                connection.execute(ins, tail)
                                case "Tag":
                                        ins = "INSERT INTO tag VALUES (?)"
                                        tail[0] = cambiaCaratteri(tail[0])
                                        connection.execute(ins, tail)
                                case "Raccolte":
                                        ins = "INSERT INTO raccolte VALUES (?,?)"
                                        connection.execute(ins, tail)
                                case "Contenuto":
                                        ins = "INSERT INTO contenuto VALUES (?,?)"
                                        connection.execute(ins, tail)
                                case "AttributoCanzone":
                                        ins = "INSERT INTO attributo_canzone VALUES (?,?)"
                                        tail[0] = cambiaCaratteri(tail[0])
                                        connection.execute(ins, tail)
                                case "AttributoAlbum":
                                        ins = "INSERT INTO attributo_album VALUES (?,?)"
                                        tail[0] = cambiaCaratteri(tail[0])
                                        connection.execute(ins, tail)
                                case "AttributoPlaylist":
                                        ins = "INSERT INTO attributo_playlist VALUES (?,?)"
                                        tail[0] = cambiaCaratteri(tail[0])
                                        connection.execute(ins, tail)
                                case "StatCanzoni":
                                        ins = "INSERT INTO statistiche_canzoni VALUES (?,?)"
                                        connection.execute(ins, tail)
                                case _:
                                        print("Something went wrong")
        else:
                for c in data:
                        head, *tail = c
                        if(head == "Utenti"):
                                ins = "INSERT INTO utenti VALUES (?,?,?,?,?,?,?,?,?)"
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
                                        connection.execute(ins, [None]+tail2)
                                else:
                                        connection.execute(ins, tail)
                        elif(head == "Artisti"):
                                ins = "INSERT INTO artisti VALUES (?,?)"
                                connection.execute(ins, tail)
                        elif(head == "Playlist"):
                                ins = "INSERT INTO playlist VALUES (?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                if(tail[3] == "void"):
                                    tail[3] = ""
                                head2, *tail2 = tail
                                if head2 == "None":
                                        connection.execute(ins, [None]+tail2)
                                else:
                                        connection.execute(ins, tail)
                        elif(head == "Canzoni"):
                                ins = "INSERT INTO canzoni VALUES (?,?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                tail[1] = cambiaCaratteri(tail[1])
                                head2, *tail2 = tail
                                if head2 == "None":
                                        connection.execute(ins, [None]+tail2)
                                else:
                                        connection.execute(ins, tail)
                        elif(head == "Album"):
                                ins = "INSERT INTO album VALUES (?,?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                tail[1] = cambiaCaratteri(tail[1])
                                head2, *tail2 = tail
                                if head2 == "None":
                                        connection.execute(ins, [None]+tail2)
                                else:
                                        connection.execute(ins, tail)
                        elif(head == "Statistiche"):
                                ins = "INSERT INTO statistiche VALUES (?,?,?,?,?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                head2, *tail2 = tail
                                if head2 == "None":
                                        connection.execute(ins, [None]+tail2)
                                else:
                                        connection.execute(ins, tail)
                        elif(head == "Tag"):
                                ins = "INSERT INTO tag VALUES (?)"
                                tail[0] = cambiaCaratteri(tail[0])
                                connection.execute(ins, tail)
                        elif(head == "Raccolte"):
                                ins = "INSERT INTO raccolte VALUES (?,?)"
                                connection.execute(ins, tail)
                        elif(head == "Contenuto"):
                                ins = "INSERT INTO contenuto VALUES (?,?)"
                                connection.execute(ins, tail)
                        elif(head == "AttributoCanzone"):
                                ins = "INSERT INTO attributo_canzone VALUES (?,?)"
                                tail[0] = cambiaCaratteri(tail[0])
                                connection.execute(ins, tail)
                        elif(head == "AttributoAlbum"):
                                ins = "INSERT INTO attributo_album VALUES (?,?)"
                                tail[0] = cambiaCaratteri(tail[0])
                                connection.execute(ins, tail)
                        elif(head == "AttributoPlaylist"):
                                ins = "INSERT INTO attributo_playlist VALUES (?,?)"
                                tail[0] = cambiaCaratteri(tail[0])
                                connection.execute(ins, tail)
                        elif(head == "StatCanzoni"):
                                ins = "INSERT INTO statistiche_canzoni VALUES (?,?)"
                                connection.execute(ins, tail)
                        else:
                                print("Something went wrong else else")

#popolo db
conn = engine.connect()

csvList = ["PopDB - Utenti.csv", "PopDB - Artisti.csv", "PopDB - Playlist.csv", "PopDB - Canzoni.csv", "PopDB - Album.csv", "PopDB - Statistiche.csv", "PopDB - Tag.csv",
                "PopDB - Raccolte.csv", "PopDB - Contenuto.csv", "PopDB - AttributoCanzone.csv","PopDB - AttributoAlbum.csv","PopDB - AttributoPlaylist.csv",
                "PopDB - StatCanzoni.csv"]


for csvFile in csvList:
        data = load_data("csvFiles/" + csvFile)
        insertData(data, conn)

'''
csvList = ["PopDB - Utenti.csv", "PopDB - Artisti.csv", "PopDB - Playlist.csv", "PopDB - Canzoni.csv", "PopDB - Album.csv", "PopDB - Statistiche.csv", "PopDB - Tag.csv",
                "PopDB - Raccolte.csv", "PopDB - Contenuto.csv", "PopDB - AttributoCanzone.csv","PopDB - AttributoAlbum.csv","PopDB - AttributoPlaylist.csv",
                "PopDB - StatCanzoni.csv"]


for csvFile in csvList:
        data = load_data(csvFile)
        insertData(data, conn)
'''