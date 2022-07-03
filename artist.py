from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask import *
from sqlalchemy import *
from flask_login import login_required
import main 

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
        
        rs = conn.execute('SELECT MAX(Album.IdAlbum) FROM Album WHERE Album.IdArtista = ? ', [current_user.id])
        IdAlbum = rs.fetchone()

        rs = conn.execute('SELECT Tag.Tag FROM Tag WHERE Tag.Tag = ?', request.form['Tag_1'])
        tag = rs.fetchone()
        if not tag:
            rs = conn.execute('INSERT INTO Tag (Tag) VALUES (?)',  request.form['Tag_1'])
        
        rs = conn.execute('INSERT INTO AttributoAlbum (IdTag, IdAlbum) VALUES (?,?)', [request.form['Tag_1'], IdAlbum[0]])

        rs = conn.execute('SELECT Tag.Tag FROM Tag WHERE Tag.Tag = ?', request.form['Tag_2'])
        tag = rs.fetchone()
        if not tag:
            rs = conn.execute('INSERT INTO Tag (Tag) VALUES (?)', request.form['Tag_2'])

        rs = conn.execute('INSERT INTO AttributoAlbum (IdTag, IdAlbum) VALUES (?,?)', [request.form['Tag_2'], IdAlbum[0]])
        
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
        data = (request.form["Titolo"], request.form["Rilascio"], request.form["Durata"], request.form["Colore"], request.form["Lingua"], current_user.id)
        rs = conn.execute('INSERT INTO Canzoni (Titolo, Rilascio, Durata, Colore, Lingua, IdArtista) VALUES (?,?,?,?,?,?)', data)
        rs = conn.execute('SELECT MAX(Canzoni.IdCanzone) FROM Canzoni WHERE Canzoni.IdArtista = ? ', [current_user.id])
        IdCanzone = rs.fetchone()
        data = [IdAlbum, IdCanzone[0]]
        rs = conn.execute(' INSERT INTO Contenuto (IdAlbum, IdCanzone) VALUES (?,?)', data)
        rs = conn.execute(' INSERT INTO Statistiche ("13-19", "20-29", "30-39", "40-49", "50-65", "65+", NRiproduzioniTotali, NRiproduzioniSettimanali)'
                          ' VALUES (?,?,?,?,?,?,?,?)', [0,0,0,0,0,0,0,0])
        rs = conn.execute('SELECT MAX(Statistiche.IdStatistica) FROM Statistiche')
        IdStatistica = rs.fetchone()
        rs = conn.execute('INSERT INTO StatCanzoni (IdStatistica, IdCanzone) VALUES (?,?)', [IdStatistica[0], IdCanzone[0]])

        rs = conn.execute('SELECT Tag.Tag FROM Tag WHERE Tag.Tag = ?', request.form['Tag_1'])
        tag = rs.fetchone()
        if not tag:
            rs = conn.execute('INSERT INTO Tag (Tag) VALUES (?)',  request.form['Tag_1'])
        
        rs = conn.execute('INSERT INTO AttributoCanzone (IdTag, IdCanzone) VALUES (?,?)', [request.form['Tag_1'], IdCanzone[0]])

        rs = conn.execute('SELECT Tag.Tag FROM Tag WHERE Tag.Tag = ?', request.form['Tag_2'])
        tag = rs.fetchone()
        if not tag:
            rs = conn.execute('INSERT INTO Tag (Tag) VALUES (?)', request.form['Tag_2'])

        rs = conn.execute('INSERT INTO AttributoCanzone (IdTag, IdCanzone) VALUES (?,?)', [request.form['Tag_2'], IdCanzone[0]])
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
    rs = conn.execute(' SELECT Album.IdAlbum, Album.Titolo, Album.Rilascio, Album.CasaDiscografica'
                      ' FROM Album'
                      ' WHERE Album.IdArtista = ?', current_user.id)
    albums = rs.fetchall()
    rs = conn.execute(' SELECT Contenuto.IdAlbum, Canzoni.Titolo, Canzoni.Rilascio, Canzoni.Durata, Canzoni.Colore, Canzoni.IdCanzone, Utenti.Nickname'  
                      ' FROM Canzoni NATURAL JOIN Contenuto  JOIN Utenti ON Canzoni.IdArtista = Utenti.IdUtenti'
                      ' WHERE Contenuto.IdAlbum IN (SELECT Album.IdAlbum FROM Album'
                      ' WHERE Album.IdArtista = ?)'
                      ' GROUP BY Contenuto.IdAlbum, Canzoni.Titolo, Canzoni.Rilascio, Canzoni.Durata, Canzoni.Colore', current_user.id)
    songs = rs.fetchall()

    songs = main.ResultProxy_To_ListOfDict(songs)
    for song in songs:
        rs = conn.execute('SELECT AttributoCanzone.IdTag FROM AttributoCanzone WHERE AttributoCanzone.IdCanzone = ?', song['IdCanzone'])
        tags = rs.fetchall()
        if tags:
           song['Tag_1'] = tags[0][0]
           song['Tag_2'] = tags[1][0]

    albums_songs = []
    for album in albums:
        album_s = []
        for song in songs:
            if song['IdAlbum'] == album.IdAlbum:
                album_s.append(song)
        albums_songs.append(album_s)
    print(albums_songs)
    resp = make_response(render_template("Produzioni.html", user=current_user, albums=albums, albums_songs=albums_songs))
    conn.close()
    return resp

@ArtistBP.route('/album/<IdAlbum>')
def get_album_data(IdAlbum):
    conn = engine.connect()

    rs = conn.execute(' SELECT * FROM Album JOIN Utenti ON Album.IdArtista = Utenti.IdUtenti WHERE Album.IdAlbum = ?', IdAlbum)
    Albumdata = rs.fetchone()
    rs = conn.execute(' SELECT * FROM Canzoni NATURAL JOIN Contenuto JOIN Utenti ON Canzoni.IdArtista = Utenti.IdUtenti'
                      ' WHERE Contenuto.IdAlbum = ?', IdAlbum)
    songAlbum = rs.fetchall()

    songAlbum = main.ResultProxy_To_ListOfDict(songAlbum)
    for song in songAlbum:
        rs = conn.execute('SELECT AttributoCanzone.IdTag FROM AttributoCanzone WHERE AttributoCanzone.IdCanzone = ?', song['IdCanzone'])
        tags = rs.fetchall()
        if tags:
           song['Tag_1'] = tags[0][0]
           song['Tag_2'] = tags[1][0]

    resp = make_response(render_template("Album.html", album=Albumdata, songAlbum=songAlbum))
    conn.close()
    return resp

@ArtistBP.route('/DelAlbum/<IdAlbum>')
@login_required  # richiede autenticazione
def DelAlbum(IdAlbum):
    conn = engine.connect()
    
    #Una canzone è contenuta in un solo album vero?
    rs = conn.execute(' DELETE FROM Canzoni WHERE IdCanzone IN'
                      ' (SELECT Contenuto.IdCanzone FROM Contenuto WHERE Contenuto.IdAlbum = ?)', IdAlbum)
    rs = conn.execute(' DELETE FROM Contenuto WHERE IdAlbum = ?', IdAlbum)
    rs = conn.execute(' DELETE FROM Album WHERE IdAlbum = ?', IdAlbum)     

    conn.close()
    return redirect(url_for('ArtistBP.get_albums'))
