from flask_login import current_user
from flask import *
from sqlalchemy import *
from flask_login import login_required
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

import login
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
    if current_user.Ruolo != 3:
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
    else:
        # pagina dell'admin col bottone
        return render_template("AdminPage.html", user=current_user)


@UserBP.route('/new_playlist', methods=['GET', 'POST'])
@login_required
def NewPlaylist():
    conn = engine.connect()
    rs = conn.execute('SELECT COUNT(*) FROM unive_music.playlist WHERE playlist.id_utente = %s', current_user.id)
    conn.close()
    num = rs.fetchall()
    playlist_limit = 5
    if current_user.premium:
        playlist_limit = 20
    if len(num) < playlist_limit:
        if request.method == 'POST':
            conn = engine.connect()
            data = (current_user.id, request.form["Nome"], request.form["Descrizione"], "0")
            rs = conn.execute(
                'INSERT INTO unive_music.playlist (id_utente, nome, descrizione, n_canzoni) VALUES (%s,%s,%s,%s)', data)
            conn.close()
            return redirect(url_for('UserBP.private'))
        else:
            return render_template("NuovaRaccolta.html")
    else:
        # Decidere cosa fare e messaggio di errore
        return redirect(url_for('UserBP.private'))


@UserBP.route('/ModPlaylist/<IdPlaylist>', methods=['GET', 'POST'])
@login_required
def ModPlaylist(IdPlaylist):
    return render_template("ModificaRaccolta.html", IdPlaylist=IdPlaylist, message='')


@UserBP.route('/mod_playlist_Nome/<IdPlaylist>', methods=['GET', 'POST'])
@login_required
def ModPlaylist_Nome(IdPlaylist):
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute(' UPDATE unive_music.playlist SET nome = ? WHERE playlist.id_playlist = ?', request.form['Nome'], IdPlaylist)
        conn.close()
        return render_template("ModificaRaccolta.html", IdPlaylist=IdPlaylist, message='Modifica eseguita')


@UserBP.route('/mod_playlist_Descr/<IdPlaylist>', methods=['GET', 'POST'])
@login_required
def ModPlaylist_Descr(IdPlaylist):
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute(' UPDATE unive_music.playlist SET descrizione = ? WHERE playlist.id_playlist = ?', request.form['Descrizione'], IdPlaylist)
        conn.close()
        return render_template("ModificaRaccolta.html", IdPlaylist=IdPlaylist, message='Modifica eseguita')

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
                                  ' WHERE playlist.id_playlist = %s', NCanzoni[0] + 1, playlist.id_playlist)

                age = date.today().year - current_user.data_nascita.year
                att = '_13_19'
                if 13 <= age <= 19:
                    att = '_13_19'
                if 20 <= age <= 29:
                    att = '_20_29'
                if 30 <= age <= 39:
                    att = '_30_39'
                if 40 <= age <= 49:
                    att = '_40_49'
                if 50 <= age <= 65:
                    att = '_50_65'
                if age > 65:
                    att = '_65piu'

                # controllare che funzioni questa query perché ho tolto gli apici che c'erano prima
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
    return render_template("ModificaDatiPersonali.html", message='')

@UserBP.route('/mod_data_nickname', methods=['GET', 'POST'])
@login_required  # richiede autenticazione
def ModData_Nickname():
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM unive_music.utenti WHERE utenti.Nickname = ?', request.form['Nickname'])
    user = rs.fetchone()
    if not user:
        rs = conn.execute(' UPDATE unive_music.utenti SET nickname = ? WHERE utenti.id_utente = ?', request.form['Nickname'], current_user.id)
        conn.close()
        return render_template("ModificaDatiPersonali.html", message='Modifica eseguita')
    else:
        return render_template("ModificaDatiPersonali.html", message='Nickname non disponibile', style='error active')


@UserBP.route('/mod_data_email', methods=['GET', 'POST'])
@login_required  # richiede autenticazione
def ModData_Email():
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM unive_music.utenti WHERE utenti.email = ?', request.form['Email'])
    user = rs.fetchone()
    if not user:
        rs = conn.execute(' UPDATE unive_music.utenti SET email = ? WHERE utenti.id_utente = ?', request.form['Email'], current_user.id)
        conn.close()
        return render_template("ModificaDatiPersonali.html", message='Modifica eseguita')
    else:
        return render_template("ModificaDatiPersonali.html",  message='E-mail non disponibile')


@UserBP.route('/mod_data_biografia', methods=['GET', 'POST'])
@login_required  # richiede autenticazione
def ModData_Bio():
    conn = engine.connect()
    rs = conn.execute(' UPDATE unive_music.utenti SET bio = ? WHERE utenti.id_utente = ?', request.form['bio'], current_user.id)
    conn.close()
    return render_template("ModificaDatiPersonali.html", message='Modifica eseguita', style='error active')


@UserBP.route('/mod_data_pwd', methods=['GET', 'POST'])
@login_required  # richiede autenticazione
def ModData_Pwd():
    if request.form['new_pwd'] == request.form['old_pwd']:
        pwhash = generate_password_hash(request.form["NewPwd"], method='pbkdf2:sha256:260000', salt_length=16)
        conn = engine.connect()
        rs = conn.execute(' UPDATE unive_music.utenti SET password = ? WHERE utenti.id_utente = ?', pwhash, current_user.id)
        conn.close()
        return render_template("ModificaDatiPersonali.html", message='Modifica eseguita')
    else:
        return render_template("ModificaDatiPersonali.html", message='Le password non coincidono')


@UserBP.route('/Dati_Personali')
@login_required  # richiede autenticazione
def get_data():
    conn = engine.connect()
    resp = make_response(render_template("DatiPersonali.html", user=current_user))
    conn.close()
    return resp
