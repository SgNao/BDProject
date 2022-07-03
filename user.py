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
    rs = conn.execute(' SELECT * FROM Playlist WHERE Playlist.IdUtente = ?', current_user.id)
    playlists = rs.fetchall()
    rs = conn.execute(' SELECT raccolte.IdPlaylist, Canzoni.Titolo, Canzoni.Rilascio, Canzoni.Durata, Canzoni.Colore, Canzoni.IdCanzone, Utenti.Nickname'  
                      ' FROM Canzoni NATURAL JOIN Raccolte JOIN Utenti ON Canzoni.IdArtista = Utenti.IdUtenti'
                      ' WHERE Raccolte.IdPlaylist IN (SELECT Playlist.IdPlaylist FROM Playlist'
                      ' WHERE Playlist.IdUtente = ?)'
                      ' GROUP BY Raccolte.IdPlaylist, Canzoni.Titolo, Canzoni.Rilascio, Canzoni.Durata, Canzoni.Colore, Canzoni.IdCanzone', current_user.id)
    songs = rs.fetchall()
    songs =  main.ResultProxy_To_ListOfDict(songs)
    for song in songs:
        rs = conn.execute('SELECT AttributoCanzone.IdTag FROM AttributoCanzone WHERE AttributoCanzone.IdCanzone = ?', song['IdCanzone'])
        tags = rs.fetchall()
        if tags:
           song['Tag_1'] = tags[0][0]
           song['Tag_2'] = tags[1][0]

    playlist_songs = []
    for playlist in playlists:
        playlist_s = []
        for song in songs:
            if song['IdPlaylist'] == playlist.IdPlaylist:
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
        rs = conn.execute('INSERT INTO Playlist (IdUtente, Nome, Descrizione, NCanzoni) VALUES (?,?,?,?)', data)
        conn.close()
        return redirect(url_for('UserBP.private'))
    else:
        return render_template("NuovaRaccolta.html")

@UserBP.route('/ModPlaylist/<IdPlaylist>', methods=['GET', 'POST'])
@login_required
def ModPlaylist(IdPlaylist):
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute(' UPDATE Playlist SET Nome = ?, Descrizione = ? WHERE IdPlaylist = ?', request.form['nome'], request.form['descrizione'], IdPlaylist)
        conn.close()
        return redirect(url_for('UserBP.private'))
    else:
        return render_template("ModificaRaccolta.html", IdPlaylist = IdPlaylist)

@UserBP.route('/AddSongToPlaylist/<IdCanzone>', methods=['POST'])
@login_required
def AddSongToPlaylist(IdCanzone):
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute(' SELECT * FROM Playlist WHERE Playlist.Idutente = ? ORDER BY Playlist.Nome', current_user.id)
        playlists = rs.fetchall()
        for i,playlist in enumerate(playlists):
            if request.form.get("P_"+str(i)):
                rs = conn.execute('INSERT INTO Raccolte (IdPlaylist, IdCanzone) VALUES (?,?)', playlist.IdPlaylist, IdCanzone)
                rs = conn.execute('SELECT Playlist.NCanzoni FROM Playlist WHERE Playlist.IdPlaylist = ?', playlist.IdPlaylist)
                NCanzoni = rs.fetchone()
                rs = conn.execute(' UPDATE Playlist' 
                                  ' SET NCanzoni = ?' 
                                  ' WHERE IdPlaylist = ?', NCanzoni[0]+1, playlist.IdPlaylist)

                age = date.today().year - date.fromisoformat(current_user.DataNascita).year
                att = '13-19'
                if age>= 13 and age <= 19:
                    att = '13-19'
                if age>= 20 and age <= 29:
                    att = '20-29'
                if age>= 30 and age <= 39:
                    att = '30-39'
                if age>= 40 and age <= 49:
                    att = '40-49'
                if age>= 50 and age <= 65:
                    att = '50-65'
                if age>65:
                    att = '65+'

                query_1 = 'SELECT Statistiche."'+att+'" FROM Statistiche NATURAL JOIN StatCanzoni WHERE StatCanzoni.IdCanzone = ?'
                query_2 = 'UPDATE Statistiche SET "'+att+'" = ? WHERE IdStatistica = ( SELECT StatCanzoni.IdStatistica FROM StatCanzoni WHERE StatCanzoni.IdCanzone = ?)'
                
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
    rs = conn.execute('SELECT Playlist.NCanzoni FROM Playlist WHERE Playlist.IdPlaylist = ?', IdPlaylist)
    NCanzoni = (rs.fetchone())[0]

    for IdSong in Data_List:
        rs = conn.execute(' DELETE FROM Raccolte WHERE Raccolte.IdCanzone = ? AND Raccolte.IdPlaylist = ?', int(IdSong), IdPlaylist)
        NCanzoni = NCanzoni-1

    rs = conn.execute(' UPDATE Playlist SET NCanzoni = ? WHERE IdPlaylist = ?', NCanzoni, IdPlaylist)
    conn.close()
    return  redirect(url_for('UserBP.private'))

@UserBP.route('/Delplaylist/<IdPlaylist>')
@login_required
def DelPlaylist(IdPlaylist):
    
    conn = engine.connect()

    rs = conn.execute(' DELETE FROM Playlist WHERE Playlist.IdPlaylist = ?', IdPlaylist)
    rs = conn.execute(' DELETE FROM Raccolte WHERE Raccolte.IdPlaylist = ?', IdPlaylist)

    conn.close()
    
    return  redirect(url_for('UserBP.private'))

@UserBP.route('/ModData', methods=['GET', 'POST'])
@login_required  # richiede autenticazione
def ModData():
    if request.method == 'POST':
        if check_password_hash(current_user.Password, request.form['OldPwd']):
            conn = engine.connect()
            rs = conn.execute('SELECT * FROM Utenti WHERE Utenti.Email = ?', request.form['NewPwd'])
            user = rs.fetchone()
            if not user:
                pwhash = generate_password_hash(request.form["NewPwd"], method='pbkdf2:sha256:260000', salt_length=16)
                rs = conn.execute(' UPDATE Utenti SET Nickname = ?, Email = ?, Bio = ?, Password = ? WHERE IdUtenti = ?', 
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