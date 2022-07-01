from flask import *
from sqlalchemy import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

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
    rs = conn.execute(' SELECT * FROM canzoni WHERE canzoni.id_canzone = ?', IdCanzone)
    songdata = rs.fetchone()
    rs = conn.execute(' SELECT contenuto.id_album FROM canzoni NATURAL JOIN contenuto WHERE canzoni.id_canzone = ?', IdCanzone)
    IdAlbum = rs.fetchone()
    rs = conn.execute(' SELECT * FROM canzoni NATURAL JOIN contenuto WHERE contenuto.id_album = ?', IdAlbum)
    songAlbum = rs.fetchall()
    rs = conn.execute(' SELECT * FROM playlist WHERE playlist.id_utente = ?', current_user.id)
    playlists = rs.fetchall()
    print(songAlbum)
    resp = make_response(render_template("Song.html", playlists=playlists, song=songdata, songAlbum=songAlbum))
    conn.close()
    return resp