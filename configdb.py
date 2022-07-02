from flask import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered
from sqlalchemy import *
#import psycopg2

def selectDB():
    return true

# In questo file Python si possono settare le varie informazioni per far funzionare un database di PostGre sulla propria macchina.
# Settare le seguenti 5 funzioni in modo che ritornino stringhe coerenti con i campi richiesti.
# Nelle funzioni saranno presenti anche le stringhe di configurazione dello studente Massimiliano Zuin come esempio.

def getDatabase():
    # return "DBProject"
    return "BDProject"

def getHost():
    # return "localhost" 
    return "localhost"

def getUser():
    # return "postgres"
    return "postgres"

def getPassword():
    # return "BDProject2022"
    return "BDProject2022"

def getPort():
    # return "5432"
    return "5432"


# inserire funzione che ritorna la connessione per alleggerire il codice in tutte gli file
# in questo modo posso avere anche la connessione giusta di base e poi itero sul cursone con postgre