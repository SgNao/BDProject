from flask import *
from sqlalchemy import *

SongBP = Blueprint('SongBP', __name__)
engine = create_engine('sqlite:///database.db', echo=True)

# IMPORTANTE NON TOGLIERE
@SongBP.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)

@SongBP.route('/song_stat')
def SongStat():
    return render_template("SongStatistics.html")

@SongBP.route('/songs/<IdCanzone>')
def songs(IdCanzone):
    conn = engine.connect()
    rs = conn.execute(' SELECT * FROM Canzoni WHERE Canzoni.IdCanzone = ?', IdCanzone)
    songdata = rs.fetchone()
    rs = conn.execute(' SELECT Contenuto.IdAlbum FROM Canzoni NATURAL JOIN Contenuto WHERE Canzoni.IdCanzone = ?', IdCanzone)
    IdAlbum = rs.fetchone()
    rs = conn.execute(' SELECT * FROM Canzoni NATURAL JOIN Contenuto WHERE Contenuto.IdAlbum = ?', IdAlbum)
    songAlbum = rs.fetchall()
    print(songAlbum)
    resp = make_response(render_template("Song.html", song=songdata, songAlbum=songAlbum))
    conn.close()
    return resp