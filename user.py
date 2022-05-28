from flask import *
from sqlalchemy import *
from flask_login import login_required

UserBP = Blueprint('UserBP', __name__)
engine = create_engine('sqlite:///database.db', echo=True)

# IMPORTANTE NON TOGLIERE
@UserBP.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)

@UserBP.route('/private')
@login_required  # richiede autenticazione
def private():
    conn = engine.connect()
    #users = conn.execute("SELECT * FROM Utenti")
    user={'Nome':'Donald','Cognome':'Duck', 'Nickname':'Ducky','Ruolo':'UTENTE'}#Implementare query che ritorna l'utente attuale
    playlists=[{'Nome':'Giro a Paperopoli','Descrizione':'Le migliori canzoni paperopolesi'}]#Implementare query che ricava le playlist dell'utente
    playlist_songs = [{'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"}] #E le relative canzoni
    resp = make_response(render_template("UserPage.html", user=user, playlists=playlists, playlist_songs=playlist_songs))
    conn.close()
    return resp