from flask import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered
from sqlalchemy import *
import sys
from werkzeug.security import generate_password_hash

engine = create_engine('sqlite:///database.db', echo = True)
metadata = MetaData()

users = Table('Utenti', metadata, 
        Column('IdUtenti', Integer, primary_key=True, nullable=False, autoincrement=True),
        Column('Email', String, nullable=False, unique=True),
        Column('Nome', String, nullable=False), 
        Column('Cognome', String, nullable=False),
        Column('Nickname', String(16), nullable=True, unique=True),
        Column('Bio', String(160), nullable=True),
        Column('DataNascita', Date, nullable=False), # sembra che non si possa controllare a livello di DB l'età di una persona
        Column('Password', String, nullable=False),
        Column('Ruolo', Integer, nullable=False),
        Index('idx_email', 'Email'),
        CheckConstraint('Ruolo>0 AND Ruolo<4', name='checkRuolo')
        #CheckConstraint('datetime.datetime() - DataNascita > 13', name='check13')
        )

artist = Table('Artisti', metadata,
        Column('IdUtente', Integer, ForeignKey("Utenti.IdUtenti", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True, nullable=False),
        Column('Debutto', Date, nullable=True), # Data prima canzone
        Index('idx_Utente', 'IdUtente')
        )

playlist = Table('Playlist', metadata,
        Column('IdPlaylist', Integer, primary_key=True, nullable=False, autoincrement=True),
        Column('IdUtente', Integer, ForeignKey("Utenti.IdUtenti", onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
        Column('Nome', String(64), nullable=False),
        Column('Descrizione', String(160), nullable=True),
        Column('NCanzoni', Integer, CheckConstraint('NCanzoni>=0'), nullable=False),
        Index('idx_playlist', 'IdUtente', 'Nome')
        )

canzoni = Table('Canzoni', metadata,
        Column('IdCanzone', Integer, primary_key=True, nullable=False, autoincrement=True),
        Column('Titolo', String, nullable=False),
        Column('Rilascio', Date, nullable=False),
        Column('Durata', Integer, nullable=False),
        Column('Colore', String, nullable=False),
        Column('IdArtista', Integer, ForeignKey('Artisti.IdUtente', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        UniqueConstraint('Titolo', 'Rilascio', 'IdArtista', name='songKey'),
        Index('idx_canzone_anno', 'Rilascio'),
        Index('idx_canzone_Titolo', 'Titolo')
        )

album = Table('Album', metadata,
        Column('IdAlbum', Integer, primary_key=True, nullable=False, autoincrement=True),
        Column('Titolo', String, nullable=False),
        Column('Rilascio', Date, nullable=False),
        Column('Colore', String, nullable=False),
        Column('NCanzoni', Integer, nullable=False),
        Column('IdArtista', Integer, ForeignKey('Artisti.IdUtente', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        UniqueConstraint('Titolo', 'Rilascio', 'IdArtista', name='albumKey'),
        Index('idx_album_titolo', 'Titolo'),
        Index('idx_album_anno', 'Rilascio')
        )

Statistiche = Table('Statistiche', metadata,
        Column('IdStatistica', Integer, primary_key = True, nullable=False, autoincrement = True),
        Column('13-19', Integer, nullable=False),
        Column('20-29', Integer, nullable=False),
        Column('30-39', Integer, nullable=False),
        Column('40-49', Integer, nullable=False),
        Column('50-65', Integer, nullable=False),
        Column('65+', Integer, nullable=False),
        Column('NRiproduzioniTotali', Integer, nullable=False),
        Column('NRiproduzioniSettimanali', Integer, nullable=False)
        )

tag = Table('Tag', metadata,
        Column('Tag', String, primary_key=True, nullable=False),
        )

raccolte = Table('Raccolte', metadata,
        Column('IdPlaylist', Integer, ForeignKey('Playlist.IdPlaylist', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        Column('IdCanzone', Integer, ForeignKey('Canzoni.IdCanzone', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        PrimaryKeyConstraint('IdPlaylist', 'IdCanzone', name='RaccoltePK')
        )

contenuto = Table('Contenuto', metadata,
        Column('IdAlbum', Integer, ForeignKey('Album.IdAlbum', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        Column('IdCanzone', Integer, ForeignKey('Canzoni.IdCanzone', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        PrimaryKeyConstraint('IdAlbum', 'IdCanzone', name='ConteutoPK')
        )

attCanzone = Table('AttributoCanzone', metadata,
        Column('IdTag', String, ForeignKey('Tag.Tag', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        Column('IdCanzone', Integer, ForeignKey('Canzoni.IdCanzone', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        PrimaryKeyConstraint('IdTag', 'IdCanzone', name='AttributoCanzonePK')
        )

attAlbum = Table('AttributoAlbum', metadata,
        Column('IdTag', String, ForeignKey('Tag.Tag', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        Column('IdAlbum', Integer, ForeignKey('Album.IdAlbum', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        PrimaryKeyConstraint('IdTag', 'IdAlbum', name='AttributoAlbumPK')
        )

AttPlaylist = Table('AttributoPlaylist', metadata,
        Column('IdTag', String, ForeignKey('Tag.Tag', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        Column('IdPlaylist', Integer, ForeignKey('Playlist.IdPlaylist', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        PrimaryKeyConstraint('IdTag', 'IdPlaylist', name='AttributoPlaylistPK')
        )

StatCanzoni = Table('StatCanzoni', metadata,
        Column('IdStatistica', Integer, ForeignKey('Statistiche.IdStatistica', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        Column('IdCanzone', Integer, ForeignKey('Canzoni.IdCanzone', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        PrimaryKeyConstraint('IdStatistica', 'IdCanzone', name='StatCanzoniPK')
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
                                        ins = "INSERT INTO Utenti VALUES (?,?,?,?,?,?,?,?,?)"
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
                                        ins = "INSERT INTO Artisti VALUES (?,?)"
                                        connection.execute(ins, tail)
                                case "Playlist":
                                        ins = "INSERT INTO Playlist VALUES (?,?,?,?,?)"
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
                                        ins = "INSERT INTO Canzoni VALUES (?,?,?,?,?,?)"
                                        # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                        tail[1] = cambiaCaratteri(tail[1])
                                        head2, *tail2 = tail
                                        if head2 == "None":
                                                connection.execute(ins, [None]+tail2)
                                        else:
                                                connection.execute(ins, tail)
                                case "Album":
                                        ins = "INSERT INTO Album VALUES (?,?,?,?,?,?)"
                                        # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                        tail[1] = cambiaCaratteri(tail[1])
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
                                        tail[0] = cambiaCaratteri(tail[0])
                                        connection.execute(ins, tail)
                                case "Raccolte":
                                        ins = "INSERT INTO Raccolte VALUES (?,?)"
                                        connection.execute(ins, tail)
                                case "Contenuto":
                                        ins = "INSERT INTO Contenuto VALUES (?,?)"
                                        connection.execute(ins, tail)
                                case "AttributoCanzone":
                                        ins = "INSERT INTO AttributoCanzone VALUES (?,?)"
                                        tail[0] = cambiaCaratteri(tail[0])
                                        connection.execute(ins, tail)
                                case "AttributoAlbum":
                                        ins = "INSERT INTO AttributoAlbum VALUES (?,?)"
                                        tail[0] = cambiaCaratteri(tail[0])
                                        connection.execute(ins, tail)
                                case "AttributoPlaylist":
                                        ins = "INSERT INTO AttributoPlaylist VALUES (?,?)"
                                        tail[0] = cambiaCaratteri(tail[0])
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
                                ins = "INSERT INTO Artisti VALUES (?,?)"
                                connection.execute(ins, tail)
                        elif(head == "Playlist"):
                                ins = "INSERT INTO Playlist VALUES (?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                if(tail[3] == "void"):
                                    tail[3] = ""
                                head2, *tail2 = tail
                                if head2 == "None":
                                        connection.execute(ins, [None]+tail2)
                                else:
                                        connection.execute(ins, tail)
                        elif(head == "Canzoni"):
                                ins = "INSERT INTO Canzoni VALUES (?,?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                tail[1] = cambiaCaratteri(tail[1])
                                head2, *tail2 = tail
                                if head2 == "None":
                                        connection.execute(ins, [None]+tail2)
                                else:
                                        connection.execute(ins, tail)
                        elif(head == "Album"):
                                ins = "INSERT INTO Album VALUES (?,?,?,?,?,?)"
                                # None per avere un Integer con autoincremento. Mettere gli autoincrement per primi per poter estrarre i None
                                tail[1] = cambiaCaratteri(tail[1])
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
                                tail[0] = cambiaCaratteri(tail[0])
                                connection.execute(ins, tail)
                        elif(head == "Raccolte"):
                                ins = "INSERT INTO Raccolte VALUES (?,?)"
                                connection.execute(ins, tail)
                        elif(head == "Contenuto"):
                                ins = "INSERT INTO Contenuto VALUES (?,?)"
                                connection.execute(ins, tail)
                        elif(head == "AttributoCanzone"):
                                ins = "INSERT INTO AttributoCanzone VALUES (?,?)"
                                tail[0] = cambiaCaratteri(tail[0])
                                connection.execute(ins, tail)
                        elif(head == "AttributoAlbum"):
                                ins = "INSERT INTO AttributoAlbum VALUES (?,?)"
                                tail[0] = cambiaCaratteri(tail[0])
                                connection.execute(ins, tail)
                        elif(head == "AttributoPlaylist"):
                                ins = "INSERT INTO AttributoPlaylist VALUES (?,?)"
                                tail[0] = cambiaCaratteri(tail[0])
                                connection.execute(ins, tail)
                        elif(head == "StatCanzoni"):
                                ins = "INSERT INTO StatCanzoni VALUES (?,?)"
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