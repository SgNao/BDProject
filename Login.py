from flask import *
from sqlalchemy import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
import main


LoginBP = Blueprint('LoginBP', __name__)
engine = create_engine('sqlite:///database.db', echo=True)

# IMPORTANTE NON TOGLIERE
@LoginBP.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)


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


@LoginBP.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@LoginBP.route('/Registrati')
def Registrati():
    return render_template("Registrati.html")

@LoginBP.route('/singin', methods=['GET', 'POST'])
def SingIn():
    if request.method == 'POST':
        conn = engine.connect()
        pwhash = generate_password_hash(request.form["password"], method='pbkdf2:sha256:260000', salt_length=16)
        data = (request.form["email"], request.form["nome"], request.form["cognome"], request.form["nickname"], request.form["bio"], request.form["DataNascita"], pwhash, "1")
        rs = conn.execute('INSERT INTO Utenti (Email, Nome, Cognome, Nickname, Bio, DataNascita, Password, Ruolo)'
                          ' VALUES (?,?,?,?,?,?,?,?)', data)
        
        conn.close()
        return redirect(url_for('LoginBP.Accedi'))
    else:
        return redirect(url_for('LoginBP.Registrati'))