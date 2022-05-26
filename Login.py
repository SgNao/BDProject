from flask import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered
from sqlalchemy import *
import os.path
import sys

# export FLASK_APP=Login.py
# export FLASK_ENV=development
# flask run

# set FLASK_APP=Login.py
# set FLASK_ENV=development
# $env:FLASK_APP = "Login.py"
# flask run

app = Flask(__name__)

# Controllo che esista database e, in caso non esistesse, lo genero
if(not os.path.exists('database.bd')):
    # Il database manca, quindi provo a generarlo. Controllo che ci sia il file csv per farlo
    # Se non c'è il file csv, mando una eccezione
    if(not os.path.exists('songdb.csv')):
        raise Exception('Manca il file csv per generare il database')
    else:
        if(sys.version_info[0]<3):
            execfile('gendb.py')
            execfile('popdb.py')
        else:
            exec(open('gendb.py').read())
            exec(open('popdb.py').read())
        
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
    return User(user.Id_Utenti, user.Email, user.Nome, user.Cognome, user.Nickname, user.Data_Nascita, user.Password)


@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM Utenti WHERE Id_Utenti = ?', user_id)
    user = rs.fetchone()
    conn.close()
    return User(user.Id_Utenti, user.Email, user.Nome, user.Cognome, user.Nickname, user.Data_Nascita, user.Password)


@app.route('/')
def home():
    # current_user identifica l’utente attuale utente anonimo prima dell’autenticazione
    if current_user.is_authenticated:
        return redirect(url_for('private'))
    return render_template("base.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute('SELECT Password FROM Utenti WHERE Email = ?', [request.form['user']])
        real_pwd = rs.fetchone()
        conn.close()

        if (real_pwd is not None):
            if request.form['pass'] == real_pwd['Password']:
                user = get_user_by_email(request.form['user'])
                login_user(user)
                return redirect(url_for('private'))
            else:
                return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


@app.route('/private')
@login_required  # richiede autenticazione
def private():
    conn = engine.connect()
    users = conn.execute('SELECT * FROM Utenti')
    resp = make_response(render_template("private.html", users=users))
    conn.close()
    return resp


@app.route('/logout')
@login_required  # richiede autenticazione
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/tosongs')
@login_required
def tosongs():
    return redirect(url_for('songs'))


@app.route('/songs')
@login_required
def songs():
    conn = engine.connect()
    songlist = conn.execute('SELECT * FROM Canzoni')
    resp = make_response(render_template("songs.html", songs=songlist))
    conn.close()
    return resp
