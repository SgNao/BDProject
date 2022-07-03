from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask import *
from sqlalchemy import *
from flask_login import login_required
import main 
from datetime import date 

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
        rs = conn.execute('INSERT INTO album (titolo, rilascio, colore, n_canzoni, id_artista) VALUES (?,?,?,?,?)', data)
        
        rs = conn.execute('SELECT * FROM album WHERE album.id_artista = ? AND album.titolo = ? AND album.rilascio = ?', [current_user.id], request.form["Titolo"], request.form["Rilascio"])
        IdAlbum = rs.fetchone()

        rs = conn.execute('SELECT tag.tag FROM tag WHERE tag.tag = ?', request.form['Tag_1'])
        tag = rs.fetchone()
        if not tag:
            rs = conn.execute('INSERT INTO tag (tag) VALUES (?)',  request.form['Tag_1'])
        
        rs = conn.execute('INSERT INTO attributo_album (id_tag, id_album) VALUES (?,?)', [request.form['Tag_1'], IdAlbum[0]])

        rs = conn.execute('SELECT tag.tag FROM tag WHERE tag.tag = ?', request.form['Tag_2'])
        tag = rs.fetchone()
        if not tag:
            rs = conn.execute('INSERT INTO tag (tag) VALUES (?)', request.form['Tag_2'])

        rs = conn.execute('INSERT INTO attributo_album (id_tag, id_album) VALUES (?,?)', [request.form['Tag_2'], IdAlbum[0]])
        
        rs = conn.execute('SELECT tag.tag FROM tag WHERE tag.tag = ?', request.form['CasaDiscografica'])
        tag = rs.fetchone()
        if not tag:
            rs = conn.execute('INSERT INTO tag (tag) VALUES (?)', request.form['CasaDiscografica'])

        rs = conn.execute('INSERT INTO attributo_album (id_tag, id_album) VALUES (?,?)', [request.form['CasaDiscografica'], IdAlbum[0]])

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
@login_required
def NewSong(IdAlbum):
    print(IdAlbum)
    if request.method == 'POST':
        conn = engine.connect()
        data = (request.form["Titolo"], request.form["Rilascio"], request.form["Durata"], request.form["Colore"], current_user.id)
        rs = conn.execute('INSERT INTO canzoni (titolo, rilascio, durata, colore, id_artista) VALUES (?,?,?,?,?,?)', data)
        rs = conn.execute('SELECT canzoni.id_canzone FROM canzoni WHERE canzoni.id_artista = ? AND canzoni.titolo = ? AND canzoni.rilascio = ?', [current_user.id], request.form["Titolo"], request.form["Rilascio"])
        IdCanzone = rs.fetchone()
        data = [IdAlbum, IdCanzone[0]]
        rs = conn.execute(' INSERT INTO contenuto (id_album, id_canzone) VALUES (?,?)', data)
        rs = conn.execute(' INSERT INTO statistiche (_13_19, _20_29, _30_39, _40_49, _50_65, _65piu , n_riproduzioni_totali, n_riproduzioni_settimanali)'
                          ' VALUES (?,?,?,?,?,?,?,?)', [0,0,0,0,0,0,0,0])
        rs = conn.execute('SELECT MAX(statistiche.id_statistica) FROM statistiche')
        IdStatistica = rs.fetchone()
        rs = conn.execute('INSERT INTO statistiche_canzoni (id_statistica, id_canzone) VALUES (?,?)', [IdStatistica[0], IdCanzone[0]])

        rs = conn.execute('SELECT tag.tag FROM tag WHERE tag.tag = ?', request.form['Tag_1'])
        tag = rs.fetchone()
        if not tag:
            rs = conn.execute('INSERT INTO tag (tag) VALUES (?)',  request.form['Tag_1'])
        
        rs = conn.execute('INSERT INTO attributo_canzone (id_tag, id_canzone) VALUES (?,?)', [request.form['Tag_1'], IdCanzone[0]])

        rs = conn.execute('SELECT tag.tag FROM tag WHERE tag.tag = ?', request.form['Tag_2'])
        tag = rs.fetchone()
        if not tag:
            rs = conn.execute('INSERT INTO tag (tag) VALUES (?)', request.form['Tag_2'])

        rs = conn.execute('INSERT INTO attributo_canzone (id_tag, id_canzone) VALUES (?,?)', [request.form['Tag_2'], IdCanzone[0]])
    
        rs = conn.execute('SELECT tag.tag FROM tag WHERE tag.tag = ?', request.form['Lingua'])
        tag = rs.fetchone()
        if not tag:
            rs = conn.execute('INSERT INTO tag (tag) VALUES (?)',  request.form['Lingua'])

        rs = conn.execute('INSERT INTO attributo_canzone (id_tag, id_canzone) VALUES (?,?)', [request.form['Lingua'], IdCanzone[0]])

        conn.close()
        return redirect(url_for('ArtistBP.get_albums'))
    else:
         return render_template("NuovaCanzone.html")

