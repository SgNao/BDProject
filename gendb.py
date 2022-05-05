from sqlalchemy import *

engine = create_engine('sqlite:///database.db', echo = True)
metadata = MetaData()

users = Table('Users', metadata,
            Column('id', Integer, primary_key=True),
            Column('email', String),
            Column('pwd', String)
        )

metadata.create_all(engine)

conn = engine.connect()
ins = "INSERT INTO Users VALUES (?,?,?)"
conn.execute(ins, ['1', 'alice@gmail.com', 'love'])
conn.execute(ins, ['2', 'bob@gmail.com', 'milk'])

user_list = conn.execute("SELECT * FROM Users")
for u in user_list:
    print(u)