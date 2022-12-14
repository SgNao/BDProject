from flask import *
from sqlalchemy import *
from flask_login import current_user
import main

SongBP = Blueprint('SongBP', __name__)
engine = create_engine('postgresql://postgres:BDProject2022@localhost:5432/BDProject')


@SongBP.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)


@SongBP.route('/canzone_statistiche/<id_canzone>')
def canzone_statistiche(id_canzone):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM unive_music.statistiche WHERE statistiche.id_statistica = (SELECT '
                      'statistiche.id_statistica FROM unive_music.statistiche_canzoni NATURAL JOIN '
                      'unive_music.statistiche WHERE statistiche_canzoni.id_canzone = %s)', id_canzone)
    stat = rs.fetchone()
    tot = stat[1] + stat[2] + stat[3] + stat[4] + stat[5] + stat[6]
    statistiche = {'Fascia1': stat[1], 'Fascia2': stat[2], 'Fascia3': stat[3], 'Fascia4': stat[4], 'Fascia5': stat[5],
                   'Fascia6': stat[6], 'Tot': tot, 'n_riproduzioni_totali': stat[7],
                   'n_riproduzioni_settimanali': stat[8]}
    rs = conn.execute('SELECT * FROM unive_music.canzoni JOIN unive_music.utenti ON canzoni.id_artista = '
                      'utenti.id_utente WHERE canzoni.id_canzone = %s', id_canzone) 
    song = rs.fetchone()
    song_duration = main.seconds_to_minutes(song['durata'])
    rs = conn.execute('SELECT attributo_canzone.id_tag FROM unive_music.attributo_canzone WHERE '
                      'attributo_canzone.id_canzone = %s', id_canzone)
    tag = rs.fetchall()
    tags = {'Tag_1': tag[0][0], 'Tag_2': tag[1][0]}
    conn.close()
    return render_template("SongStatistics.html", stat=statistiche, song=song, tags=tags, song_duration=song_duration,)


@SongBP.route('/canzone/<id_canzone>')
def canzone(id_canzone):
    conn = engine.connect()
    rs = conn.execute('SELECT statistiche.n_riproduzioni_totali, statistiche.n_riproduzioni_settimanali FROM '
                      'unive_music.statistiche NATURAL JOIN unive_music.statistiche_canzoni WHERE '
                      'statistiche_canzoni.id_canzone = %s', id_canzone)
    stat = rs.fetchone()
    conn.execute('UPDATE unive_music.statistiche SET n_riproduzioni_totali = %s, n_riproduzioni_settimanali = %s '
                 'WHERE id_statistica = (SELECT statistiche_canzoni.id_statistica FROM '
                 'unive_music.statistiche_canzoni WHERE statistiche_canzoni.id_canzone = %s)', stat[0] + 1,
                 stat[1] + 1, id_canzone)
    rs = conn.execute('SELECT * FROM unive_music.canzoni JOIN unive_music.utenti ON canzoni.id_artista = '
                      'utenti.id_utente WHERE canzoni.id_canzone = %s', id_canzone) 
    song_data = rs.fetchone()
    song_duration = main.seconds_to_minutes(song_data['durata'])
    rs = conn.execute('SELECT contenuto.id_album FROM unive_music.canzoni NATURAL JOIN unive_music.contenuto WHERE '
                      'canzoni.id_canzone = %s', id_canzone) 
    id_album = rs.fetchone()
    rs = conn.execute('SELECT * FROM unive_music.canzoni NATURAL JOIN unive_music.contenuto JOIN unive_music.utenti '
                      'ON canzoni.id_artista = utenti.id_utente WHERE contenuto.id_album = %s', id_album)
    song_album = rs.fetchall()
    song_album = main.result_proxy_to_list_of_dict(song_album)
    
    for song in song_album:
        rs = conn.execute('SELECT attributo_canzone.id_tag FROM unive_music.attributo_canzone WHERE '
                          'attributo_canzone.id_canzone = %s', song['id_canzone']) 
        tags = rs.fetchall()
        if tags:
            song['Tag_1'] = tags[0][0]
            song['Tag_2'] = tags[1][0]

    rs = conn.execute('SELECT * FROM unive_music.album WHERE id_album = %s', id_album)
    album = rs.fetchone()
    rs = conn.execute('SELECT attributo_canzone.id_tag FROM unive_music.attributo_canzone WHERE '
                      'attributo_canzone.id_canzone = %s', id_canzone)
    tag = rs.fetchall()
    tags = {'Tag_1': tag[0][0], 'Tag_2': tag[1][0]}

    if current_user.is_authenticated:
        rs = conn.execute('SELECT * FROM unive_music.playlist WHERE playlist.id_utente = %s AND playlist.id_playlist '
                          'NOT IN (SELECT raccolte.id_playlist FROM unive_music.raccolte NATURAL JOIN '
                          'unive_music.canzoni WHERE canzoni.id_canzone = %s) ORDER BY playlist.nome',
                          current_user.id, id_canzone)
        playlists = rs.fetchall()
        resp = make_response(
            render_template("Song.html", playlists=playlists, song=song_data, song_duration=song_duration,
                            song_album=song_album, album=album, tags=tags))
    else:
        resp = make_response(render_template("Song.html", song=song_data, song_duration=song_duration,
                                             song_album=song_album, album=album, tags=tags))
    conn.close()
    return resp
