from flask_login import current_user
from flask import *
from sqlalchemy import *
from flask_login import login_required
from werkzeug.security import generate_password_hash
from datetime import date
import main

UserBP = Blueprint('UserBP', __name__)
engine = create_engine('postgresql://postgres:BDProject2022@localhost:5432/BDProject')


@UserBP.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)


@UserBP.route('/area_personale')
@login_required
def area_personale():
    if current_user.ruolo != 3:
        conn = engine.connect()
        rs = conn.execute('SELECT * FROM unive_music.playlist WHERE playlist.id_utente = %s', current_user.id)
        playlists = rs.fetchall()
        rs = conn.execute('SELECT raccolte.id_playlist, canzoni.titolo, canzoni.rilascio, canzoni.durata, '
                          'canzoni.colore, canzoni.id_canzone, utenti.nickname FROM unive_music.canzoni NATURAL JOIN '
                          'unive_music.raccolte JOIN unive_music.utenti ON canzoni.id_artista = utenti.id_utente '
                          'WHERE raccolte.id_playlist IN (SELECT playlist.id_playlist FROM unive_music.playlist WHERE '
                          'playlist.id_utente = %s) GROUP BY raccolte.id_playlist, canzoni.titolo, canzoni.rilascio, '
                          'canzoni.durata, canzoni.colore, canzoni.id_canzone, utenti.nickname', current_user.id)
        songs = rs.fetchall()
        songs = main.result_proxy_to_list_of_dict(songs)

        for song in songs:
            rs = conn.execute('SELECT attributo_canzone.id_tag FROM unive_music.attributo_canzone WHERE '
                              'attributo_canzone.id_canzone = %s', song['id_canzone'])
            tags = rs.fetchall()
            if tags:
                song['Tag_1'] = tags[0][0]
                song['Tag_2'] = tags[1][0]

        playlist_songs = []

        for playlist in playlists:
            playlist_s = []
            for song in songs:
                if song['id_playlist'] == playlist['id_playlist']:
                    playlist_s.append(song)
            playlist_songs.append(playlist_s)

        resp = make_response(render_template("UserPage.html", user=current_user, playlists=playlists,
                                             playlist_songs=playlist_songs))
        conn.close()
        return resp
    else:
        return render_template("AdminPage.html", user=current_user)


@UserBP.route('/nuova_playlist', methods=['GET', 'POST'])
@login_required
def nuova_playlist():
    conn = engine.connect()
    rs = conn.execute('SELECT COUNT(*) FROM unive_music.playlist WHERE playlist.id_utente = %s', current_user.id)
    conn.close()
    num = rs.fetchall()
    playlist_limit = 5
    
    if current_user.premium:
        playlist_limit = 20
        
    if num[0][0] < playlist_limit:
        if request.method == 'POST':
            conn = engine.connect()
            data = (current_user.id, request.form["Nome"], request.form["Descrizione"], "0")
            conn.execute('INSERT INTO unive_music.playlist (id_utente, nome, descrizione, n_canzoni) VALUES (%s,%s,'
                         '%s,%s)', data)
            conn.close()
            return redirect(url_for('UserBP.area_personale'))
        else:
            return render_template("NuovaRaccolta.html")
    else:
        flash("Hai raggiunto il numero massimo di playlist creabili")
        return redirect(url_for('UserBP.area_personale'))


@UserBP.route('/modifica_playlist/<id_playlist>', methods=['GET', 'POST'])
@login_required
def modifica_playlist(id_playlist):
    return render_template("ModificaRaccolta.html", id_playlist=id_playlist, message='')


@UserBP.route('/modifica_playlist_nome/<id_playlist>', methods=['GET', 'POST'])
@login_required
def modifica_playlist_nome(id_playlist):
    if request.method == 'POST':
        conn = engine.connect()
        conn.execute('UPDATE unive_music.playlist SET nome = %s WHERE playlist.id_playlist = %s', request.form['Nome'],
                     id_playlist)
        conn.close()
        return render_template("ModificaRaccolta.html", id_playlist=id_playlist, message='Modifica eseguita')


@UserBP.route('/modifica_playlist_descrizione/<id_playlist>', methods=['GET', 'POST'])
@login_required
def modifica_playlist_descrizione(id_playlist):
    if request.method == 'POST':
        conn = engine.connect()
        conn.execute('UPDATE unive_music.playlist SET descrizione = %s WHERE playlist.id_playlist = %s',
                     request.form['Descrizione'], id_playlist)
        conn.close()
        return render_template("ModificaRaccolta.html", id_playlist=id_playlist, message='Modifica eseguita')


