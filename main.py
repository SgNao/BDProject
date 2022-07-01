from flask import *
from sqlalchemy import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered
from login import LoginBP
from user import UserBP
from song import SongBP
from artist import ArtistBP
from werkzeug.security import check_password_hash, generate_password_hash
#import psycopg2
#import configdb

#conn = configdb.setupConnection()

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
    def __init__(self, id, email, nome, cognome, nickname, bio, data_nascita, password, ruolo):  # active=True
        self.id = id
        self.email = email
        self.nome = nome
        self.cognome = cognome
        self.nickname = nickname
        self.bio = bio
        self.data_nascita = data_nascita
        self.password = password
        self.ruolo = ruolo

def verify_password(self, pwd):
    return check_password_hash(self.Password, pwd)

def get_user_by_email(email):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM utenti WHERE email = ?', email)
    user = rs.fetchone()
    conn.close()
    return User(user.id_utenti, user.email, user.nome, user.cognome, user.nickname, user.bio, user.data_nascita, user.password, user.ruolo)

@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM utenti WHERE id_utenti = ?', user_id)
    user = rs.fetchone()
    conn.close()
    return User(user.id_utenti, user.email, user.nome, user.cognome, user.nickname, user.bio, user.data_nascita, user.password, user.ruolo)

@app.route('/')
def home():
    # current_user identifica l’utente attuale utente anonimo prima dell’autenticazione

    conn = engine.connect()
    
    rs = conn.execute('SELECT id_canzone, titolo, rilascio FROM canzoni')
    all_songs = rs.fetchall()

    rs = conn.execute('SELECT id_canzone, titolo, rilascio FROM canzoni ORDER BY rilascio DESC LIMIT 5')
    latest_songs = rs.fetchall()

    most_played_songs = [{'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                         {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                         {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                         {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                         {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"}] #Implementare query che ritorna le 5 canzoni più riprodotte

    if current_user.is_authenticated:
        recommended_songs = [{'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                             {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                             {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                             {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                             {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"}] #Implementare query che ritorna le canzoni consigliate per l'utente

        conn.close()
        return render_template("Index.html", user=current_user, all_songs=all_songs, latest_songs=latest_songs, most_played_songs=most_played_songs, recommended_songs=recommended_songs)
    
    conn.close()
    return render_template("Index.html", all_songs=all_songs, latest_songs=latest_songs, most_played_songs=most_played_songs)