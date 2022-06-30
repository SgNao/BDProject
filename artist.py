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
        data = (request.form["Titolo"], request.form["Rilascio"], request.form["Colore"], "0", current_user.id)
        data2 = request.form["CasaDiscografica"]
        # Serve sanitizzare l'input
        rs = conn.execute('INSERT INTO album (titolo, rilascio, colore, n_canzoni, id_artista) VALUES (?,?,?,?,?)', data)
        # Check se casa discografica è presente
        # Inserimento in tag se non è presente
        # recupero id album appena inserito con key (titolo, rilascio, idartista)
        # Inserimento in attributoAlbum in ogni caso
        conn.close()
        return redirect(url_for('ArtistBP.get_albums'))
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
        data = (request.form["Titolo"], request.form["Rilascio"], request.form["Durata"], request.form["Colore"], current_user.id)
        data2 = request.form["Lingua"]
        #sanitizzare input
        rs = conn.execute('INSERT INTO canzoni (titolo, rilascio, durata, colore, id_artista) VALUES (?,?,?,?,?)', data)
        # fare insert della lingua con data2
        rs = conn.execute('SELECT * FROM canzoni WHERE canzoni.id_artista = ?  AND canzoni.titolo = ? AND canzoni.rilascio = ?', [current_user.id],
            request.form["Titolo"], request.form["Rilascio"])
        IdCanzone = rs.fetchone()
        data = [IdAlbum, IdCanzone[0]]
        rs = conn.execute('INSERT INTO contenuto (id_album, id_canzone) VALUES (?,?)', data)
        # Check se lingua è presente
        # Inserimento in tag se non è presente
        # recupero id canzone appena inserita con key (titolo, rilascio, id_artista)
        # Inserimento in attributoCanzone in ogni caso
        conn.close()
        return redirect(url_for('ArtistBP.get_albums'))
    else:
         return render_template("NuovaCanzone.html")

@ArtistBP.route('/album_stat')
def Albumstat():
    return render_template("AlbumStatistics.html")

@ArtistBP.route('/Produzioni')
@login_required  # richiede autenticazione
def get_albums():
    conn = engine.connect()
    rs = conn.execute(' SELECT album.id_album, album.titolo, album.tilascio'
                      ' FROM album'
                      ' WHERE album.id_artista = ?', current_user.id)
    albums = rs.fetchall()
    rs = conn.execute(' SELECT contenuto.id_album, canzoni.titolo, canzoni.rilascio, canzoni.durata, canzoni.colore, canzoni.id_canzone'  
                      ' FROM canzoni NATURAL JOIN contenuto'
                      ' WHERE contenuto.id_album IN (SELECT album.id_album FROM album'
                      ' WHERE album.id_artista = ?)'
                      ' GROUP BY contenuto.id_album, canzoni.titolo, canzoni.rilascio, canzoni.durata, canzoni.colore', current_user.id)
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