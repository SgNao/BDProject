from flask import *
from sqlalchemy import *
from flask_login import LoginManager, UserMixin, login_required
from login import LoginBP
from user import UserBP
from song import SongBP
from artist import ArtistBP
from werkzeug.security import check_password_hash

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
engine = create_engine('postgresql://postgres:BDProject2022@localhost:5432/BDProject')

app.register_blueprint(LoginBP)
app.register_blueprint(UserBP)
app.register_blueprint(SongBP)
app.register_blueprint(ArtistBP)

app.config['SECRET_KEY'] = 'uber_secret'
login_manager = LoginManager()
login_manager.init_app(app)


@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)


class User(UserMixin):
    def __init__(self, id, email, nome, cognome, nickname, bio, data_nascita, password, ruolo, premium):
        self.id = id
        self.email = email
        self.nome = nome
        self.cognome = cognome
        self.nickname = nickname
        self.bio = bio
        self.data_nascita = data_nascita
        self.password = password
        self.ruolo = ruolo
        self.premium = premium

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)


def get_user_by_email(email):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM unive_music.utenti WHERE email = %s', email)
    user = rs.fetchone()
    conn.close()
    return User(user.id_utente, user.email, user.nome, user.cognome, user.nickname, user.bio, user.data_nascita,
                user.password, user.ruolo, user.premium)


def result_proxy_to_list_of_dict(query_result):
    d, a = {}, []
    for row_proxy in query_result:
        for key, value in row_proxy.items():
            d = {**d, **{key: value}}
        a.append(d)
    return a


def seconds_to_minutes(input_second):
    minutes = input_second / 60
    seconds = input_second % 60
    return "" + minutes + ":" + seconds


def minutes_to_seconds(minutes):
    return minutes*60


@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM unive_music.utenti WHERE id_utente = %s', user_id)
    user = rs.fetchone()
    conn.close()
    return User(user.id_utente, user.email, user.nome, user.cognome, user.nickname, user.bio, user.data_nascita,
                user.password, user.ruolo, user.premium)


@app.route('/')
def home():
    conn = engine.connect()
    rs = conn.execute(' SELECT canzoni.id_canzone, canzoni.titolo, canzoni.rilascio, canzoni.colore, utenti.nickname '
                      ' FROM unive_music.canzoni JOIN unive_music.utenti ON canzoni.id_artista = utenti.id_utente')
    all_songs = rs.fetchall()
    all_songs = result_proxy_to_list_of_dict(all_songs)

    for song in all_songs:
        rs = conn.execute('SELECT attributo_canzone.id_tag FROM unive_music.attributo_canzone WHERE '
                          'attributo_canzone.id_canzone = %s', song['id_canzone'])
        tags = rs.fetchall()
        if tags:
            song['Tag_1'] = tags[0][0]
            song['Tag_2'] = tags[1][0]

    rs = conn.execute('SELECT canzoni.id_canzone, canzoni.titolo, canzoni.rilascio, canzoni.colore, utenti.nickname '
                      'FROM unive_music.canzoni JOIN unive_music.utenti ON canzoni.id_artista = utenti.id_utente '
                      'ORDER BY Canzoni.Rilascio DESC LIMIT 5')
    latest_songs = rs.fetchall()
    latest_songs = result_proxy_to_list_of_dict(latest_songs)

    for song in latest_songs:
        rs = conn.execute('SELECT attributo_canzone.id_tag FROM unive_music.attributo_canzone WHERE '
                          'attributo_canzone.id_canzone = %s', song['id_canzone'])
        tags = rs.fetchall()
        if tags:
            song['Tag_1'] = tags[0][0]
            song['Tag_2'] = tags[1][0]

    rs = conn.execute('SELECT canzoni.id_canzone, canzoni.titolo, canzoni.rilascio, canzoni.colore, utenti.nickname '
                      'FROM unive_music.canzoni JOIN unive_music.utenti ON canzoni.id_artista = utenti.id_utente '
                      'NATURAL JOIN unive_music.statistiche_canzoni NATURAL JOIN unive_music.statistiche ORDER BY '
                      'statistiche.n_riproduzioni_totali DESC LIMIT 5')
    most_played_songs = rs.fetchall()
    most_played_songs = result_proxy_to_list_of_dict(most_played_songs)

    for song in most_played_songs:
        rs = conn.execute('SELECT attributo_canzone.id_tag FROM unive_music.attributo_canzone WHERE '
                          'attributo_canzone.id_canzone = %s', song['id_canzone'])
        tags = rs.fetchall()
        if tags:
            song['Tag_1'] = tags[0][0]
            song['Tag_2'] = tags[1][0]

    conn.close()
    return render_template("Index.html", all_songs=all_songs, latest_songs=latest_songs,
                           most_played_songs=most_played_songs)


@app.route('/reset')
@login_required
def reset():
    conn = engine.connect()
    conn.execute('UPDATE unive_music.statistiche SET n_riproduzioni_settimanali = %s', 0)
    conn.close()
    return redirect(url_for('home'))
