from flask_login import current_user
from flask import *
from sqlalchemy import *
from flask_login import login_required
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
import main

UserBP = Blueprint('UserBP', __name__)
engine = create_engine('postgresql://postgres:BDProject2022@localhost:5432/BDProject')


# IMPORTANTE NON TOGLIERE
@UserBP.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)


@UserBP.route('/private')
@login_required
def private():
    conn = engine.connect()
    rs = conn.execute(' SELECT * FROM unive_music.playlist WHERE playlist.id_utente = %s', current_user.id)
    playlists = rs.fetchall()
    rs = conn.execute(
        ' SELECT raccolte.id_playlist, canzoni.titolo, canzoni.rilascio, canzoni.durata, canzoni.colore, '
        'canzoni.id_canzone, utenti.nickname'
        ' FROM unive_music.canzoni NATURAL JOIN unive_music.raccolte '
        ' JOIN unive_music.utenti ON canzoni.id_artista = utenti.id_utente'
        ' WHERE raccolte.id_playlist IN (SELECT playlist.id_playlist FROM unive_music.playlist'
        ' WHERE playlist.id_utente = %s)'
        ' GROUP BY raccolte.id_playlist, canzoni.titolo, canzoni.rilascio, canzoni.durata, canzoni.colore, '
        ' canzoni.id_canzone, utenti.nickname',
        current_user.id)
    songs = rs.fetchall()
    songs = main.ResultProxy_To_ListOfDict(songs)
    for song in songs:
        rs = conn.execute(
            'SELECT attributo_canzone.id_tag FROM unive_music.attributo_canzone WHERE attributo_canzone.id_canzone = %s'
            , song['id_canzone'])
        tags = rs.fetchall()
        if tags:
            song['Tag_1'] = tags[0][0]
            song['Tag_2'] = tags[1][0]

    playlist_songs = []
    for playlist in playlists:
        playlist_s = []
        for song in songs:
            if song['id_playlist'] == playlist.id_playlist:
                playlist_s.append(song)
        playlist_songs.append(playlist_s)

    resp = make_response(
        render_template("UserPage.html", user=current_user, playlists=playlists, playlist_songs=playlist_songs))
    conn.close()
    return resp


@UserBP.route('/new_playlist', methods=['GET', 'POST'])
@login_required
def NewPlaylist():
    if request.method == 'POST':
        conn = engine.connect()
        # Query necessaria per bug di serial
        rs = conn.execute('SELECT MAX(playlist.id_playlist) FROM unive_music.playlist')
        max = rs.fetchone()
        data = (max[0] + 1, current_user.id, request.form["Nome"], request.form["Descrizione"], "0")
        rs = conn.execute(
            'INSERT INTO unive_music.playlist (id_playlist, id_utente, nome, descrizione, n_canzoni) VALUES (%s, %s,%s,%s,%s)', data)
        conn.close()
        return redirect(url_for('UserBP.private'))
    else:
        return render_template("NuovaRaccolta.html")


@UserBP.route('/ModPlaylist/<IdPlaylist>', methods=['GET', 'POST'])
@login_required
def ModPlaylist(IdPlaylist):
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute(' UPDATE unive_music.playlist SET nome = %s, descrizione = %s WHERE id_playlist = %s',
                          request.form['nome'], request.form['descrizione'], IdPlaylist)
        conn.close()
        return redirect(url_for('UserBP.private'))
    else:
        return render_template("ModificaRaccolta.html", IdPlaylist=IdPlaylist)


