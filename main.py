from flask import *
from sqlalchemy import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered
from Login import LoginBP
from user import UserBP
from song import SongBP
from werkzeug.security import check_password_hash, generate_password_hash

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
    # current_user identifica l’utente attuale utente anonimo prima dell’autenticazione
    # latest_songs = [{'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987,
    #                  'Tag': "#Rock and Roll"}]  # Implementare query che ritorna le 5 canzoni più recenti

    latest_songs = latest_s()

    # most_played_songs = [{'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #                      {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #                      {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #                      {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #                      {'Titolo': "Sweet Child O' Mine", 'Anno': 1987,
    #                       'Tag': "#Rock and Roll"}]  # Implementare query che ritorna le 5 canzoni più riprodotte

    most_played_songs = most_played()

    # all_songs = [{'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #              {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #              {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #              {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #              {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #              {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #              {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #              {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #              {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #              {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #              {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
    #              {'Titolo': "Sweet Child O' Mine", 'Anno': 1987,
    #               'Tag': "#Rock and Roll"}]  # Implementare query che ritorna tutte le canzoni

    all_songs = all_s()

    if current_user.is_authenticated:
        # user = {'Nome': 'Donald', 'Cognome': 'Duck', 'Nickname': 'Ducky',
        #         'Ruolo': 'UTENTE'}  # Implementare query che ritorna l'utente attuale
        user = current_user.__getattribute__(id)  # controllare con currUser() di user.py
        recommended_songs = [{'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                             {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                             {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                             {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                             {'Titolo': "Sweet Child O' Mine", 'Anno': 1987,
                              'Tag': "#Rock and Roll"}]  # Implementare query che ritorna le canzoni consigliate per
        # l'utente

        return render_template("Index.html", user=user, all_songs=all_songs, latest_songs=latest_songs,
                               most_played_songs=most_played_songs, recommended_songs=recommended_songs)
    return render_template("Index.html", all_songs=all_songs, latest_songs=latest_songs,
                           most_played_songs=most_played_songs)


'''
# Controllo che esista database e, in caso non esistesse, lo genero
try:
    os.path.realpath('database.bd', strict=True)
except:
    # Il database manca, quindi provo a generarlo. Controllo che ci sia il file csv per farlo
    # Se non c'è il file csv, mando una eccezione
    try:
        os.path.realpath('./songdb.csv', strict=True)
    except:
        raise Exception('Manca il file csv per generare il database')
    if(sys.version_info[0]<3):
        execfile('gendb.py')
        execfile('popdb.py')
    else:
        exec(open('gendb.py').read())
        exec(open('popdb.py').read())
'''
