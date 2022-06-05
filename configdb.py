from flask import *
from sqlalchemy import *
import psycopg2

# da riempire con dati corretti per far partire
def setupConnection():
    conn = psycopg2.connect(database="DBProject",
                            host="db_host", #da mettere
                            user="postgres", #da mettere
                            password="db_pass", #da mettere
                            port="5050") #da mettere
    return conn


def setupDone():
    return false # se si è fatto il setup della connessione, sostituire con true