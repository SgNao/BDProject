from flask import *
from sqlalchemy import *
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
import main
from datetime import date

LoginBP = Blueprint('LoginBP', __name__)
engine = create_engine('postgresql://postgres:BDProject2022@localhost:5432/BDProject')


# IMPORTANTE NON TOGLIERE
@LoginBP.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)


# pagina di accesso
@LoginBP.route('/Accedi')
def Accedi():
    return render_template("Accedi.html")


# pagina di login
@LoginBP.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute('SELECT password FROM unive_music.utenti WHERE email = %s', [request.form['user']])
        real_pwd = rs.fetchone()
        conn.close()
        if real_pwd is not None:
            if check_password_hash(real_pwd[0], request.form['pass']):
                user = main.get_user_by_email(request.form['user'])
                login_user(user)
                return redirect(url_for('home'))
            else:
                return redirect(url_for('LoginBP.Accedi'))
        else:
            return redirect(url_for('LoginBP.Accedi'))
    else:
        return redirect(url_for('LoginBP.Accedi'))


# logout
@LoginBP.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# redirect alla pagina di sign in
@LoginBP.route('/Registrati')
def Registrati():
    return render_template("Registrati.html")


# pagina di registrazione
@LoginBP.route('/singin', methods=['GET', 'POST'])
def SingIn():
    if request.method == 'POST':
        print(3)
        conn = engine.connect()
        age = date.today().year - date.fromisoformat(request.form["DataNascita"]).year
        rs = conn.execute('SELECT * FROM unive_music.utenti WHERE utenti.email = %s', request.form['email'])
        user = rs.fetchone()
        rs = conn.execute('SELECT * FROM unive_music.utenti WHERE utenti.nickname = %s', request.form['nickname'])
        nickname = rs.fetchone()
        if age >= 13 and not user and not nickname:
            pwhash = generate_password_hash(request.form["password"], method='pbkdf2:sha256:260000', salt_length=16)
            # Query necessaria per bug di serial
            rs = conn.execute('SELECT MAX(utenti.id_utente) FROM unive_music.utenti')
            max = rs.fetchone()
            data = (max[0] + 1, request.form["email"], request.form["nome"], request.form["cognome"], request.form["nickname"],
                    request.form["bio"], request.form["DataNascita"], pwhash, "1")
            rs = conn.execute(
                'INSERT INTO unive_music.utenti (id_utente, email, nome, cognome, nickname, bio, data_nascita, password, ruolo)'
                ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)', data)

            conn.close()
            return redirect(url_for('LoginBP.Accedi'))
        else:
            conn.close()
            print(1)
            return redirect(url_for('LoginBP.Registrati'))
    else:
        print(2)
        return redirect(url_for('LoginBP.Registrati'))
