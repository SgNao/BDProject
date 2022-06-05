from flask import *
from sqlalchemy import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered
from login import LoginBP
from user import UserBP
from song import SongBP
from artist import ArtistBP
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2
import configdb

conn = configdb.setupConnection()

'''
export FLASK_APP=main.py
export FLASK_ENV=development
flask run

set FLASK_APP=main.py
set FLASK_ENV=development
$env:FLASK_APP = "main.py"
flask run
'''

app = Flask(__name__)

app.register_blueprint(LoginBP)
app.register_blueprint(UserBP)
app.register_blueprint(SongBP)
app.register_blueprint(ArtistBP)

engine = create_engine('sqlite:///database.db', echo=True)
app.config['SECRET_KEY'] = 'ubersecret'
login_manager = LoginManager()
login_manager.init_app(app)


# IMPORTANTE NON TOGLIERE
@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)


class User(UserMixin):
    def __init__(self, id, email, nome, cognome, nick, birthday, Password):
        self.id = id
        self.email = email
        self.nome = nome
        self.cognome = cognome
        self.nick = nick
        self.birthday = birthday
        self.Password = Password

    def verify_password(self, pwd):
        return check_password_hash(self.Password, pwd)


def get_user_by_email(email):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM Utenti WHERE Email = ?', email)
    user = rs.fetchone()
    conn.close()
    return User(user.IdUtenti, user.Email, user.Nome, user.Cognome, user.Nickname, user.DataNascita, user.Password)


@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM Utenti WHERE IdUtenti = ?', user_id)
    user = rs.fetchone()
    conn.close()
    return User(user.IdUtenti, user.Email, user.Nome, user.Cognome, user.Nickname, user.DataNascita, user.Password)


def latest_s():
    conn = engine.connect()
    rs = conn.execute('SELECT Titolo, Rilascio, Lingua FROM Canzoni ORDER BY Rilascio DESC LIMIT 5')
    latest_songs = rs.fetchone()
    conn.close()
    return latest_songs


def all_s():
    conn = engine.connect()
    rs = conn.execute('SELECT Titolo, Rilascio, Lingua FROM Canzoni')
    all_songs = rs.fetchone()
    conn.close()
    return all_songs


def most_played():
    conn = engine.connect()
    rs = conn.execute('SELECT C.* FROM StatCanzoni S NATURAL JOIN Canzoni C NATURAL JOIN '
                      'Statistiche ST WHERE IdStatistica IN (SELECT * FROM Statistiche '
                      'ORDER BY NRiproduzioniTotali DESC LIMIT 5)')
    most_p = rs.fetchone()
    conn.close()
    return most_p


@app.route('/')
def home():
    latest_songs = latest_s()
    most_played_songs = most_played()
    all_songs = all_s()

    if current_user.is_authenticated:
        user = current_user.__getattribute__(id)  # controllare con currUser() di user.py
        recommended_songs = [{'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                             {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                             {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                             {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                             {'Titolo': "Sweet Child O' Mine", 'Anno': 1987,
                              'Tag': "#Rock and Roll"}]  # Implementare query che ritorna le canzoni consigliate per l'utente

        return render_template("Index.html", user=user, all_songs=all_songs, latest_songs=latest_songs,
                               most_played_songs=most_played_songs, recommended_songs=recommended_songs)
    return render_template("Index.html", all_songs=all_songs, latest_songs=latest_songs,
                           most_played_songs=most_played_songs)
