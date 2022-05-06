from sqlalchemy import *

engine = create_engine('sqlite:///database.db', echo = True)
metadata = MetaData()

users = Table('Utenti', metadata, 
            Column('Email', String(17), primary_key=True, nullable=False),
            Column('Nome', String(17), nullable=False), 
            Column('Cognome', String(17), nullable=False),
            Column('Nickname', String(24), nullable=True, unique=True),
            Column('Data_Nascita', Date, nullable=False),
            Column('Password', String(16), nullable=False),
        )
#Index('idx_email', 'email')
metadata.create_all(engine)
#Text non ha limiti di caratteri, String deve essere specificato; Per testare ho messo String(17) visto che da errore perchè Text non ha limiti
 #index singoli. Per index multicolonna serve crearli dopo l'ultima colonna
 #mettiamo un limite alla grandezza?
artist = Table('Artisti', metadata,
            Column('Id_Utente', String(17), ForeignKey("Utenti.Email", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True, nullable=False),
            Column('Bio', String(160), nullable=True), 
            Column('Debutto', Date, nullable=True),
        )
#Index('idx_Utente', 'Id_Utente')
metadata.create_all(engine)
 #trigger per la prima canzone caricata?
playlist = Table('Playlist', metadata,
            Column('Id_Playlist', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Id_utente', String(17), ForeignKey("Utenti.Email", onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
            Column('Nome', String(24), nullable=False),
            Column('Descrizione', String(160), nullable=True),
            Column('Tag', String(24), nullable=False), 
            Column('N_Canzoni', Integer, nullable=False),
        )
#Index('idx_playlist', 'Id_Utente', 'Nome')
metadata.create_all(engine)
# possibile usare un ARRAY per avere più di un tag
canzoni = Table('Canzoni', metadata,
            Column('Id_Canzone', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Titolo', String(17), nullable=False),
            Column('Anno', Integer, nullable=False),
            Column('Durata', Integer, nullable=False),
            Column('Genere', String(17), nullable=False),
            Column('Tag', String(17), nullable=False),
            Column('N_Riproduzioni', Integer, nullable=False),
            Column('Lingua', String(17), nullable=False),
            Column('Id_Artista', String(17), ForeignKey('Artisti.Id_Utente', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        )
#Index('idx_canzone_anno', 'Anno'),
#Index('idx_canzone_Titolo', 'Titolo')
metadata.create_all(engine)
#per possibili raccomandazioni in base ad anno
album = Table('Album', metadata,
            Column('Id_Album', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Titolo', String(17), nullable=False),
            Column('Anno', Integer, nullable=False),
            Column('Genere', String(17), nullable=False),
            Column('N_Canzoni', Integer, nullable=False),
            Column('Casa_Discografica', String(17), nullable=False),
            Column('Id_Artista', String(17), ForeignKey('Artisti.Id_Utente', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        )
#Index('idx_album_titolo', 'Titolo'),
#Index('idx_album_anno', 'Anno')
metadata.create_all(engine)
raccolte = Table('Raccolte', metadata,
            Column('Id_Playlist', Integer, ForeignKey('Playlist.Id_Playlist', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
            Column('Id_Canzone', Integer, ForeignKey('Canzoni.Id_Canzone', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
            PrimaryKeyConstraint('Id_Playlist', 'Id_Canzone', name='Raccolte_PK')
        )
metadata.create_all(engine)
contenuto = Table('Contenuto', metadata,
            Column('Id_Album', Integer, ForeignKey('Album.Id_Album', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
            Column('Id_Canzone', Integer, ForeignKey('Canzoni.Id_Canzone', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
            PrimaryKeyConstraint('Id_Album', 'Id_Canzone', name='Conteuto_PK')
        )

metadata.create_all(engine)

conn = engine.connect()
ins = "INSERT INTO Utenti VALUES (?,?,?,?,?,?)"
conn.execute(ins, ['alice@gmail.com', 'alice', 'A', 'Ali', '2022-05-06', 'love'])
conn.execute(ins, ['bob@gmail.com', 'bob', 'B', 'Bo', '2022-05-06', 'milk'])

user_list = conn.execute("SELECT * FROM Utenti")
for u in user_list:
    print(u)
