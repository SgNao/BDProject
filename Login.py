from venv import create
from flask import *
from flask_login import *
from sqlalchemy import *

app = Flask(__name__)
engine = create_engine('sqlite:///database.db', echo=True)
app.config['SECRET_KEY'] = 'ubersecret'
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin): # costruttore di classe
    def __init__ (self, id, email, pwd): #active=True
        self.id = id
        self.email = email
        self.pwd = pwd
        #self.active = active

def get_user_by_email(email):
    conn = engine.connect ()
    rs = conn.execute('SELECT * FROM Users WHERE email = ?', email )
    user = rs.fetchone()
    conn.close()
    return User(user.id, user.email, user.pwd)


@login_manager.user_loader
def load_user (user_id):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM Users WHERE id = ?', user_id)
    user = rs.fetchone ()
    conn.close()
    return User(user.id, user.email, user.pwd)

@app.route ('/')
def home ():
    # current_user identifica l’utente attuale utente anonimo prima dell’autenticazione
    if current_user.is_authenticated :
        return redirect(url_for('private'))
    return render_template("base.html")

@app.route('/login', methods =['GET','POST'])
def login():
    if request.method == 'POST':
        conn = engine.connect ()
        rs = conn.execute('SELECT pwd FROM Users WHERE email = ?', [request.form['user']])
        real_pwd = rs.fetchone ()
        conn.close ()

        if ( real_pwd is not None ):
            if request.form['pass'] == real_pwd['pwd']:
                user = get_user_by_email(request.form['user'])
                login_user(user)
                return redirect (url_for('private'))
            else :
                return redirect (url_for ('home'))
        else :
            return redirect (url_for ('home'))
    else :
        return redirect ( url_for ('home'))

@app.route ('/private')
@login_required # richiede autenticazione
def private():
    conn = engine.connect ()
    users = conn.execute('SELECT * FROM Users')
    resp = make_response(render_template("private.html ", users = users))
    conn.close()
    return resp

@app.route ('/logout')
@login_required # richiede autenticazione
def logout():
    logout_user()
    return redirect (url_for('home'))