@ArtistBP.route('/Produzioni')
@login_required  # richiede autenticazione
def get_albums():
    conn = engine.connect()
    rs = conn.execute(' SELECT album.id_album, album.titolo, album.rilascio'
                      ' FROM album'
                      ' WHERE album.id_artista = ?', current_user.id)
    albums = rs.fetchall()
    rs = conn.execute(' SELECT contenuto.id_album, canzoni.titolo, canzoni.rilascio, canzoni.durata, canzoni.colore, canzoni.id_canzone, utenti.nickname'  
                      ' FROM canzoni NATURAL JOIN contenuto  JOIN utenti ON canzoni.id_artista = utenti.id_utente'
                      ' WHERE contenuto.id_album IN (SELECT album.id_album FROM album'
                      ' WHERE album.id_artista = ?)'
                      ' GROUP BY contenuto.id_album, canzoni.titolo, canzoni.rilascio, canzoni.durata, canzoni.colore', current_user.id)
    songs = rs.fetchall()

    songs = main.ResultProxy_To_ListOfDict(songs)
    for song in songs:
        rs = conn.execute('SELECT attributo_canzone.id_tag FROM attributo_canzone WHERE attributo_canzone.id_canzone = ?', song['id_canzone'])
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

    rs = conn.execute(' SELECT * FROM album JOIN utenti ON album.id_artista = utenti.id_utente WHERE album.id_album = ?', IdAlbum)
    Albumdata = rs.fetchone()
    rs = conn.execute(' SELECT * FROM canzoni NATURAL JOIN contenuto JOIN utenti ON canzoni.id_artista = utenti.id_utente'
                      ' WHERE contenuto.id_album = ?', IdAlbum)
    songAlbum = rs.fetchall()

    songAlbum = main.ResultProxy_To_ListOfDict(songAlbum)
    for song in songAlbum:
        rs = conn.execute('SELECT attributo_canzone.id_tag FROM attributo_canzone WHERE attributo_canzone.id_canzone = ?', song['id_canzone'])
        tags = rs.fetchall()
        if tags:
           song['Tag_1'] = tags[0][0]
           song['Tag_2'] = tags[1][0]

    rs = conn.execute('SELECT attributo_album.id_tag FROM attributo_album WHERE attributo_album.id_album = ?', IdAlbum)
    tags = rs.fetchall()
    Tags = {'Tag_1': tags[0][0], 'Tag_2': tags[1][0]}

    resp = make_response(render_template("Album.html", album=Albumdata, songAlbum=songAlbum, tags=Tags))
    conn.close()
    return resp

