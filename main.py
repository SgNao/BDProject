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

app.config['SECRET_KEY'] = 'ubersecret'
login_manager = LoginManager()
login_manager.init_app(app)

# IMPORTANTE NON TOGLIERE
@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)

class User(UserMixin):
    def __init__(self, id, email, nome, cognome, nickname, bio, data_nascita, password, ruolo):
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
        return check_password_hash(self.password, pwd)

def get_user_by_email(email):
    conn = configdb.getConnection()
    rs = None
    if(configdb.selectDB() == true):
        cur = conn.cursor()
        rs = cur.execute('SELECT * FROM unive_music.utenti WHERE email = %s', email)
        conn.commit()
        cur.close()
    else:
        rs = conn.execute('SELECT * FROM utenti WHERE email = ?', email)
    user = rs.fetchone()
    conn.close()
    return User(user.id_utente, user.email, user.nome, user.cognome, user.nickname, user.bio, user.data_nascita, user.password, user.ruolo)

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
    conn = configdb.getConnection()
    rs = conn.execute('SELECT * FROM utenti WHERE id_utente = ?', user_id)
    user = rs.fetchone()
    conn.close()
    return User(user.id_utente, user.email, user.nome, user.cognome, user.nickname, user.bio, user.data_nascita, user.password, user.ruolo)

@app.route('/')
def home():
    # current_user identifica l’utente attuale utente anonimo prima dell’autenticazione

    conn = configdb.getConnection()
    
    rs = conn.execute(' SELECT canzoni.id_canzone, canzoni.titolo, canzoni.rilascio, utenti.nickname'
                      ' FROM canzoni JOIN utenti ON canzoni.id_artista = utenti.id_utente')
    all_songs = rs.fetchall()
    all_songs =  ResultProxy_To_ListOfDict(all_songs)
    for song in all_songs:
        rs = conn.execute('SELECT attributo_canzone.id_tag FROM attributo_canzone WHERE attributo_canzone.id_canzone = ?', song['id_canzone'])
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
        rs = conn.execute('SELECT attributo_canzone.id_tag FROM attributo_canzone WHERE attributo_canzone.id_canzone = ?', song['id_canzone'])
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
        rs = conn.execute('SELECT attributo_canzone.id_tag FROM attributo_canzone WHERE attributo_canzone.id_canzone = ?', song['id_canzone'])
        tags = rs.fetchall()
        if tags:
           song['Tag_1'] = tags[0][0]
           song['Tag_2'] = tags[1][0]

    conn.close()
    return render_template("Index.html", all_songs=all_songs, latest_songs=latest_songs, most_played_songs=most_played_songs)

@app.route('/Reset')
@login_required
def Reset():
    conn = configdb.getConnection()

    rs = conn.execute('UPDATE statistiche SET n_riproduzioni_settimanali = ?', 0)

    conn.close()
    return redirect(url_for('home'))
