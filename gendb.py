from sqlalchemy import *

engine = create_engine('sqlite:///database.db', echo = True)
metadata = MetaData()

users = Table('Utenti', metadata, 
        Column('Id_Utenti', Integer, primary_key=True, nullable=False, autoincrement=True),
        Column('Email', String, nullable=False),
        Column('Nome', String, nullable=False), 
        Column('Cognome', String, nullable=False),
        Column('Nickname', String(32), nullable=True, unique=True),
        Column('Data_Nascita', Date, nullable=False),
        Column('Password', String(16), nullable=False),
        Index('idx_email', 'Email'),
        )

artist = Table('Artisti', metadata,
        Column('Id_Utente', Integer, ForeignKey("Utenti.Id_Utenti", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True, nullable=False),
        Column('Bio', String(160), nullable=True), 
        Column('Debutto', Date, nullable=True),
        Index('idx_Utente', 'Id_Utente')
        )
#trigger per la prima canzone caricata?
playlist = Table('Playlist', metadata,
        Column('Id_Playlist', Integer, primary_key=True, nullable=False, autoincrement=True),
        Column('Id_Utente', Integer, ForeignKey("Utenti.Id_Utenti", onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
        Column('Nome', String(24), nullable=False),
        Column('Descrizione', String(160), nullable=True),
        Column('N_Canzoni', Integer, CheckConstraint('N_Canzoni >0'), nullable=False),
        Index('idx_playlist', 'Id_Utente', 'Nome')
        )
# possibile usare un ARRAY per avere più di un tag
canzoni = Table('Canzoni', metadata,
        Column('Id_Canzone', Integer, primary_key=True, nullable=False, autoincrement=True),
        Column('Titolo', String, nullable=False),
        Column('Anno', Integer, nullable=False),
        Column('Durata', Integer, nullable=False),
        Column('Genere', String, nullable=False),
        Column('Tag', String, nullable=False),
        Column('N_Riproduzioni', Integer, nullable=False),
        Column('Lingua', String, nullable=False),
        Column('Id_Artista', Integer, ForeignKey('Artisti.Id_Utente', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        Index('idx_canzone_anno', 'Anno'),
        Index('idx_canzone_Titolo', 'Titolo')
        )

album = Table('Album', metadata,
        Column('Id_Album', Integer, primary_key=True, nullable=False, autoincrement=True),
        Column('Titolo', String, nullable=False),
        Column('Anno', Integer, nullable=False),
        Column('Genere', String, nullable=False),
        Column('N_Canzoni', Integer, nullable=False),
        Column('Casa_Discografica', String, nullable=False),
        Column('Id_Artista', Integer, ForeignKey('Artisti.Id_Utente', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        Index('idx_album_titolo', 'Titolo'),
        Index('idx_album_anno', 'Anno')
        )

tag = Table('Tag', metadata,
        Column('Tag', String, primary_key=True, nullable=False),
        )

raccolte = Table('Raccolte', metadata,
        Column('Id_Playlist', Integer, ForeignKey('Playlist.Id_Playlist', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        Column('Id_Canzone', Integer, ForeignKey('Canzoni.Id_Canzone', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        PrimaryKeyConstraint('Id_Playlist', 'Id_Canzone', name='Raccolte_PK')
        )

contenuto = Table('Contenuto', metadata,
        Column('Id_Album', Integer, ForeignKey('Album.Id_Album', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        Column('Id_Canzone', Integer, ForeignKey('Canzoni.Id_Canzone', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        PrimaryKeyConstraint('Id_Album', 'Id_Canzone', name='Conteuto_PK')
        )

attCanzone = Table('AttributoCanzone', metadata,
        Column('Id_Tag', String, ForeignKey('Tag.Tag', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        Column('Id_Canzone', Integer, ForeignKey('Canzoni.Id_Canzone', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        PrimaryKeyConstraint('Id_Tag', 'Id_Canzone', name='AttributoCanzone_PK')
        )

attAlbum = Table('AttributoAlbum', metadata,
        Column('Id_Tag', String, ForeignKey('Tag.Tag', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        Column('Id_Album', Integer, ForeignKey('Album.Id_Album', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        PrimaryKeyConstraint('Id_Tag', 'Id_Album', name='AttributoAlbum_PK')
        )

AttPlaylist = Table('AttributoPlaylist', metadata,
        Column('Id_Tag', String, ForeignKey('Tag.Tag', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        Column('Id_Playlist', Integer, ForeignKey('Playlist.Id_Playlist', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        PrimaryKeyConstraint('Id_Tag', 'Id_Playlist', name='AttributoPlaylist_PK')
        )

metadata.create_all(engine)

"""
conn = engine.connect()
ins = "INSERT INTO Utenti VALUES (?,?,?,?,?,?,?)"
conn.execute(ins, [None,'alice@gmail.com', 'alice', 'A', 'Ali', '2022-05-06', 'love'])
conn.execute(ins, [None,'bob@gmail.com', 'bob', 'B', 'Bo', '2022-05-06', 'milk'])
# None per avere un Integer con autoincremento
user_list = conn.execute("SELECT * FROM Utenti")
for u in user_list:
    print(u)
"""