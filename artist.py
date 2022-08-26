from flask_login import current_user
from flask import *
from sqlalchemy import *
from flask_login import login_required
import main
from datetime import date

ArtistBP = Blueprint('ArtistBP', __name__)
engine = create_engine('postgresql://postgres:BDProject2022@localhost:5432/BDProject')


@ArtistBP.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)


@ArtistBP.route('/new_album', methods=['GET', 'POST'])
@login_required
def new_album():
    if request.method == 'POST':
        conn = engine.connect()
        data = (request.form["Titolo"], request.form["Rilascio"], request.form["Colore"], "0", current_user.id)
        conn.execute('INSERT INTO unive_music.album (titolo, rilascio, colore, n_canzoni, id_artista) VALUES (%s,%s,'
                     '%s,%s,%s)', data)
        rs = conn.execute('SELECT * FROM unive_music.album WHERE album.id_artista = %s AND album.titolo = %s AND '
                          'album.rilascio = %s', [current_user.id, request.form["Titolo"], request.form["Rilascio"]])
        id_album = rs.fetchone()
        rs = conn.execute('SELECT tag.tag FROM unive_music.tag WHERE tag.tag = %s', request.form['Tag_1'])
        tag = rs.fetchone()

        if not tag:
            conn.execute('INSERT INTO unive_music.tag (tag) VALUES (%s)', request.form['Tag_1'])

        conn.execute('INSERT INTO unive_music.attributo_album (id_tag, id_album) VALUES (%s, %s)',
                     [request.form['Tag_1'], id_album[0]])
        rs = conn.execute('SELECT tag.tag FROM unive_music.tag WHERE tag.tag = %s', request.form['Tag_2'])
        tag = rs.fetchone()

        if not tag:
            conn.execute('INSERT INTO unive_music.tag (tag) VALUES (%s)', request.form['Tag_2'])

        conn.execute('INSERT INTO unive_music.attributo_album (id_tag, id_album) VALUES (%s, %s)',
                     [request.form['Tag_2'], id_album[0]])
        rs = conn.execute('SELECT tag.tag FROM unive_music.tag WHERE tag.tag = %s', request.form['CasaDiscografica'])
        tag = rs.fetchone()

        if not tag:
            conn.execute('INSERT INTO unive_music.tag (tag) VALUES (%s)', request.form['CasaDiscografica'])

        conn.execute('INSERT INTO unive_music.attributo_album (id_tag, id_album) VALUES (%s,%s)',
                     [request.form['CasaDiscografica'], id_album[0]])
        conn.close()
        return redirect(url_for('ArtistBP.get_albums'))
    else:
        return render_template("NuovoAlbum.html")


@ArtistBP.route('/nuova_canzone/<id_album>')
@login_required
def new_song_data(id_album):
    return render_template("NuovaCanzone.html", id_album=id_album)


