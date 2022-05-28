from flask import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered
from sqlalchemy import *
import os.path
import sys
import main
from werkzeug.security import *

'''
export FLASK_APP=Login.py
export FLASK_ENV=development
flask run

set FLASK_APP=Login.py
set FLASK_ENV=development
$env:FLASK_APP = "Login.py"
flask run
'''
#FUNZIONAAAAA

LoginBP = Blueprint('LoginBP', __name__)
engine = create_engine('sqlite:///database.db', echo=True)

# IMPORTANTE NON TOGLIERE
@LoginBP.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)
'''
app = Flask(__name__)
engine = create_engine('sqlite:///database.db', echo=True)
app.config['SECRET_KEY'] = 'ubersecret'
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):  # costruttore di classe
    def __init__(self, id, email, nome, cognome, nick, birthday, Password):  # active=True
        self.id = id
        self.email = email
        self.nome = nome
        self.cognome = cognome
        self.nick = nick
        self.birthday = birthday
        self.Password = Password
        # self.active = active


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
'''

@LoginBP.route('/')
def home():
    # current_user identifica l’utente attuale utente anonimo prima dell’autenticazione
    latest_songs = [{'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                    {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                    {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                    {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                    {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"}] #Implementare query che ritorna le 5 canzoni più recenti
    most_played_songs = [{'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                         {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                         {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                         {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                         {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"}] #Implementare query che ritorna le 5 canzoni più riprodotte
    all_songs = [{'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
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
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"}] #Implementare query che ritorna tutte le canzoni
    if current_user.is_authenticated:
        user={'Nome':'Donald','Cognome':'Duck', 'Nickname':'Ducky','Ruolo':'UTENTE'}#Implementare query che ritorna l'utente attuale
        recommended_songs = [{'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                             {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                             {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                             {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                             {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"}] #Implementare query che ritorna le canzoni consigliate per l'utente

        return render_template("Index.html", user=user, all_songs=all_songs, latest_songs=latest_songs, most_played_songs=most_played_songs, recommended_songs=recommended_songs)
    return render_template("Index.html",  all_songs=all_songs, latest_songs=latest_songs, most_played_songs=most_played_songs)

@LoginBP.route('/Accedi')
def Accedi():
    return render_template("Accedi.html")

@LoginBP.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute('SELECT Password FROM Utenti WHERE Email = ?', [request.form['user']])
        real_pwd = rs.fetchone()
        conn.close()

        print('1')

        if (real_pwd is not None):
            print('2')
            #if request.form['pass'] == real_pwd['Password']:
            if (check_password_hash(real_pwd, request.form['pass'])):
                print('3')
                user = main.get_user_by_email(request.form['user'])
                login_user(user)
                return redirect(url_for('LoginBP.home'))
            else:
                print('4')
                return redirect(url_for('LoginBP.Accedi'))
        else:
            print('5')
            return redirect(url_for('LoginBP.Accedi'))#redirect(url_for('LoginBP.home'))
    else:
        print('6')
        return redirect(url_for('LoginBP.Accedi'))#redirect(url_for('LoginBP.home'))


@LoginBP.route('/private')
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


@LoginBP.route('/logout')
@login_required  # richiede autenticazione
def logout():
    logout_user()
    return redirect(url_for('LoginBP.home'))


@LoginBP.route('/tosongs')
@login_required
def tosongs():
    return redirect(url_for('songs'))


@LoginBP.route('/songs')
@login_required
def songs():
    conn = engine.connect()
    songlist = conn.execute('SELECT * FROM Canzoni')
    resp = make_response(render_template("songs.html", songs=songlist))
    conn.close()
    return resp
