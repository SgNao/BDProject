from sqlalchemy import *
import psycopg2


def select_db():
    # return true se si vuole utilizzare postgres
    # return false se si vuole utilizzare sqlite 
    return true


# In questo file Python si possono settare le varie informazioni per far funzionare un database di PostGre sulla
# propria macchina. Settare le seguenti cinque funzioni in modo che ritornino stringhe coerenti con i campi richiesti.
# Nelle funzioni saranno presenti anche le stringhe di configurazione della matricola 881455@stud.unive.it come esempio.


def get_database():
    # return "DBProject"
    return "BDProject"


def get_host():
    # return "localhost" 
    return "localhost"


def get_user():
    # return "postgres"
    return "postgres"


def get_password():
    # return "BDProject2022"
    return "BDProject2022"


def get_port():
    # return "5432"
    return "5432"


# inserire funzione che ritorna la connessione per alleggerire il codice in tutte gli file
# in questo modo posso avere anche la connessione giusta di base e poi itero sul cursore con postgres


def get_connection():
    if select_db() == true:
        conn = psycopg2.connect(
            database=get_database(),
            host=get_host(),
            user=get_user(),
            password=get_password(),
            port=get_port())
        return conn
    else:
        sqlite_engine = create_engine('sqlite:///database.db', echo=True)
        connection = sqlite_engine.connect()
        return connection
