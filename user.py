from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered
from flask import *
from sqlalchemy import *
from flask_login import login_required

UserBP = Blueprint('UserBP', __name__)
engine = create_engine('sqlite:///database.db', echo=True)


# IMPORTANTE NON TOGLIERE
@UserBP.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)

def currUser():
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM Utenti WHERE IdUtenti = ?', current_user.id)
    curr_user = rs.fetchone()
    conn.close()
    return curr_user

def getPlaylist(userid):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM Playlist WHERE IdUtente = ?', userid)
    playlists = rs.fetchone()
    conn.close()
    return playlists


def getPlaylistSongs(playlistId):
    conn = engine.connect()
    rs = conn.execute('SELECT C.* FROM Raccolte R JOIN Canzoni C on C.IdCanzone = R.IdCanzone WHERE IdPlaylist = ?', playlistId)
    playlists_songs = rs.fetchone()
    conn.close()
    return playlists_songs

@UserBP.route('/private')
@login_required
def private():
    conn = engine.connect()
    rs = conn.execute(' SELECT * FROM Playlist WHERE Playlist.IdUtente = ?', current_user.id)
    playlists = rs.fetchall()
    rs = conn.execute(' SELECT Raccolte.IdPlaylist, Canzoni.Titolo, Canzoni.Rilascio, Canzoni.Durata, Canzoni.Colore'  
                      ' FROM Canzoni NATURAL JOIN Raccolte'
                      ' WHERE Raccolte.IdPlaylist IN (SELECT Playlist.IdPlaylist FROM Playlist'
                      ' WHERE Playlist.IdPlaylist = ?)'
                      ' GROUP BY Raccolte.IdPlaylist, Canzoni.Titolo, Canzoni.Rilascio, Canzoni.Durata, Canzoni.Colore', current_user.id)
    songs = rs.fetchall()
    playlist_songs = []
    for playlist in playlists:
        playlist_s = []
        for song in songs:
            if song.IdPlaylist == playlist.IdPlaylist:
                playlist_s.append(song)
        playlist_songs.append(playlist_s)
    print(playlist_songs)
    print(playlists)
    resp = make_response(render_template("UserPage.html", user=current_user, playlists=playlists, playlist_songs=playlist_songs))
    conn.close()
    return resp

@UserBP.route('/new_playlist', methods=['GET', 'POST'])
def NewPlaylist():
    if request.method == 'POST':
        conn = engine.connect()
        data = ( current_user.id, request.form["Nome"], request.form["Descrizione"], "0")
        # Serve sanitizzare l'input
        rs = conn.execute('INSERT INTO Playlist (IdUtente, Nome, Descrizione, NCanzoni) VALUES (?,?,?,?)', data)
        conn.close()
        return redirect(url_for('UserBP.private'))
    else:
        return render_template("NuovaRaccolta.html")

@UserBP.route('/mod_playlist', methods=['GET', 'POST'])
def ModPlaylist():
    if request.method == 'POST':
        #implementare query per creare una playlist
        # Serve sanitizzare l'input
        print('ciao')
    else:
         return render_template("ModificaRaccolta.html")

@UserBP.route('/mod_data', methods=['GET', 'POST'])
def ModData():
    if request.method == 'POST':
        #implementare query per creare una playlist
        # Serve sanitizzare l'input
        print('ciao')
    else:
         return render_template("ModificaDatiPersonali.html")

@UserBP.route('/Dati_Personali')
@login_required  # richiede autenticazione
def get_data():
    conn = engine.connect()
    resp = make_response(render_template("DatiPersonali.html", user=current_user))
    conn.close()
    return resp