@UserBP.route('/AddSongToPlaylist/<IdCanzone>', methods=['POST'])
@login_required
def AddSongToPlaylist(IdCanzone):
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute(' SELECT * FROM unive_music.playlist WHERE playlist.id_utente = %s ORDER BY playlist.nome',
                          current_user.id)
        playlists = rs.fetchall()
        for i, playlist in enumerate(playlists):
            if request.form.get("P_" + str(i)):
                rs = conn.execute('INSERT INTO unive_music.raccolte (id_playlist, id_canzone) VALUES (%s,%s)',
                                  playlist.id_playlist, IdCanzone)
                rs = conn.execute('SELECT playlist.n_canzoni FROM unive_music.playlist WHERE playlist.id_playlist = %s',
                                  playlist.id_playlist)
                NCanzoni = rs.fetchone()
                rs = conn.execute(' UPDATE unive_music.playlist'
                                  ' SET n_canzoni = %s'
                                  ' WHERE id_playlist = %s', NCanzoni[0] + 1, playlist.id_playlist)

                age = date.today().year - (current_user.data_nascita).year
                att = '_13_19'
                if age >= 13 and age <= 19:
                    att = '_13_19'
                if age >= 20 and age <= 29:
                    att = '_20_29'
                if age >= 30 and age <= 39:
                    att = '_30_39'
                if age >= 40 and age <= 49:
                    att = '_40_49'
                if age >= 50 and age <= 65:
                    att = '_50_65'
                if age > 65:
                    att = '_65piu'

                # controllare che funzioni questa query perchè ho tolto gli apici che c'erano prima
                query_1 = 'SELECT statistiche.' + att + ' FROM unive_music.statistiche ' \
                                                        'NATURAL JOIN unive_music.statistiche_canzoni ' \
                                                        'WHERE statistiche_canzoni.id_canzone = %s'
                query_2 = 'UPDATE unive_music.statistiche SET ' + att + ' = %s ' \
                                                                        'WHERE id_statistica = ' \
                                                                        '( SELECT statistiche_canzoni.id_statistica ' \
                                                                        'FROM unive_music.statistiche_canzoni ' \
                                                                        'WHERE statistiche_canzoni.id_canzone = %s)'

                rs = conn.execute(query_1, IdCanzone)
                stat = rs.fetchone()
                rs = conn.execute(query_2, stat[0] + 1, IdCanzone)
        conn.close()
        return redirect(url_for('UserBP.private'))
    else:
        return render_template("ModificaRaccolta.html")


@UserBP.route('/RemoveSongFromPlaylist/<Data>')
@login_required
def RemoveSongFromPlaylist(Data):
    Data_List = list(Data.split(' '))
    IdPlaylist = int(Data_List.pop())

    conn = engine.connect()
    rs = conn.execute('SELECT playlist.n_canzoni FROM unive_music.playlist WHERE playlist.id_playlist = %s', IdPlaylist)
    NCanzoni = (rs.fetchone())[0]

    for IdSong in Data_List:
        rs = conn.execute(
            ' DELETE FROM unive_music.raccolte WHERE raccolte.id_canzone = %s AND raccolte.id_playlist = %s',
            int(IdSong), IdPlaylist)
        NCanzoni = NCanzoni - 1

    rs = conn.execute(' UPDATE unive_music.playlist SET n_canzoni = %s WHERE id_playlist = %s', NCanzoni, IdPlaylist)
    conn.close()
    return redirect(url_for('UserBP.private'))


@UserBP.route('/Delplaylist/<IdPlaylist>')
@login_required
def DelPlaylist(IdPlaylist):
    conn = engine.connect()

    rs = conn.execute(' DELETE FROM unive_music.raccolte WHERE raccolte.id_playlist = %s', IdPlaylist)
    rs = conn.execute(' DELETE FROM unive_music.playlist WHERE playlist.id_playlist = %s', IdPlaylist)

    conn.close()

    return redirect(url_for('UserBP.private'))


@UserBP.route('/ModData', methods=['GET', 'POST'])
@login_required  # richiede autenticazione
def ModData():
    if request.method == 'POST':
        if check_password_hash(current_user.password, request.form['OldPwd']):
            conn = engine.connect()
            rs = conn.execute('SELECT * FROM unive_music.utenti WHERE utenti.email = %s', request.form['Email'])
            user = rs.fetchone()
            rs = conn.execute('SELECT * FROM unive_music.utenti WHERE utenti.nickname = %s', request.form['Nickname'])
            nickname = rs.fetchone()
            if request.form['Email'] != current_user.email:
                if not nickname:
                    rs = conn.execute(' UPDATE unive_music.utenti SET nickname = %s, email = %s WHERE id_utente = %s',
                                      request.form['Nickname'], request.form['Email'], current_user.id)
                else:
                    rs = conn.execute(' UPDATE unive_music.utenti SET email = %s WHERE id_utente = %s',
                                      request.form['Email'], current_user.id)

            if request.form['Nickname'] != current_user.nickname:
                if user:
                    rs = conn.execute(' UPDATE unive_music.utenti SET nickname = %s WHERE id_utente = %s',
                                      request.form['Nickname'], current_user.id)
            pwhash = generate_password_hash(request.form["NewPwd"], method='pbkdf2:sha256:260000', salt_length=16)
            rs = conn.execute('UPDATE unive_music.utenti SET bio = %s, password = %s WHERE id_utente = %s ',
                              request.form['Bio'], pwhash, current_user.id)
            conn.close()
            return redirect(url_for('UserBP.private'))
        else:
            return render_template("ModificaDatiPersonali.html")
    else:
        return render_template("ModificaDatiPersonali.html")


@UserBP.route('/Dati_Personali')
@login_required  # richiede autenticazione
def get_data():
    conn = engine.connect()
    resp = make_response(render_template("DatiPersonali.html", user=current_user))
    conn.close()
    return resp