@UserBP.route('/aggiungi_canzone_a_playlist/<id_canzone>', methods=['POST'])
@login_required
def aggiungi_canzone_a_playlist(id_canzone):
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute('SELECT * FROM unive_music.playlist WHERE playlist.id_utente = %s ORDER BY playlist.nome',
                          current_user.id)
        playlists = rs.fetchall()

        for i, playlist in enumerate(playlists):
            if request.form.get("P_" + str(i)):
                conn.execute('INSERT INTO unive_music.raccolte (id_playlist, id_canzone) VALUES (%s,%s)',
                             playlist['id_playlist'], id_canzone)
                rs = conn.execute('SELECT playlist.n_canzoni FROM unive_music.playlist WHERE playlist.id_playlist = %s',
                                  playlist['id_playlist'])
                n_canzoni = rs.fetchone()
                conn.execute('UPDATE unive_music.playlist SET n_canzoni = %s WHERE playlist.id_playlist = %s',
                             n_canzoni[0] + 1, playlist['id_playlist'])
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

                query_1 = ('SELECT statistiche.' + att + ' FROM unive_music.statistiche NATURAL JOIN '
                                                         'unive_music.statistiche_canzoni WHERE '
                                                         'statistiche_canzoni.id_canzone = %s')
                query_2 = ('UPDATE unive_music.statistiche SET ' + att + '= %s WHERE id_statistica = ( SELECT '
                                                                         'statistiche_canzoni.id_statistica FROM '
                                                                         'unive_music.statistiche_canzoni WHERE '
                                                                         'statistiche_canzoni.id_canzone = %s)')

                rs = conn.execute(query_1, id_canzone)
                stat = rs.fetchone()
                conn.execute(query_2, stat[0] + 1, id_canzone)
        conn.close()
        return redirect(url_for('UserBP.area_personale'))
    else:
        return render_template("ModificaRaccolta.html")


@UserBP.route('/rimuovi_canzone_da_playlist/<data>')
@login_required
def rimuovi_canzone_da_playlist(data):
    data_list = list(data.split(' '))
    id_playlist = int(data_list.pop())
    conn = engine.connect()
    rs = conn.execute('SELECT playlist.n_canzoni FROM unive_music.playlist WHERE playlist.id_playlist = %s',
                      id_playlist)
    n_canzoni = (rs.fetchone())[0]

    for id_song in data_list:
        conn.execute('DELETE FROM unive_music.raccolte WHERE raccolte.id_canzone = %s AND raccolte.id_playlist = %s',
                     int(id_song), id_playlist)
        n_canzoni = n_canzoni - 1

    conn.execute('UPDATE unive_music.playlist SET n_canzoni = %s WHERE id_playlist = %s', n_canzoni, id_playlist)
    conn.close()
    return redirect(url_for('UserBP.area_personale'))


@UserBP.route('/cancella_playlist/<id_playlist>')
@login_required
def cancella_playlist(id_playlist):
    conn = engine.connect()
    conn.execute('DELETE FROM unive_music.raccolte WHERE raccolte.id_playlist = %s', id_playlist)
    conn.execute('DELETE FROM unive_music.playlist WHERE playlist.id_playlist = %s', id_playlist)
    conn.close()
    return redirect(url_for('UserBP.area_personale'))


@UserBP.route('/modifica_informazioni', methods=['GET', 'POST'])
@login_required
def modifica_informazioni():
    return render_template("ModificaDatiPersonali.html", message='')


@UserBP.route('/modifica_informazioni_nickname', methods=['GET', 'POST'])
@login_required
def modifica_informazioni_nickname():
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM unive_music.utenti WHERE utenti.nickname = %s', request.form['Nickname'])
    user = rs.fetchone()

    if not user:
        conn.execute('UPDATE unive_music.utenti SET nickname = %s WHERE utenti.id_utente = %s',
                     request.form['Nickname'], current_user.id)
        conn.close()
        return render_template("ModificaDatiPersonali.html", message='Modifica eseguita')
    else:
        return render_template("ModificaDatiPersonali.html", message='Nickname non disponibile', style='error active')


@UserBP.route('/modifica_informazioni_email', methods=['GET', 'POST'])
@login_required
def modifica_informazioni_email():
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM unive_music.utenti WHERE utenti.email = %s', request.form['Email'])
    user = rs.fetchone()

    if not user:
        conn.execute(' UPDATE unive_music.utenti SET email = %s WHERE utenti.id_utente = %s', request.form['Email'],
                     current_user.id)
        conn.close()
        return render_template("ModificaDatiPersonali.html", message='Modifica eseguita')
    else:
        return render_template("ModificaDatiPersonali.html",  message='E-mail non disponibile')


@UserBP.route('/modifica_informazioni_biografia', methods=['GET', 'POST'])
@login_required
def modifica_informazioni_biografia():
    conn = engine.connect()
    conn.execute('UPDATE unive_music.utenti SET bio = %s WHERE utenti.id_utente = %s', request.form['bio'],
                 current_user.id)
    conn.close()
    return render_template("ModificaDatiPersonali.html", message='Modifica eseguita', style='error active')


@UserBP.route('/modifica_informazioni_password', methods=['GET', 'POST'])
@login_required
def modifica_informazioni_password():
    if request.form['new_pwd'] == request.form['old_pwd']:
        pwhash = generate_password_hash(request.form["NewPwd"], method='pbkdf2:sha256:260000', salt_length=16)
        conn = engine.connect()
        conn.execute('UPDATE unive_music.utenti SET password = %s WHERE utenti.id_utente = %s', pwhash, current_user.id)
        conn.close()
        return render_template("ModificaDatiPersonali.html", message='Modifica eseguita')
    else:
        return render_template("ModificaDatiPersonali.html", message='Le password non coincidono')


@UserBP.route('/dati_personali')
@login_required
def dati_personali():
    conn = engine.connect()
    resp = make_response(render_template("DatiPersonali.html", user=current_user))
    conn.close()
    return resp
