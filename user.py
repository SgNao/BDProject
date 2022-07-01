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
    rs = conn.execute('SELECT * FROM utenti WHERE id_utente = ?', current_user.id)
    curr_user = rs.fetchone()
    conn.close()
    return curr_user

def getPlaylist(userid):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM playlist WHERE id_utente = ?', userid)
    playlists = rs.fetchone()
    conn.close()
    return playlists


def getPlaylistSongs(playlistId):
    conn = engine.connect()
    rs = conn.execute('SELECT C.* FROM raccolte R JOIN canzoni C on C.id_canzone = R.id_canzone WHERE id_playlist = ?', playlistId)
    playlists_songs = rs.fetchone()
    conn.close()
    return playlists_songs

@UserBP.route('/private')
@login_required
def private():
    conn = engine.connect()
    #rs = conn.execute(' SELECT * FROM playlist WHERE playlist.id_utente = ?', current_user.id)
    playlists =  getPlaylist(currUser()) #rs.fetchall()
    rs = conn.execute(' SELECT raccolte.id_playlist, canzoni.titolo, canzoni.rilascio, canzoni.durata, canzoni.colore'  
                      ' FROM canzoni NATURAL JOIN raccolte'
                      ' WHERE raccolte.id_playlist IN (SELECT playlist.id_playlist FROM playlist'
                      ' WHERE playlist.id_playlist = ?)'
                      ' GROUP BY raccolte.id_playlist, canzoni.titolo, canzoni.rilascio, canzoni.durata, canzoni.colore', current_user.id)
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
        rs = conn.execute('INSERT INTO playlist (id_utente, nome, descrizione, n_canzoni) VALUES (?,?,?,?)', data)
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

@UserBP.route('/delete_playlist/<IdPlaylist>', methods=['GET', 'POST'])
def DelPlaylist(IdPlaylist):
    if request.method == 'POST':
        conn = engine.connect()
        data = ( current_user.id, request.form["Nome"], request.form["Descrizione"], "0")
        # questa fa insert, no delete
        rs = conn.execute('INSERT INTO playlist (id_utente, nome, descrizione, n_canzoni) VALUES (?,?,?,?)', data)
        conn.close()
        return redirect(url_for('UserBP.private'))
    else:
        return render_template("NuovaRaccolta.html")

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