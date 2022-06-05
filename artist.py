from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered
from flask import *
from sqlalchemy import *
from flask_login import login_required

ArtistBP = Blueprint('ArtistBP', __name__)
engine = create_engine('sqlite:///database.db', echo=True)

# IMPORTANTE NON TOGLIERE
@ArtistBP.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)

@ArtistBP.route('/new_album', methods=['GET', 'POST'])
@login_required 
def NewAlbum():
    if request.method == 'POST':
        conn = engine.connect()
        data = (request.form["Titolo"], request.form["Rilascio"], request.form["Colore"], "0", request.form["CasaDiscografica"], current_user.id)
        rs = conn.execute('INSERT INTO Album (Titolo, Rilascio, Colore, NCanzoni, CasaDiscografica,IdArtista) VALUES (?,?,?,?,?,?)', data)
        conn.close()
        return redirect(url_for('Produzioni'))
    else:
        return render_template("NuovoAlbum.html")

@ArtistBP.route('/Nuova_Canzone/<IdAlbum>')
@login_required  # richiede autenticazione
def NewSongData(IdAlbum):
    print(IdAlbum)
    return render_template("NuovaCanzone.html", IdAlbum=IdAlbum)

@ArtistBP.route('/new_song/<IdAlbum>', methods=['GET', 'POST'])
def NewSong(IdAlbum):
    print(IdAlbum)
    if request.method == 'POST':
        conn = engine.connect()
        data = (request.form["Titolo"], request.form["Rilascio"], request.form["Durata"], request.form["Colore"], request.form["Lingua"], current_user.id)
        rs = conn.execute('INSERT INTO Canzoni (Titolo, Rilascio, Durata, Colore, Lingua, IdArtista) VALUES (?,?,?,?,?,?)', data)
        #Sottile problema - dopo aver inserito una nuova canzone, il DB genera IdCanzone automaticamente.  
        #Questo è l'unico modo che ci è venuto in mente per recuperarlo 
        rs = conn.execute('SELECT MAX(Canzoni.IdCanzone) FROM Canzoni WHERE Canzoni.IdArtista = ? ', [current_user.id])
        IdCanzone = rs.fetchone()
        data = [IdAlbum, IdCanzone[0]]
        rs = conn.execute('INSERT INTO Contenuto (IdAlbum, IdCanzone) VALUES (?,?)', data)
        conn.close()
        return redirect(url_for('get_albums'))
    else:
         return render_template("NuovaCanzone.html")

@ArtistBP.route('/album_stat')
def Albumstat():
    return render_template("AlbumStatistics.html")

@ArtistBP.route('/Produzioni')
@login_required  # richiede autenticazione
def get_albums():
    conn = engine.connect()
    rs = conn.execute(' SELECT Album.IdAlbum, Album.Titolo, Album.Rilascio, Album.CasaDiscografica'
                      ' FROM Album'
                      ' WHERE Album.IdArtista = ?', current_user.id)
    albums = rs.fetchall()
    rs = conn.execute(' SELECT Contenuto.IdAlbum, Canzoni.Titolo, Canzoni.Rilascio, Canzoni.Durata, Canzoni.Colore'  
                      ' FROM Canzoni NATURAL JOIN Contenuto'
                      ' WHERE Contenuto.IdAlbum IN (SELECT Album.IdAlbum FROM Album'
                      ' WHERE Album.IdArtista = ?)'
                      ' GROUP BY Contenuto.IdAlbum, Canzoni.Titolo, Canzoni.Rilascio, Canzoni.Durata, Canzoni.Colore', current_user.id)
    songs = rs.fetchall()
    albums_songs = []
    for album in albums:
        album_s = []
        for song in songs:
            if song.IdAlbum == album.IdAlbum:
                album_s.append(song)
        albums_songs.append(album_s)
    print(albums_songs)
    resp = make_response(render_template("Produzioni.html", user=current_user, albums=albums, albums_songs=albums_songs))
    conn.close()
    return resp

@ArtistBP.route('/album')
def get_album_data():
    conn = engine.connect()
    #songdata = conn.execute('SELECT Titolo, Durata, Anno, Genere FROM Canzoni')
    Albumdata = {'Titolo':'Appetite for Destruction','Anno': 1987, 'Casa_Discografica': 'Geffen Records'}
    songAlbum = [{'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"},
                 {'Titolo': "Sweet Child O' Mine", 'Anno': 1987, 'Tag': "#Rock and Roll"}] 
    resp = make_response(render_template("Album.html", album=Albumdata, songAlbum=songAlbum))
    conn.close()
    return resp