@ArtistBP.route('/DelAlbum/<IdAlbum>')
@login_required  # richiede autenticazione
def DelAlbum(IdAlbum):
    conn = engine.connect()

    rs = conn.execute('DELETE FROM attributo_album WHERE attributo_album.id_album = ?', IdAlbum)
    rs = conn.execute('SELECT contenuto.id_canzone FROM contenuto WHERE contenuto.id_album = ?', IdAlbum)
    IdCanzoni = rs.fetchall()
    for IdCanzone in IdCanzoni:
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in IdCanzone.items():
            rs = conn.execute('DELETE FROM attributo_canzone WHERE id_canzone = ?', IdCanzone)
            rs = conn.execute('SELECT statistiche.id_statistica FROM statistiche NATURAL JOIN statistiche_canzoni'
                              'WHERE statistiche_canzoni.id_canzone = ?', IdCanzone)
            IdStatistica = rs.fetchone()
            rs = conn.execute('DELETE FROM statistiche WHERE id_statistica = ?', IdStatistica[0])
            rs = conn.execute('DELETE FROM statistiche_canzoni WHERE id_statistica = ?', IdStatistica[0])

    rs = conn.execute(' DELETE FROM canzoni WHERE id_canzone IN'
                      ' (SELECT contenuto.id_canzone FROM contenuto WHERE contenuto.id_album = ?)', IdAlbum)
    rs = conn.execute(' DELETE FROM contenuto WHERE id_album = ?', IdAlbum)
    rs = conn.execute(' DELETE FROM album WHERE id_album = ?', IdAlbum)     

    conn.close()
    return redirect(url_for('ArtistBP.get_albums'))

@ArtistBP.route('/AlbumStat/<IdAlbum>')
@login_required
def AlbumStat(IdAlbum):
    conn = engine.connect()
    rs = conn.execute(' SELECT canzoni.id_canzone FROM canzoni NATURAL JOIN contenuto'
                      ' WHERE contenuto.id_album = ?', IdAlbum)
    IdCanzoni = rs.fetchall()

    statistiche = {'Fascia1':0, 'Fascia2': 0, 'Fascia3': 0, 'Fascia4': 0, 'Fascia5': 0, 'Fascia6': 0, 'Tot': 0, 'n_riproduzioni_totali': 0, 'n_riproduzioni_settimanali': 0}

    for IdCanzone in IdCanzoni:
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in IdCanzone.items():
            # build up the dictionary
            rs = conn.execute(' SELECT * FROM statistiche WHERE statistiche.id_statistica = ('
                              ' SELECT statistiche.id_statistica FROM statistiche_canzoni NATURAL JOIN statistiche' 
                              ' WHERE statistiche_canzoni.id_canzone = ?)', value)
            stat = rs.fetchone()
            Tot = stat[1]+stat[2]+stat[3]+stat[4]+stat[5]+stat[6]
            statistiche = {'Fascia1': statistiche['Fascia1']+stat[1],
                           'Fascia2': statistiche['Fascia2']+stat[2],
                           'Fascia3': statistiche['Fascia3']+stat[3],
                           'Fascia4': statistiche['Fascia4']+stat[4],
                           'Fascia5': statistiche['Fascia5']+stat[5],
                           'Fascia6': statistiche['Fascia6']+stat[6],
                           'Tot': statistiche['Tot']+Tot,
                           'n_riproduzioni_totali': statistiche['n_riproduzioni_totali']+stat[7], 
                           'n_riproduzioni_settimanali': statistiche['n_riproduzioni_settimanali']+stat[8]}
       
    
    rs = conn.execute(' SELECT * FROM album JOIN utenti ON album.id_artista = utenti.id_utente WHERE album.id_album = ?', IdAlbum)
    album = rs.fetchone()
    
    rs = conn.execute('SELECT attributo_album.id_tag FROM attributo_album WHERE attributo_album.id_album = ?', IdAlbum)
    tags = rs.fetchall()
    Tags = {'Tag_1': tags[0][0], 'Tag_2': tags[1][0]}

    conn.close()
    return render_template("AlbumStatistics.html", stat=statistiche, album=album, tags=Tags)

@ArtistBP.route('/BecomeArtist')
@login_required  # richiede autenticazione
def BecomeArtist():
    conn = engine.connect() 

    rs = conn.execute('UPDATE utenti SET ruolo = ? WHERE id_utente = ?', 2, current_user.id)
    rs = conn.execute('INSERT INTO artisti (id_utente, debutto) VALUES (?,?)', current_user.id, date.today())

    conn.close()
    return redirect(url_for('ArtistBP.get_albums'))