@ArtistBP.route('/new_song/<id_album>', methods=['GET', 'POST'])
@login_required
def new_song(id_album):
    if request.method == 'POST':
        conn = engine.connect()
        durata = main.minutes_to_seconds(request.form['Durata_min']) + request.form['Durata_sec']
        data = (request.form["Titolo"], request.form["Rilascio"], durata, request.form["Colore"], current_user.id)
        conn.execute('INSERT INTO unive_music.canzoni (titolo, rilascio, durata, colore, id_artista) VALUES (%s,%s,'
                     '%s,%s,%s)', data)
        rs = conn.execute('SELECT canzoni.id_canzone FROM unive_music.canzoni WHERE canzoni.id_artista = %s AND '
                          'canzoni.titolo = %s AND canzoni.rilascio = %s',
                          [current_user.id, request.form["Titolo"], request.form["Rilascio"]])
        id_canzone = rs.fetchone()
        data = [id_album, id_canzone[0]]
        conn.execute(' INSERT INTO unive_music.contenuto (id_album, id_canzone) VALUES (%s,%s)', data)
        conn.execute('INSERT INTO unive_music.statistiche (_13_19, _20_29, _30_39, _40_49, _50_65, _65piu, '
                     'n_riproduzioni_totali, n_riproduzioni_settimanali) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                     [0, 0, 0, 0, 0, 0, 0, 0])
        rs = conn.execute('SELECT MAX(statistiche.id_statistica) FROM unive_music.statistiche')
        id_statistica = rs.fetchone()
        conn.execute('INSERT INTO unive_music.statistiche_canzoni (id_statistica, id_canzone) VALUES (%s,%s)',
                     [id_statistica[0], id_canzone[0]])
        rs = conn.execute('SELECT tag.tag FROM unive_music.tag WHERE tag.tag = %s', request.form['Tag_1'])
        tag = rs.fetchone()

        if not tag:
            conn.execute('INSERT INTO unive_music.tag (tag) VALUES (%s)', request.form['Tag_1'])

        conn.execute('INSERT INTO unive_music.attributo_canzone (id_tag, id_canzone) VALUES (%s,%s)',
                     [request.form['Tag_1'], id_canzone[0]])
        rs = conn.execute('SELECT tag.tag FROM unive_music.tag WHERE tag.tag = %s', request.form['Tag_2'])
        tag = rs.fetchone()

        if not tag:
            conn.execute('INSERT INTO unive_music.tag (tag) VALUES (%s)', request.form['Tag_2'])

        conn.execute('INSERT INTO unive_music.attributo_canzone (id_tag, id_canzone) VALUES (%s,%s)',
                     [request.form['Tag_2'], id_canzone[0]])
        rs = conn.execute('SELECT tag.tag FROM unive_music.tag WHERE tag.tag = %s', request.form['Lingua'])
        tag = rs.fetchone()

        if not tag:
            conn.execute('INSERT INTO unive_music.tag (tag) VALUES (%s)', request.form['Lingua'])

        conn.execute('INSERT INTO unive_music.attributo_canzone (id_tag, id_canzone) VALUES (%s,%s)',
                     [request.form['Lingua'], id_canzone[0]])
        conn.close()
        return redirect(url_for('ArtistBP.get_albums'))
    else:
        return render_template("NuovaCanzone.html")


@ArtistBP.route('/produzioni')
@login_required
def get_albums():
    conn = engine.connect()
    rs = conn.execute('SELECT album.id_album, album.titolo, album.rilascio FROM unive_music.album WHERE '
                      'album.id_artista = %s', current_user.id)
    albums = rs.fetchall()
    rs = conn.execute('SELECT contenuto.id_album, canzoni.titolo, canzoni.rilascio, canzoni.durata, canzoni.colore, '
                      'canzoni.id_canzone, utenti.nickname FROM unive_music.canzoni NATURAL JOIN '
                      'unive_music.contenuto  JOIN unive_music.utenti ON canzoni.id_artista = utenti.id_utente WHERE '
                      'contenuto.id_album IN (SELECT album.id_album FROM unive_music.album WHERE album.id_artista = '
                      '%s) GROUP BY contenuto.id_album, canzoni.titolo, canzoni.rilascio, canzoni.durata, '
                      'canzoni.colore, canzoni.id_canzone, utenti.nickname', current_user.id)
    songs = rs.fetchall()
    songs = main.result_proxy_to_list_of_dict(songs)

    for song in songs:
        rs = conn.execute('SELECT attributo_canzone.id_tag FROM unive_music.attributo_canzone WHERE '
                          'attributo_canzone.id_canzone = %s', song['id_canzone'])
        tags = rs.fetchall()
        if tags:
            song['Tag_1'] = tags[0][0]
            song['Tag_2'] = tags[1][0]

    albums_songs = []

    for album in albums:
        album_s = []
        for song in songs:
            if song['id_album'] == album[0]:
                album_s.append(song)
        albums_songs.append(album_s)

    resp = make_response(render_template("Produzioni.html", user=current_user, albums=albums,
                                         albums_songs=albums_songs))
    conn.close()
    return resp


@ArtistBP.route('/album/<id_album>')
def get_album_data(id_album):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM unive_music.album JOIN unive_music.utenti ON album.id_artista = utenti.id_utente '
                      'WHERE album.id_album = %s', id_album)
    album_data = rs.fetchone()
    rs = conn.execute('SELECT * FROM unive_music.canzoni NATURAL JOIN unive_music.contenuto JOIN unive_music.utenti '
                      'ON canzoni.id_artista = utenti.id_utente WHERE contenuto.id_album = %s', id_album) 
    song_album = rs.fetchall()
    song_album = main.result_proxy_to_list_of_dict(song_album)

    for song in song_album:
        rs = conn.execute('SELECT attributo_canzone.id_tag FROM unive_music.attributo_canzone WHERE '
                          'attributo_canzone.id_canzone = %s', song['id_canzone'])
        tmp = rs.fetchall()
        if tmp:
            song['Tag_1'] = tmp[0][0]
            song['Tag_2'] = tmp[1][0]

    rs = conn.execute('SELECT attributo_album.id_tag FROM unive_music.attributo_album WHERE attributo_album.id_album '
                      '= %s', id_album)
    tag = rs.fetchall()
    if len(tag) > 1:
        tags = {'Tag_1': tag[0][0], 'Tag_2': tag[1][0]}
    else:
        tags = {'Tag_1': tag[0][0]}
    resp = make_response(render_template("Album.html", album=album_data, song_album=song_album, tags=tags))
    conn.close()
    return resp


