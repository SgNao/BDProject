from flask import *
from sqlalchemy import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

SongBP = Blueprint('SongBP', __name__)
engine = create_engine('sqlite:///database.db', echo=True)

# IMPORTANTE NON TOGLIERE
@SongBP.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)

@SongBP.route('/SongStat/<IdCanzone>')
def SongStat(IdCanzone):
    conn = engine.connect()
    rs = conn.execute(' SELECT * FROM Statistiche WHERE Statistiche.IdStatistica = ('
                      ' SELECT Statistiche.IdStatistica FROM StatCanzoni NATURAL JOIN Statistiche' 
                      ' WHERE StatCanzoni.IdCanzone = ?)', IdCanzone)
    stat = rs.fetchone()
    Tot = stat[1]+stat[2]+stat[3]+stat[4]+stat[5]+stat[6]
    statistiche = {'Fascia1': stat[1],'Fascia2': stat[2],'Fascia3': stat[3],'Fascia4': stat[4],'Fascia5': stat[5],'Fascia6': stat[6],'Tot': Tot,
                    'NRiproduzioniTotali': stat[7], 'NRiproduzioniSettimanali': stat[8]}
    rs = conn.execute(' SELECT * FROM Canzoni JOIN Utenti ON Canzoni.IdArtista = Utenti.IdUtenti WHERE Canzoni.IdCanzone = ?', IdCanzone)
    song = rs.fetchone()
    conn.close()
    return render_template("SongStatistics.html", stat=statistiche, song=song)

@SongBP.route('/songs/<IdCanzone>')
def songs(IdCanzone):
    conn = engine.connect()
    rs = conn.execute(' SELECT Statistiche.NRiproduzioniTotali, Statistiche.NRiproduzioniSettimanali'
                      ' FROM Statistiche NATURAL JOIN StatCanzoni'
                      ' WHERE StatCanzoni.IdCanzone = ?', IdCanzone)
    Stat = rs.fetchone()
    rs = conn.execute(' UPDATE Statistiche SET NRiproduzioniTotali = ?, NRiproduzioniSettimanali = ?'
                      ' WHERE IdStatistica = (SELECT StatCanzoni.IdStatistica FROM StatCanzoni'
                      ' WHERE StatCanzoni.IdCanzone = ?)', Stat[0]+1, Stat[1]+1, IdCanzone)
    rs = conn.execute(' SELECT * FROM Canzoni JOIN Utenti ON Canzoni.IdArtista = Utenti.IdUtenti'
                      ' WHERE Canzoni.IdCanzone = ?', IdCanzone)
    songdata = rs.fetchone()
    rs = conn.execute(' SELECT Contenuto.IdAlbum FROM Canzoni NATURAL JOIN Contenuto WHERE Canzoni.IdCanzone = ?', IdCanzone)
    IdAlbum = rs.fetchone()
    rs = conn.execute(' SELECT * FROM Canzoni NATURAL JOIN Contenuto JOIN Utenti ON Canzoni.IdArtista = Utenti.IdUtenti'
                      ' WHERE Contenuto.IdAlbum = ?', IdAlbum)
    songAlbum = rs.fetchall()
    rs = conn.execute(' SELECT * FROM Album WHERE IdAlbum = ?', IdAlbum)
    album = rs.fetchone()
    if current_user.is_authenticated:
        rs = conn.execute(' SELECT * ' 
                      ' FROM Playlist ' 
                      ' WHERE Playlist.Idutente = ?  AND Playlist.IdPlaylist NOT IN (SELECT Raccolte.IdPlaylist'
                      ' FROM Raccolte NATURAL JOIN Canzoni WHERE Canzoni.IdCanzone = ?)'
                      ' ORDER BY Playlist.Nome', current_user.id, IdCanzone)
        playlists = rs.fetchall()
    rs = conn.execute('SELECT AttributoCanzone.IdTag FROM AttributoCanzone WHERE AttributoCanzone.IdCanzone = ?', IdCanzone)
    tags = rs.fetchall()
    Tags = {'Tag_1': tags[0][0], 'Tag_2': tags[1][0]}
    if current_user.is_authenticated:
        resp = make_response(render_template("Song.html", playlists=playlists, song=songdata, songAlbum=songAlbum, album=album, tags=Tags))
    else:
        resp = make_response(render_template("Song.html", song=songdata, songAlbum=songAlbum, album=album, tags=Tags))
    conn.close()
    return resp