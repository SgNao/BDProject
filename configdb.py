from flask import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered
from sqlalchemy import *
import psycopg2

# da riempire con dati corretti per far partire con Postgres
def setupConnection():
    conn = psycopg2.connect(database="DBProject",
        host="localhost", #da mettere
        user="postgres", #da mettere
        password="db_pass", #da mettere
        port="5050") #da mettere
    return conn

# se si è fatto il setup della connessione, sostituire con true
def isSetupDone():
    return false

def createConnection():
    if (isSetupDone()):
        return setupConnection()
    else:
        engine = create_engine('sqlite:///database.db', echo = True)
        conn = engine.connect()
        return conn

def myExecute(conn, ins, list):
    if (isSetupDone()):
        conn.execute(ins, list) # da controllare cosa serve su postgress
    else:
        conn.execute(ins, list)

def myClose(conn):
    conn.close()