from flask import *
from sqlalchemy import *
#from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered

SongBP = Blueprint('SongBP', __name__)
engine = create_engine('sqlite:///database.db', echo=True)

# IMPORTANTE NON TOGLIERE
@SongBP.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)

@SongBP.route('/tosongs')
def tosongs():
    return redirect(url_for('Songs'))


@SongBP.route('/songs')
def songs():
    conn = engine.connect()
    songlist = conn.execute('SELECT * FROM Canzoni')
    resp = make_response(render_template("Songs.html", songs=songlist))
    conn.close()
    return resp
