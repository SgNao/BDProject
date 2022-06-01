from flask import *
from sqlalchemy import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered
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

        print('1')

        if real_pwd is not None:
            print('2')
            # if request.form['pass'] == real_pwd['Password']:
            # if (check_password_hash(real_pwd, request.form['pass'])):
            if main.User.verify_password(real_pwd, request.form['pass']):
                print('3')
                user = main.get_user_by_email(request.form['user'])
                login_user(user)
                return redirect(url_for('home'))
            else:
                print('4')
                return redirect(url_for('LoginBP.Accedi'))
        else:
            print('5')
            return redirect(url_for('LoginBP.Accedi'))  # redirect(url_for('LoginBP.home'))
    else:
        print('6')
        return redirect(url_for('LoginBP.Accedi'))  # redirect(url_for('LoginBP.home'))


@LoginBP.route('/logout')
@login_required  # richiede autenticazione
def logout():
    logout_user()
    return redirect(url_for('LoginBP.home'))
