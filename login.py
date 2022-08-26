from flask import *
from sqlalchemy import *
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
import main
from datetime import date

LoginBP = Blueprint('LoginBP', __name__)
engine = create_engine('postgresql://postgres:BDProject2022@localhost:5432/BDProject')


@LoginBP.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)


@LoginBP.route('/accedi')
def accedi():
    return render_template("Accedi.html", message='')


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
                return render_template('Accedi.html', message='E-mail o Password errati')
        else:
            return render_template('Accedi.html', message='E-mail o Password errati')
    else:
        return redirect(url_for('LoginBP.accedi'))


@LoginBP.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# redirect alla pagina di sign in
@LoginBP.route('/registrati')
def registrati():
    return render_template("Registrati.html")


# pagina di registrazione
@LoginBP.route('/sing_in', methods=['GET', 'POST'])
def sing_in():
    if request.method == 'POST':
        conn = engine.connect()
        age = date.today().year - date.fromisoformat(request.form["DataNascita"]).year
        if age >= 13:
            if request.form['password'] == request.form['rip_password']:
                pwhash = generate_password_hash(request.form["password"], method='pbkdf2:sha256:260000', salt_length=16)
                data = (request.form["email"], request.form["nome"], request.form["cognome"], request.form["nickname"],
                        request.form["bio"], request.form["DataNascita"], pwhash, "1", "false")
                conn.execute('INSERT INTO unive_music.utenti (email, nome, cognome, nickname, bio, data_nascita, '
                             'password, ruolo, premium) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)', data)
                conn.close()
                return redirect(url_for('LoginBP.accedi'))
            else:
                conn.close()
                return render_template("Registrati.html", message='Le password non coincidono')
        else:
            conn.close()
            return render_template("Registrati.html", message='Sei troppo piccolo')
    else:
        return redirect(url_for('LoginBP.registrati'))
