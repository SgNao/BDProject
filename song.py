from flask import *
from sqlalchemy import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import main

SongBP = Blueprint('SongBP', __name__)
engine = create_engine('sqlite:///database.db', echo=True)

# IMPORTANTE NON TOGLIERE
@SongBP.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)

@SongBP.route('/SongStat/<IdCanzone>')
def SongStat(IdCanzone):
    conn = engine.connect()
    rs = conn.execute(' SELECT * FROM statistiche WHERE statistiche.id_statistica = ('
                      ' SELECT statistiche.id_statistica FROM statistiche_canzoni NATURAL JOIN statistiche' 
                      ' WHERE statistiche_canzoni.id_canzone = ?)', IdCanzone)
    stat = rs.fetchone()
    Tot = stat[1]+stat[2]+stat[3]+stat[4]+stat[5]+stat[6]
    statistiche = {'Fascia1': stat[1],'Fascia2': stat[2],'Fascia3': stat[3],'Fascia4': stat[4],'Fascia5': stat[5],'Fascia6': stat[6],'Tot': Tot,
                    'n_riproduzioni_totali': stat[7], 'n_riproduzioni_settimanali': stat[8]}
    rs = conn.execute(' SELECT * FROM canzoni JOIN utenti ON canzoni.id_artista = utenti.id_utente WHERE canzoni.id_canzone = ?', IdCanzone)
    song = rs.fetchone()

    rs = conn.execute('SELECT attributo_canzone.id_tag FROM attributo_canzone WHERE attributo_canzone.id_canzone = ?', IdCanzone)
    tags = rs.fetchall()
    Tags = {'Tag_1': tags[0][0], 'Tag_2': tags[1][0]}

    conn.close()
    return render_template("SongStatistics.html", stat=statistiche, song=song)

@SongBP.route('/songs/<IdCanzone>')
def songs(IdCanzone):
    conn = engine.connect()
    rs = conn.execute(' SELECT statistiche.n_riproduzioni_totali, statistiche.n_riproduzioni_settimanali'
                      ' FROM statistiche NATURAL JOIN statistiche_canzoni'
                      ' WHERE statistiche_canzoni.id_canzone = ?', IdCanzone)
    Stat = rs.fetchone()
    rs = conn.execute(' UPDATE statistiche SET n_riproduzioni_totali = ?, n_riproduzioni_settimanali = ?'
                      ' WHERE id_statistica = (SELECT statistiche_canzoni.id_statistica FROM statistiche_canzoni'
                      ' WHERE statistiche_canzoni.id_canzone = ?)', Stat[0]+1, Stat[1]+1, IdCanzone)
    rs = conn.execute(' SELECT * FROM canzoni JOIN utenti ON canzoni.id_artista = utenti.id_utente'
                      ' WHERE canzoni.id_canzone = ?', IdCanzone)
    songdata = rs.fetchone()
    rs = conn.execute(' SELECT contenuto.id_album FROM canzoni NATURAL JOIN contenuto WHERE canzoni.id_canzone = ?', IdCanzone)
    IdAlbum = rs.fetchone()
    rs = conn.execute(' SELECT * FROM canzoni NATURAL JOIN contenuto JOIN utenti ON canzoni.id_artista = utenti.id_utente'
                      ' WHERE contenuto.id_album = ?', IdAlbum)
    songAlbum = rs.fetchall()
    songAlbum =  main.ResultProxy_To_ListOfDict(songAlbum)
    for song in songAlbum:
        rs = conn.execute('SELECT attributo_canzone.id_tag FROM attributo_canzone WHERE attributo_canzone.id_canzone = ?', song['id_canzone'])
        tags = rs.fetchall()
        if tags:
           song['Tag_1'] = tags[0][0]
           song['Tag_2'] = tags[1][0]

    rs = conn.execute(' SELECT * FROM album WHERE id_album = ?', IdAlbum)
    album = rs.fetchone()

    rs = conn.execute('SELECT attributo_canzone.id_tag FROM attributo_canzone WHERE attributo_canzone.id_canzone = ?', IdCanzone)
    tags = rs.fetchall()
    Tags = {'Tag_1': tags[0][0], 'Tag_2': tags[1][0]}

    if current_user.is_authenticated:
        rs = conn.execute(' SELECT * ' 
                      ' FROM playlist ' 
                      ' WHERE playlist.id_utente = ?  AND playlist.id_playlist NOT IN (SELECT raccolte.id_playlist'
                      ' FROM raccolte NATURAL JOIN canzoni WHERE canzoni.id_canzone = ?)'
                      ' ORDER BY playlist.nome', current_user.id, IdCanzone)
        playlists = rs.fetchall()
        resp = make_response(render_template("Song.html", playlists=playlists, song=songdata, songAlbum=songAlbum, album=album, tags=Tags))
    else:
        resp = make_response(render_template("Song.html", song=songdata, songAlbum=songAlbum, album=album, tags=Tags))
    conn.close()
    return resp