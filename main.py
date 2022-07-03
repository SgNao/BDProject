from flask import *
from sqlalchemy import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from login import LoginBP
from user import UserBP
from song import SongBP
from artist import ArtistBP
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2
import configdb

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
    def __init__(self, id, Email, Nome, Cognome, Nickname, Bio, DataNascita, Password, Ruolo):  # active=True
        self.id = id
        self.Email = Email
        self.Nome = Nome
        self.Cognome = Cognome
        self.Nickname = Nickname
        self.Bio = Bio
        self.DataNascita = DataNascita
        self.Password = Password
        self.Ruolo = Ruolo

    def verify_password(self, pwd):
        return check_password_hash(self.Password, pwd)

def get_user_by_email(email):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM Utenti WHERE Email = ?', email)
    user = rs.fetchone()
    conn.close()
    return User(user.IdUtenti, user.Email, user.Nome, user.Cognome, user.Nickname, user.Bio, user.DataNascita, user.Password, user.Ruolo)

def ResultProxy_To_ListOfDict(query_result):
    d, a = {}, []
    for rowproxy in query_result:
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
            # build up the dictionary
            d = {**d, **{column: value}}
        a.append(d)

    return a

@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM utenti WHERE id_utente = ?', user_id)
    user = rs.fetchone()
    conn.close()
    return User(user.IdUtenti, user.Email, user.Nome, user.Cognome, user.Nickname, user.Bio, user.DataNascita, user.Password, user.Ruolo)

@app.route('/')
def home():
    # current_user identifica l’utente attuale utente anonimo prima dell’autenticazione

    conn = engine.connect()
    
    rs = conn.execute(' SELECT canzoni.id_canzone, canzoni.titolo, canzoni.rilascio, utenti.nickname'
                      ' FROM Canzoni JOIN Utenti ON canzoni.id_artista = utenti.id_utente')
    all_songs = rs.fetchall()
    all_songs =  ResultProxy_To_ListOfDict(all_songs)
    for song in all_songs:
        rs = conn.execute('SELECT attributo_canzone.id_tag FROM attributo_canzone WHERE attributo_canzone.id_canzone = ?', song['IdCanzone'])
        tags = rs.fetchall()
        if tags:
           song['Tag_1'] = tags[0][0]
           song['Tag_2'] = tags[1][0]

    rs = conn.execute(' SELECT canzoni.id_canzone, canzoni.titolo, canzoni.rilascio, utenti.nickname' 
                      ' FROM canzoni JOIN utenti ON canzoni.id_artista = utenti.id_utente'
                      ' ORDER BY Canzoni.Rilascio DESC LIMIT 5')
    latest_songs = rs.fetchall()
    latest_songs =  ResultProxy_To_ListOfDict(latest_songs)
    for song in latest_songs:
        rs = conn.execute('SELECT attributo_canzone.id_tag FROM attributo_canzone WHERE attributo_canzone.id_canzone = ?', song['IdCanzone'])
        tags = rs.fetchall()
        if tags:
           song['Tag_1'] = tags[0][0]
           song['Tag_2'] = tags[1][0]

    rs = conn.execute(' SELECT canzoni.id_canzone, canzoni.titolo, canzoni.rilascio, utenti.nickname'
                      ' FROM canzoni JOIN utenti ON canzoni.id_artista = utenti.id_utente'
                      ' NATURAL JOIN statistiche_canzoni NATURAL JOIN statistiche'
                      ' ORDER BY statistiche.n_riproduzioni_totali DESC LIMIT 5')

    most_played_songs = rs.fetchall()
    most_played_songs =  ResultProxy_To_ListOfDict(most_played_songs)
    for song in most_played_songs:
        rs = conn.execute('SELECT attributo_canzone.id_tag FROM attributo_canzone WHERE attributo_canzone.id_canzone = ?', song['IdCanzone'])
        tags = rs.fetchall()
        if tags:
           song['Tag_1'] = tags[0][0]
           song['Tag_2'] = tags[1][0]

    conn.close()
    return render_template("Index.html", all_songs=all_songs, latest_songs=latest_songs, most_played_songs=most_played_songs)