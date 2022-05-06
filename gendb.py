from sqlalchemy import *

engine = create_engine('sqlite:///database.db', echo = True)
metadata = MetaData()

users = Table('Utenti', metadata,
            Column('Email', String, primary_key=True, index=True), #index singoli. Per index multicolonna serve crearli dopo l'ultima colonna
            Column('Nome', String, nullable=False), #mettiamo un limite alla grandezza?
            Column('Cognome', String, nullable=False), #mettiamo un limite alla grandezza?
            Column('Nickname', String(24), nullable=True, unique=True), #mettiamo un limite alla grandezza? Unique nullable?
            Column('Data_Nascita', Date, nullable=False),
            Column('Password', String(16), nullable=False) #mettiamo un limite alla grandezza?
        )

artist = Table('Artisti', metadata,
            Column('Id_Utente', String, ForeignKey("Utenti.Email", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
            Column('Bio', String(160)), #mettiamo un limite alla grandezza?
            Column('Debutto', Date) #trigger per la prima canzone caricata?
        )

metadata.create_all(engine)

conn = engine.connect()
ins = "INSERT INTO Users VALUES (?,?,?)"
conn.execute(ins, ['1', 'alice@gmail.com', 'love'])
conn.execute(ins, ['2', 'bob@gmail.com', 'milk'])

user_list = conn.execute("SELECT * FROM Users")
for u in user_list:
    print(u)



"""
users = Table('Utenti', metadata,
            Column('', , primary_key=True),
            Column('', ),
            Column('', ),
            Column('', ),
            Column('', ),
            Column('', )
        )
"""