@ArtistBP.route('/del_album/<id_album>')
@login_required
def del_album(id_album):
    conn = engine.connect()
    # Cancello e lascio i tag. Non sarebbe meglio controllare che non ci siano tag univoci di questo album
    # per non avere tuple in tag inutilizzate?
    conn.execute('DELETE FROM unive_music.attributo_album WHERE attributo_album.id_album = %s', id_album)

    rs = conn.execute('SELECT contenuto.id_canzone FROM unive_music.contenuto WHERE contenuto.id_album = %s', id_album)
    id_canzoni = rs.fetchall()

    for id_canzone in id_canzoni:
        for _ in id_canzone[0]:
            conn.execute('DELETE FROM unive_music.attributo_canzone WHERE id_canzone = %s', id_canzone)
            rs = conn.execute('SELECT statistiche.id_statistica FROM unive_music.statistiche NATURAL JOIN '
                              'unive_music.statistiche_canzoni WHERE statistiche_canzoni.id_canzone = %s', id_canzone)
            id_statistica = rs.fetchone()
            conn.execute('DELETE FROM unive_music.statistiche WHERE id_statistica = %s', id_statistica[0])
            conn.execute('DELETE FROM unive_music.statistiche_canzoni WHERE id_statistica = %s', id_statistica[0])

    conn.execute('DELETE FROM unive_music.canzoni WHERE id_canzone IN (SELECT contenuto.id_canzone FROM '
                 'unive_music.contenuto WHERE contenuto.id_album = %s)', id_album)
    conn.execute(' DELETE FROM unive_music.contenuto WHERE id_album = %s', id_album)
    conn.execute(' DELETE FROM unive_music.album WHERE id_album = %s', id_album)
    conn.close()
    return redirect(url_for('ArtistBP.get_albums'))


@ArtistBP.route('/album_stat/<id_album>')
@login_required
def album_stat(id_album):
    conn = engine.connect()
    rs = conn.execute('SELECT canzoni.id_canzone FROM unive_music.canzoni NATURAL JOIN unive_music.contenuto WHERE '
                      'contenuto.id_album = %s', id_album)
    id_canzoni = rs.fetchall()
    statistiche = {'Fascia1': 0, 'Fascia2': 0, 'Fascia3': 0, 'Fascia4': 0, 'Fascia5': 0, 'Fascia6': 0, 'Tot': 0,
                   'n_riproduzioni_totali': 0, 'n_riproduzioni_settimanali': 0}

    for id_canzone in id_canzoni:
        for value in id_canzone[0]:
            rs = conn.execute('SELECT * FROM unive_music.statistiche WHERE statistiche.id_statistica = ( SELECT '
                              'statistiche.id_statistica FROM unive_music.statistiche_canzoni NATURAL JOIN '
                              'unive_music.statistiche WHERE statistiche_canzoni.id_canzone = %s)', value)
            stat = rs.fetchone()
            tot = stat[1] + stat[2] + stat[3] + stat[4] + stat[5] + stat[6]
            statistiche = {'Fascia1': statistiche['Fascia1'] + stat[1], 'Fascia2': statistiche['Fascia2'] + stat[2],
                           'Fascia3': statistiche['Fascia3'] + stat[3], 'Fascia4': statistiche['Fascia4'] + stat[4],
                           'Fascia5': statistiche['Fascia5'] + stat[5], 'Fascia6': statistiche['Fascia6'] + stat[6],
                           'Tot': statistiche['Tot'] + tot,
                           'n_riproduzioni_totali': statistiche['n_riproduzioni_totali'] + stat[7],
                           'n_riproduzioni_settimanali': statistiche['n_riproduzioni_settimanali'] + stat[8]}

    rs = conn.execute('SELECT * FROM unive_music.album JOIN unive_music.utenti ON album.id_artista = utenti.id_utente '
                      'WHERE album.id_album = %s', id_album)
    album = rs.fetchone()
    rs = conn.execute('SELECT attributo_album.id_tag FROM unive_music.attributo_album WHERE attributo_album.id_album '
                      '= %s', id_album)
    tag = rs.fetchall()
    tags = {'Tag_1': tag[0][0], 'Tag_2': tag[1][0]}
    conn.close()
    return render_template("AlbumStatistics.html", stat=statistiche, album=album, tags=tags)


@ArtistBP.route('/become_artist')
@login_required
def become_artist():
    conn = engine.connect()
    conn.execute('UPDATE unive_music.utenti SET ruolo = %s WHERE id_utente = %s', 2, current_user.id)
    conn.execute('INSERT INTO unive_music.artisti (id_utente, debutto) VALUES (%s,%s)', current_user.id, date.today())
    conn.close()
    return redirect(url_for('ArtistBP.get_albums'))
