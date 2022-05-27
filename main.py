from flask import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered
from sqlalchemy import *
import os.path
import sys
from Login import LoginBP

app = Flask(__name__)
app.register_blueprint(LoginBP)

'''
export FLASK_APP=Login.py
export FLASK_ENV=development
flask run

set FLASK_APP=Login.py
set FLASK_ENV=development
$env:FLASK_APP = "Login.py"
flask run
'''
'''
# Controllo che esista database e, in caso non esistesse, lo genero
try:
    os.path.realpath('database.bd', strict=True)
except:
    # Il database manca, quindi provo a generarlo. Controllo che ci sia il file csv per farlo
    # Se non c'è il file csv, mando una eccezione
    try:
        os.path.realpath('./songdb.csv', strict=True)
    except:
        raise Exception('Manca il file csv per generare il database')
    if(sys.version_info[0]<3):
        execfile('gendb.py')
        execfile('popdb.py')
    else:
        exec(open('gendb.py').read())
        exec(open('popdb.py').read())
'''