from sqlalchemy import *

engine = create_engine('sqlite:///database.db', echo = True)
metadata = MetaData()

# Mettere gli autoincrement per primi per poter estrarre i None nel popbd
users = Table('Utenti', metadata, 
        Column('IdUtenti', Integer, primary_key=True, nullable=False, autoincrement=True),
        Column('Email', String(64), nullable=False, unique=True),
        Column('Nome', String(32), nullable=False), 
        Column('Cognome', String(32), nullable=False),
        Column('Nickname', String(16), nullable=True, unique=True),
        Column('Bio', String(144), nullable=True),
        Column('DataNascita', Date, nullable=False),
        Column('Password', String(160), nullable=False),
        Column('Ruolo', Integer, CheckConstraint('Ruolo>0'),CheckConstraint('Ruolo <4'), nullable=False),
        #Index('idx_email', 'Email')
        )

artist = Table('Artisti', metadata,
        Column('IdUtente', Integer, ForeignKey("Utenti.IdUtenti", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True, nullable=False),
        Column('Debutto', Date, nullable=True),
        #Index('idx_Utente', 'Id_Utente')
        )
#trigger per la prima canzone caricata?
playlist = Table('Playlist', metadata,
        Column('IdPlaylist', Integer, primary_key=True, nullable=False, autoincrement=True),
        Column('IdUtente', Integer, ForeignKey("Utenti.IdUtenti", onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
        Column('Nome', String(144), nullable=False),
        Column('Descrizione', String(144), nullable=True),
        Column('NCanzoni', Integer, CheckConstraint('NCanzoni>=0'), nullable=False),
        #Index('idx_playlist', 'Id_Utente', 'Nome')
        )
# possibile usare un ARRAY per avere più di un tag
canzoni = Table('Canzoni', metadata,
        Column('IdCanzone', Integer, primary_key=True, nullable=False, autoincrement=True),
        Column('Titolo', String(32), nullable=False),
        Column('Rilascio', Date, nullable=False),
        Column('Durata', Integer, nullable=False),
        Column('Colore', String(32), nullable=False),
        Column('Lingua', String(32), nullable=False),
        Column('IdArtista', Integer, ForeignKey('Artisti.IdUtente', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        #Index('idx_canzone_anno', 'Anno'),
        #Index('idx_canzone_Titolo', 'Titolo')
        )

album = Table('Album', metadata,
        Column('IdAlbum', Integer, primary_key=True, nullable=False, autoincrement=True),
        Column('Titolo', String, nullable=False),
        Column('Rilascio', Date, nullable=False),
        Column('Colore', String(32), nullable=False),
        Column('NCanzoni', Integer, nullable=False),
        Column('CasaDiscografica', String(64), nullable=False),
        Column('IdArtista', Integer, ForeignKey('Artisti.IdUtente', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        #Index('idx_album_titolo', 'Titolo'),
        #Index('idx_album_anno', 'Anno')
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
        Column('Tag', String(128), primary_key=True, nullable=False),
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
        Column('IdTag', String(128), ForeignKey('Tag.Tag', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        Column('IdCanzone', Integer, ForeignKey('Canzoni.IdCanzone', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        PrimaryKeyConstraint('IdTag', 'IdCanzone', name='AttributoCanzonePK')
        )

attAlbum = Table('AttributoAlbum', metadata,
        Column('IdTag', String(128), ForeignKey('Tag.Tag', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        Column('IdAlbum', Integer, ForeignKey('Album.IdAlbum', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        PrimaryKeyConstraint('IdTag', 'IdAlbum', name='AttributoAlbumPK')
        )

AttPlaylist = Table('AttributoPlaylist', metadata,
        Column('IdTag', String(128), ForeignKey('Tag.Tag', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        Column('IdPlaylist', Integer, ForeignKey('Playlist.IdPlaylist', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        PrimaryKeyConstraint('IdTag', 'IdPlaylist', name='AttributoPlaylistPK')
        )

StatCanzoni = Table('StatCanzoni', metadata,
        Column('IdStatistica', Integer, ForeignKey('Statistiche.IdStatistica', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        Column('IdCanzone', Integer, ForeignKey('Canzoni.IdCanzone', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
        PrimaryKeyConstraint('IdStatistica', 'IdCanzone', name='StatCanzoniPK')
        )

metadata.create_all(engine)