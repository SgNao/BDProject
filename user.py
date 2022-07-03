from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask import *
from sqlalchemy import *
from flask_login import login_required
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date 
import main

UserBP = Blueprint('UserBP', __name__)
engine = create_engine('sqlite:///database.db', echo=True)


# IMPORTANTE NON TOGLIERE
@UserBP.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate, str=str, len=len)

@UserBP.route('/private')
@login_required
def private():
    conn = engine.connect()
    rs = conn.execute(' SELECT * FROM playlist WHERE playlist.id_utente = ?', current_user.id)
    playlists = rs.fetchall()
    rs = conn.execute(' SELECT raccolte.id_playlist, canzoni.titolo, canzoni.rilascio, canzoni.durata, canzoni.colore, canzoni.id_canzone, utenti.nickname'  
                      ' FROM canzoni NATURAL JOIN raccolte JOIN utenti ON canzoni.id_artista = utenti.id_utente'
                      ' WHERE raccolte.id_playlist IN (SELECT playlist.id_playlist FROM playlist'
                      ' WHERE playlist.id_utente = ?)'
                      ' GROUP BY raccolte.id_playlist, canzoni.titolo, canzoni.rilascio, canzoni.durata, canzoni.colore, canzoni.id_canzone', current_user.id)
    songs = rs.fetchall()
    songs =  main.ResultProxy_To_ListOfDict(songs)
    for song in songs:
        rs = conn.execute('SELECT attributo_canzone.id_tag FROM attributo_canzone WHERE attributo_canzone.id_canzone = ?', song['id_canzone'])
        tags = rs.fetchall()
        if tags:
           song['Tag_1'] = tags[0][0]
           song['Tag_2'] = tags[1][0]

    playlist_songs = []
    for playlist in playlists:
        playlist_s = []
        for song in songs:
            if song['IdPlaylist'] == playlist.id_playlist:
                playlist_s.append(song)
        playlist_songs.append(playlist_s)

    resp = make_response(render_template("UserPage.html", user=current_user, playlists=playlists, playlist_songs=playlist_songs))
    conn.close()
    return resp

@UserBP.route('/new_playlist', methods=['GET', 'POST'])
@login_required
def NewPlaylist():
    if request.method == 'POST':
        conn = engine.connect()
        data = ( current_user.id, request.form["Nome"], request.form["Descrizione"], "0")
        rs = conn.execute('INSERT INTO playlist (id_utente, nome, descrizione, n_canzoni) VALUES (?,?,?,?)', data)
        conn.close()
        return redirect(url_for('UserBP.private'))
    else:
        return render_template("NuovaRaccolta.html")

@UserBP.route('/ModPlaylist/<IdPlaylist>', methods=['GET', 'POST'])
@login_required
def ModPlaylist(IdPlaylist):
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute(' UPDATE playlist SET nome = ?, descrizione = ? WHERE id_playlist = ?', request.form['nome'], request.form['descrizione'], IdPlaylist)
        conn.close()
        return redirect(url_for('UserBP.private'))
    else:
        return render_template("ModificaRaccolta.html", IdPlaylist = IdPlaylist)

@UserBP.route('/AddSongToPlaylist/<IdCanzone>', methods=['POST'])
@login_required
def AddSongToPlaylist(IdCanzone):
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute(' SELECT * FROM playlist WHERE playlist.id_utente = ? ORDER BY playlist.nome', current_user.id)
        playlists = rs.fetchall()
        for i,playlist in enumerate(playlists):
            if request.form.get("P_"+str(i)):
                rs = conn.execute('INSERT INTO raccolte (id_playlist, id_canzone) VALUES (?,?)', playlist.id_playlist, IdCanzone)
                rs = conn.execute('SELECT playlist.n_canzoni FROM playlist WHERE playlist.id_playlist = ?', playlist.id_playlist)
                NCanzoni = rs.fetchone()
                rs = conn.execute(' UPDATE playlist' 
                                  ' SET n_canzoni = ?' 
                                  ' WHERE id_playlist = ?', NCanzoni[0]+1, playlist.id_playlist)

                age = date.today().year - date.fromisoformat(current_user.data_nascita).year
                att = '_13_19'
                if age>= 13 and age <= 19:
                    att = '_13_19'
                if age>= 20 and age <= 29:
                    att = '_20_29'
                if age>= 30 and age <= 39:
                    att = '_30_39'
                if age>= 40 and age <= 49:
                    att = '_40_49'
                if age>= 50 and age <= 65:
                    att = '_50_65'
                if age>65:
                    att = '_65piu'

                #controllare che funzioni questa query perchè ho tolto gli apici che c'erano prima
                query_1 = 'SELECT statistiche.'+att+' FROM statistiche NATURAL JOIN statistiche_canzoni WHERE statistiche_canzoni.id_canzone = ?'
                query_2 = 'UPDATE statistiche SET '+att+' = ? WHERE id_statistica = ( SELECT statistiche_canzoni.id_statistica FROM statistiche_canzoni WHERE statistiche_canzoni.id_canzone = ?)'
                
                rs = conn.execute(query_1, IdCanzone)
                stat = rs.fetchone()
                rs = conn.execute(query_2, stat[0]+1, IdCanzone)
        conn.close()
        return  redirect(url_for('UserBP.private'))
    else:
        return render_template("ModificaRaccolta.html")

@UserBP.route('/RemoveSongFromPlaylist/<Data>')
@login_required
def RemoveSongFromPlaylist(Data):
    Data_List = list(Data.split(' '))
    IdPlaylist = int(Data_List.pop())

    conn = engine.connect()
    rs = conn.execute('SELECT playlist.n_canzoni FROM playlist WHERE playlist.id_playlist = ?', IdPlaylist)
    NCanzoni = (rs.fetchone())[0]

    for IdSong in Data_List:
        rs = conn.execute(' DELETE FROM raccolte WHERE raccolte.id_canzone = ? AND raccolte.id_playlist = ?', int(IdSong), IdPlaylist)
        NCanzoni = NCanzoni-1

    rs = conn.execute(' UPDATE playlist SET n_canzoni = ? WHERE id_playlist = ?', NCanzoni, IdPlaylist)
    conn.close()
    return  redirect(url_for('UserBP.private'))

@UserBP.route('/Delplaylist/<IdPlaylist>')
@login_required
def DelPlaylist(IdPlaylist):
    
    conn = engine.connect()

    rs = conn.execute(' DELETE FROM raccolte WHERE raccolte.id_playlist = ?', IdPlaylist)
    rs = conn.execute(' DELETE FROM playlist WHERE playlist.id_playlist = ?', IdPlaylist)

    conn.close()
    
    return  redirect(url_for('UserBP.private'))

@UserBP.route('/ModData', methods=['GET', 'POST'])
@login_required  # richiede autenticazione
def ModData():
    if request.method == 'POST':
        if check_password_hash(current_user.Password, request.form['OldPwd']):
            conn = engine.connect()
            rs = conn.execute('SELECT * FROM utenti WHERE utenti.email = ?', request.form['NewPwd'])
            user = rs.fetchone()
            if not user:
                pwhash = generate_password_hash(request.form["NewPwd"], method='pbkdf2:sha256:260000', salt_length=16)
                rs = conn.execute(' UPDATE utenti SET nickname = ?, email = ?, bio = ?, password = ? WHERE id_utente = ?',
                                  request.form['Nickname'], request.form['Email'], request.form['Bio'], pwhash, current_user.id)
                conn.close()
                return redirect(url_for('UserBP.private'))
            else:
                conn.close()
                return render_template("ModificaDatiPersonali.html")
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