import flask_login
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
    rs = conn.execute('SELECT * FROM Utenti WHERE IdUtenti = ?', flask_login.current_user.id)
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
    rs = conn.execute('SELECT C.* FROM Raccolte R JOIN Canzoni C on C.IdCanzone = R.IdCanzone WHERE IdPlaylist = ?',
                      playlistId)
    playlists_songs = rs.fetchone()
    conn.close()
    return playlists_songs


@UserBP.route('/private')
@login_required  # richiede autenticazione
def private():
    conn = engine.connect()
    # users = conn.execute("SELECT * FROM Utenti") user={'Nome':'Donald','Cognome':'Duck', 'Nickname':'Ducky',
    # 'Ruolo':'UTENTE'}#Implementare query che ritorna l'utente attuale
    user = currUser()

    # playlists=[{'Nome':'Giro a Paperopoli','Descrizione':'Le migliori canzoni paperopolesi'}]#Implementare query
    # che ricava le playlist dell'utente
    playlists = getPlaylist(user.IdUtente)

    # playlist_songs = [{'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"}, {'Titolo': "Sweet
    # Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"}, {'Titolo': "Sweet Child O' Mine", 'Anno': 1987,
    # 'Tag': "#Rock and Roll"}, {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"}, {'Titolo':
    # "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"}, {'Titolo': "Sweet Child O' Mine", 'Anno': 1987,
    # 'Tag': "#Rock and Roll"}, {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"}, {'Titolo':
    # "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"}, {'Titolo': "Sweet Child O' Mine", 'Anno': 1987,
    # 'Tag': "#Rock and Roll"}, {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"}, {'Titolo':
    # "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"}, {'Titolo': "Sweet Child O' Mine", 'Anno': 1987,
    # 'Tag': "#Rock and Roll"}]  # E le relative canzoni

    playlist_songs = getPlaylistSongs(playlists.IdPlaylist)

    resp = make_response(
        render_template("UserPage.html", user=user, playlists=playlists, playlist_songs=playlist_songs))
    conn.close()
    return resp
