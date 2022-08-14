--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4
-- Dumped by pg_dump version 14.4

-- Started on 2022-08-14 17:08:20

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 16395)
-- Name: unive_music; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA unive_music;


ALTER SCHEMA unive_music OWNER TO postgres;

--
-- TOC entry 226 (class 1255 OID 16396)
-- Name: check_debutto(); Type: FUNCTION; Schema: unive_music; Owner: postgres
--

CREATE FUNCTION unive_music.check_debutto() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN
	IF NEW.rilascio < (SELECT debutto FROM unive_music."artisti" WHERE NEW.id_artista = unive_music."artisti".id_utente) THEN
		UPDATE unive_music."artisti" 
		SET debutto = NEW.rilascio
		WHERE NEW.id_artista = unive_music."artisti".id_utente;
	END IF;
	RETURN NEW;
END;$$;


ALTER FUNCTION unive_music.check_debutto() OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 16397)
-- Name: album_id_album_seq; Type: SEQUENCE; Schema: unive_music; Owner: postgres
--

CREATE SEQUENCE unive_music.album_id_album_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE unive_music.album_id_album_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 210 (class 1259 OID 16398)
-- Name: album; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.album (
    id_album integer DEFAULT nextval('unive_music.album_id_album_seq'::regclass) NOT NULL,
    titolo text NOT NULL,
    rilascio date NOT NULL,
    colore text NOT NULL,
    n_canzoni integer DEFAULT 0 NOT NULL,
    id_artista integer NOT NULL
);


ALTER TABLE unive_music.album OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 16405)
-- Name: artisti; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.artisti (
    id_utente integer NOT NULL,
    debutto date
);


ALTER TABLE unive_music.artisti OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 16408)
-- Name: attributo_album; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.attributo_album (
    id_tag text NOT NULL,
    id_album integer NOT NULL
);


ALTER TABLE unive_music.attributo_album OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 16413)
-- Name: attributo_canzone; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.attributo_canzone (
    id_tag text NOT NULL,
    id_canzone integer NOT NULL
);


ALTER TABLE unive_music.attributo_canzone OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 16418)
-- Name: canzoni_id_canzone_seq; Type: SEQUENCE; Schema: unive_music; Owner: postgres
--

CREATE SEQUENCE unive_music.canzoni_id_canzone_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE unive_music.canzoni_id_canzone_seq OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16419)
-- Name: canzoni; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.canzoni (
    id_canzone integer DEFAULT nextval('unive_music.canzoni_id_canzone_seq'::regclass) NOT NULL,
    titolo text NOT NULL,
    rilascio date NOT NULL,
    durata integer NOT NULL,
    colore text NOT NULL,
    id_artista integer NOT NULL
);


ALTER TABLE unive_music.canzoni OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16425)
-- Name: contenuto; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.contenuto (
    id_album integer NOT NULL,
    id_canzone integer NOT NULL
);


ALTER TABLE unive_music.contenuto OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16428)
-- Name: playlist_id_playlist_seq; Type: SEQUENCE; Schema: unive_music; Owner: postgres
--

CREATE SEQUENCE unive_music.playlist_id_playlist_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE unive_music.playlist_id_playlist_seq OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16429)
-- Name: playlist; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.playlist (
    id_utente integer NOT NULL,
    nome text NOT NULL,
    descrizione text,
    n_canzoni integer DEFAULT 0 NOT NULL,
    id_playlist integer DEFAULT nextval('unive_music.playlist_id_playlist_seq'::regclass) NOT NULL
);


ALTER TABLE unive_music.playlist OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16436)
-- Name: raccolte; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.raccolte (
    id_playlist integer NOT NULL,
    id_canzone integer NOT NULL
);


ALTER TABLE unive_music.raccolte OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16439)
-- Name: statistiche_id_statistica_seq; Type: SEQUENCE; Schema: unive_music; Owner: postgres
--

CREATE SEQUENCE unive_music.statistiche_id_statistica_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE unive_music.statistiche_id_statistica_seq OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16440)
-- Name: statistiche; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.statistiche (
    id_statistica integer DEFAULT nextval('unive_music.statistiche_id_statistica_seq'::regclass) NOT NULL,
    _13_19 integer DEFAULT 0 NOT NULL,
    _20_29 integer DEFAULT 0 NOT NULL,
    _30_39 integer DEFAULT 0 NOT NULL,
    _40_49 integer DEFAULT 0 NOT NULL,
    _50_65 integer DEFAULT 0 NOT NULL,
    _65piu integer DEFAULT 0 NOT NULL,
    n_riproduzioni_totali integer DEFAULT 0 NOT NULL,
    n_riproduzioni_settimanali integer DEFAULT 0 NOT NULL
);


ALTER TABLE unive_music.statistiche OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16452)
-- Name: statistiche_canzoni; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.statistiche_canzoni (
    id_statistica integer NOT NULL,
    id_canzone integer NOT NULL
);


ALTER TABLE unive_music.statistiche_canzoni OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16455)
-- Name: tag; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.tag (
    tag text NOT NULL
);


ALTER TABLE unive_music.tag OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16460)
-- Name: utenti_id_utenti_seq; Type: SEQUENCE; Schema: unive_music; Owner: postgres
--

CREATE SEQUENCE unive_music.utenti_id_utenti_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE unive_music.utenti_id_utenti_seq OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16461)
-- Name: utenti; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.utenti (
    id_utente integer DEFAULT nextval('unive_music.utenti_id_utenti_seq'::regclass) NOT NULL,
    email text NOT NULL,
    nome text NOT NULL,
    cognome text NOT NULL,
    nickname text,
    bio text,
    data_nascita date NOT NULL,
    password text NOT NULL,
    ruolo integer DEFAULT 1 NOT NULL,
    premium boolean DEFAULT false NOT NULL
);


ALTER TABLE unive_music.utenti OWNER TO postgres;

--
-- TOC entry 3421 (class 0 OID 16398)
-- Dependencies: 210
-- Data for Name: album; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.album (id_album, titolo, rilascio, colore, n_canzoni, id_artista) FROM stdin;
1	Kill 'em all	1983-07-25	#ff0000	10	2
2	Ride the lightning	1984-07-27	#ff4000	8	2
3	Master of puppets	1986-03-03	#ff8000	8	2
4	... And justice for all	1988-08-25	#ffbf00	9	2
5	Metallica	1991-08-12	#ffff00	12	2
6	Made in heaven	1995-11-06	#bfff00	10	3
7	The miracle	1989-05-22	#80ff00	10	3
8	A night at the opera	1975-11-21	#40ff00	12	3
9	News of the world	1977-10-28	#00ff00	11	3
10	The game	1980-06-30	#00ff40	10	3
11	Appetite for destruction	1987-07-21	#00ff80	12	4
12	G N' R Lies	1988-11-29	#00ffbf	8	4
13	Use your illusion I	1991-09-17	#00ffff	16	4
14	Use your illusion II	1991-09-17	#00bfff	14	4
15	The spaghetti incident?	1993-11-23	#0080ff	12	4
16	Ligabue	1990-05-11	#0040ff	11	5
17	Mondovisione	2013-11-26	#0000ff	14	5
18	Buon compleanno Elvis	1995-09-21	#4000ff	14	5
19	Sopravvissuti e sopravviventi	1993-01-22	#8000ff	13	5
20	Nome e cognome	2005-09-16	#bf00ff	11	5
21	...Ma cosa vuoi che sia una canzone...	1978-05-25	#ff00ff	8	6
22	Non siamo mica gli americani!	1979-04-30	#ff00bf	9	6
23	Colpa d'Alfredo	1980-04-03	#ff0080	8	6
24	Siamo solo noi	1981-04-09	#ff0040	8	6
25	Vado sl massimo	1982-04-13	#ff0000	9	6
26	Herzeleid	1995-09-25	#ff4000	11	7
27	Sehnsucht 	1997-08-22	#ff8000	11	7
28	Mutter 	2001-04-02	#ffbf00	11	7
29	Reise, reise	2004-09-27	#ffff00	11	7
30	Rosenrot	2005-08-28	#bfff00	11	7
31	Hybrid theory	2001-10-24	#80ff00	12	8
32	Meteora	2003-03-25	#40ff00	13	8
33	Minutes to midnight	2007-05-15	#00ff00	12	8
34	A thousand suns	2010-09-14	#00ff40	15	8
35	Living things	2012-06-26	#00ff80	12	8
36	Laura Pausini	1993-04-26	#00ffbf	8	9
37	Laura	1994-02-26	#00ffff	10	9
38	Le cose che vivi	1996-09-12	#00bfff	12	9
39	La mia risposta	1998-10-15	#0080ff	13	9
40	Tra te e il mare	2000-09-15	#0040ff	14	9
41	Il mare calmo della sera	1994-01-01	#0000ff	13	10
42	Bocelli	1995-11-13	#4000ff	11	10
43	Viaggio italiano	1996-01-01	#8000ff	16	10
44	Aria - The opera album	1998-01-01	#bf00ff	17	10
45	Sogno	1999-04-06	#ff00ff	14	10
46	Ricky Martin	1991-11-26	#ff00bf	11	11
47	Me amaras	1993-05-25	#ff0080	10	11
48	A medio vivir	1995-09-12	#ff0040	12	11
49	Vuelve	1998-02-10	#ff0000	12	11
50	Sound loaded	2000-12-26	#ff4000	15	11
\.


--
-- TOC entry 3422 (class 0 OID 16405)
-- Dependencies: 211
-- Data for Name: artisti; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.artisti (id_utente, debutto) FROM stdin;
2	1983-07-25
3	1975-11-21
4	1987-07-21
5	1990-05-11
6	1978-05-25
7	1995-09-25
8	2000-10-24
9	1993-04-26
10	1994-01-01
11	1991-11-26
\.


--
-- TOC entry 3423 (class 0 OID 16408)
-- Dependencies: 212
-- Data for Name: attributo_album; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.attributo_album (id_tag, id_album) FROM stdin;
Speed Metal	1
Thrash Metal	1
Speed Metal	2
Thrash Metal	2
Speed Metal	3
Thrash Metal	3
Thrash Metal	4
Heavy Metal	4
Progressive Metal	4
Heavy Metal	5
Hard Rock	5
Hard Rock	6
Pop Rock	6
Hard Rock	7
Pop Rock	7
Hard Rock	8
Pop Rock	8
Progressive Rock	8
Pop	8
Arena Rock	9
Hard Rock	9
Pop Rock	10
Megaforce	1
Elektra	2
Elektra	3
Elektra	4
Elektra	5
Hollywood Records	6
Hollywood Records	7
Hollywood Records	8
Elektra	9
EMI	10
Hard Rock	11
Heavy Metal	11
Sleaze Metal	11
Geffen	11
Hard Rock	12
Geffen	12
Musica Acustica	12
Hard Rock	13
Heavy Metal	13
Geffen	13
Hard Rock	14
Heavy Metal	14
Geffen	14
Hard Rock	15
Heavy Metal	15
Geffen	15
Punk Rock	15
Pop Rock	16
WEA Italiana	16
Zoo Aperto	17
Rock	17
Pop	18
Pop Rock	18
Alternative Country	18
Rock And Roll	18
WEA Italiana	18
Grunge	19
Pop Rock	19
Pop	19
WEA Italiana	19
Pop Rock	20
Warner Bros.	20
Musica D'Autore	21
Pop Rock	21
Lotus LOP	21
Lotus Records	22
Pop Rock	22
Rock	22
Targa	23
Rock	23
Targa	24
Rock	24
Rock	25
Pop Rock	25
Carosello	25
Industrial Metal	26
Alternative Metal	26
Neue Deutsche Harte	26
Motor Music	26
Industrial Metal	27
Alternative Metal	27
Neue Deutsche Harte	27
Motor Music	27
Industrial Metal	28
Motor Music	28
Gothic Metal	29
Industrial Metal	29
Motor Music	29
Gothic Metal	30
Industrial Metal	30
Universal	30
Nu Metal	31
Rap Metal	31
Alternative Metal	31
Warner Bros.	31
Rap Rock	32
Nu Metal	32
Alternative Metal	32
Warner Bros.	32
Alternative Rock	33
Warner Bros.	33
Alternative Rock	34
Electronic Rock	34
Experimental Rock	34
Rap Rock	34
Warner Bros.	34
Alternative Rock	35
Electronic Rock	35
Rap Rock	35
Warner Bros.	35
Pop	36
CGD	36
Pop	37
CGD	37
Pop	38
CGD	38
Pop	39
CGD	39
Pop	40
CGD	40
Pop	41
Musica Classica	41
Sugar	41
Pop	42
Sugar	42
Musica Classica	43
Polygram International	43
Opera Lirica	44
Philips Records	44
Pop	45
Philips Records	45
Musica Latina	46
Pop	46
Sony Music	46
Musica Latina	47
Pop	47
Sony Music	47
Musica Latina	48
Pop	48
Sony Music	48
Musica Latina	49
Pop	49
Sony Music	49
Pop Latino	50
Sony Music	50
\.


--
-- TOC entry 3424 (class 0 OID 16413)
-- Dependencies: 213
-- Data for Name: attributo_canzone; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.attributo_canzone (id_tag, id_canzone) FROM stdin;
Speed Metal	1
Speed Metal	2
Speed Metal	3
Speed Metal	4
Speed Metal	5
Speed Metal	6
Speed Metal	7
Speed Metal	8
Speed Metal	9
Speed Metal	10
Thrash Metal	1
Thrash Metal	2
Thrash Metal	3
Thrash Metal	4
Thrash Metal	5
Thrash Metal	6
Thrash Metal	7
Thrash Metal	8
Thrash Metal	9
Thrash Metal	10
Speed Metal	11
Speed Metal	12
Speed Metal	13
Speed Metal	14
Speed Metal	15
Speed Metal	16
Speed Metal	17
Speed Metal	18
Thrash Metal	11
Thrash Metal	12
Thrash Metal	13
Thrash Metal	14
Thrash Metal	15
Thrash Metal	16
Thrash Metal	17
Thrash Metal	18
Speed Metal	19
Speed Metal	20
Speed Metal	21
Speed Metal	22
Speed Metal	23
Speed Metal	24
Speed Metal	25
Speed Metal	26
Thrash Metal	19
Thrash Metal	20
Thrash Metal	21
Thrash Metal	22
Thrash Metal	23
Thrash Metal	24
Thrash Metal	25
Thrash Metal	26
Thrash Metal	27
Thrash Metal	28
Thrash Metal	29
Thrash Metal	30
Thrash Metal	31
Thrash Metal	32
Thrash Metal	33
Thrash Metal	34
Thrash Metal	35
Heavy Metal	27
Heavy Metal	28
Heavy Metal	29
Heavy Metal	30
Heavy Metal	31
Heavy Metal	32
Heavy Metal	33
Heavy Metal	34
Heavy Metal	35
Progressive Metal	27
Progressive Metal	28
Progressive Metal	29
Progressive Metal	30
Progressive Metal	31
Progressive Metal	32
Progressive Metal	33
Progressive Metal	34
Progressive Metal	35
Heavy Metal	36
Heavy Metal	37
Heavy Metal	38
Heavy Metal	39
Heavy Metal	40
Heavy Metal	41
Heavy Metal	42
Heavy Metal	43
Heavy Metal	44
Heavy Metal	45
Heavy Metal	46
Heavy Metal	47
Hard Rock	36
Hard Rock	37
Hard Rock	38
Hard Rock	39
Hard Rock	40
Hard Rock	41
Hard Rock	42
Hard Rock	43
Hard Rock	44
Hard Rock	45
Hard Rock	46
Hard Rock	47
Hard Rock	48
Hard Rock	49
Hard Rock	50
Hard Rock	51
Hard Rock	52
Hard Rock	53
Hard Rock	54
Hard Rock	55
Hard Rock	56
Hard Rock	57
Pop Rock	48
Pop Rock	49
Pop Rock	50
Pop Rock	51
Pop Rock	52
Pop Rock	53
Pop Rock	54
Pop Rock	55
Pop Rock	56
Pop Rock	57
Hard Rock	58
Hard Rock	59
Hard Rock	60
Hard Rock	61
Hard Rock	62
Hard Rock	63
Hard Rock	64
Hard Rock	65
Hard Rock	66
Hard Rock	67
Pop Rock	58
Pop Rock	59
Pop Rock	60
Pop Rock	61
Pop Rock	62
Pop Rock	63
Pop Rock	64
Pop Rock	65
Pop Rock	66
Pop Rock	67
Hard Rock	68
Hard Rock	69
Hard Rock	70
Hard Rock	71
Hard Rock	72
Hard Rock	73
Hard Rock	74
Hard Rock	75
Hard Rock	76
Hard Rock	77
Hard Rock	78
Hard Rock	79
Pop Rock	68
Pop Rock	69
Pop Rock	70
Pop Rock	71
Pop Rock	72
Pop Rock	73
Pop Rock	74
Pop Rock	75
Pop Rock	76
Pop Rock	77
Pop Rock	78
Pop Rock	79
Progressive Rock	68
Progressive Rock	69
Progressive Rock	70
Progressive Rock	71
Progressive Rock	72
Progressive Rock	73
Progressive Rock	74
Progressive Rock	75
Progressive Rock	76
Progressive Rock	77
Progressive Rock	78
Progressive Rock	79
Pop	68
Pop	69
Pop	70
Pop	71
Pop	72
Pop	73
Pop	74
Pop	75
Pop	76
Pop	77
Pop	78
Pop	79
Arena Rock	80
Arena Rock	81
Arena Rock	82
Arena Rock	83
Arena Rock	84
Arena Rock	85
Arena Rock	86
Arena Rock	87
Arena Rock	88
Arena Rock	89
Arena Rock	90
Hard Rock	80
Hard Rock	81
Hard Rock	82
Hard Rock	83
Hard Rock	84
Hard Rock	85
Hard Rock	86
Hard Rock	87
Hard Rock	88
Hard Rock	89
Hard Rock	90
Pop Rock	91
Pop Rock	92
Pop Rock	93
Pop Rock	94
Pop Rock	95
Pop Rock	96
Pop Rock	97
Pop Rock	98
Pop Rock	99
Pop Rock	100
Inglese	1
Inglese	2
Inglese	3
Inglese	4
Inglese	5
Inglese	6
Inglese	7
Inglese	8
Inglese	9
Inglese	10
Inglese	11
Inglese	12
Inglese	13
Inglese	14
Inglese	15
Inglese	16
Inglese	17
Inglese	18
Inglese	19
Inglese	20
Inglese	21
Inglese	22
Inglese	23
Inglese	24
Inglese	25
Inglese	26
Inglese	27
Inglese	28
Inglese	29
Inglese	30
Inglese	31
Inglese	32
Inglese	33
Inglese	34
Inglese	35
Inglese	36
Inglese	37
Inglese	38
Inglese	39
Inglese	40
Inglese	41
Inglese	42
Inglese	43
Inglese	44
Inglese	45
Inglese	46
Inglese	47
Inglese	48
Inglese	49
Inglese	50
Inglese	51
Inglese	52
Inglese	53
Inglese	54
Inglese	55
Inglese	56
Inglese	57
Inglese	58
Inglese	59
Inglese	60
Inglese	61
Inglese	62
Inglese	63
Inglese	64
Inglese	65
Inglese	66
Inglese	67
Inglese	68
Inglese	69
Inglese	70
Inglese	71
Inglese	72
Inglese	73
Inglese	74
Inglese	75
Inglese	76
Inglese	77
Inglese	78
Inglese	79
Inglese	80
Inglese	81
Inglese	82
Inglese	83
Inglese	84
Inglese	85
Inglese	86
Inglese	87
Inglese	88
Inglese	89
Inglese	90
Inglese	91
Inglese	92
Inglese	93
Inglese	94
Inglese	95
Inglese	96
Inglese	97
Inglese	98
Inglese	99
Inglese	100
Inglese	101
Inglese	102
Inglese	103
Inglese	104
Inglese	105
Inglese	106
Inglese	107
Inglese	108
Inglese	109
Inglese	110
Inglese	111
Inglese	112
Hard Rock	101
Hard Rock	102
Hard Rock	103
Hard Rock	104
Hard Rock	105
Hard Rock	106
Hard Rock	107
Hard Rock	108
Hard Rock	109
Hard Rock	110
Hard Rock	111
Hard Rock	112
Heavy Metal	101
Heavy Metal	102
Heavy Metal	103
Heavy Metal	104
Heavy Metal	105
Heavy Metal	106
Heavy Metal	107
Heavy Metal	108
Heavy Metal	109
Heavy Metal	110
Heavy Metal	111
Heavy Metal	112
Sleaze Metal	101
Sleaze Metal	102
Sleaze Metal	103
Sleaze Metal	104
Sleaze Metal	105
Sleaze Metal	106
Sleaze Metal	107
Sleaze Metal	108
Sleaze Metal	109
Sleaze Metal	110
Sleaze Metal	111
Sleaze Metal	112
Musica Acustica	113
Musica Acustica	114
Musica Acustica	115
Musica Acustica	116
Musica Acustica	117
Musica Acustica	118
Musica Acustica	119
Musica Acustica	120
Hard Rock	113
Hard Rock	114
Hard Rock	115
Hard Rock	116
Hard Rock	117
Hard Rock	118
Hard Rock	119
Hard Rock	120
Inglese	113
Inglese	114
Inglese	115
Inglese	116
Inglese	117
Inglese	118
Inglese	119
Inglese	120
Inglese	121
Inglese	122
Inglese	123
Inglese	124
Inglese	125
Inglese	126
Inglese	127
Inglese	128
Inglese	129
Inglese	130
Inglese	131
Inglese	132
Inglese	133
Inglese	134
Inglese	135
Inglese	136
Hard Rock	121
Hard Rock	122
Hard Rock	123
Hard Rock	124
Hard Rock	125
Hard Rock	126
Hard Rock	127
Hard Rock	128
Hard Rock	129
Hard Rock	130
Hard Rock	131
Hard Rock	132
Hard Rock	133
Hard Rock	134
Hard Rock	135
Hard Rock	136
Heavy Metal	121
Heavy Metal	122
Heavy Metal	123
Heavy Metal	124
Heavy Metal	125
Heavy Metal	126
Heavy Metal	127
Heavy Metal	128
Heavy Metal	129
Heavy Metal	130
Heavy Metal	131
Heavy Metal	132
Heavy Metal	133
Heavy Metal	134
Heavy Metal	135
Heavy Metal	136
Heavy Metal	137
Heavy Metal	138
Heavy Metal	139
Heavy Metal	140
Heavy Metal	141
Heavy Metal	142
Heavy Metal	143
Heavy Metal	144
Heavy Metal	145
Heavy Metal	146
Heavy Metal	147
Heavy Metal	148
Heavy Metal	149
Heavy Metal	150
Hard Rock	137
Hard Rock	138
Hard Rock	139
Hard Rock	140
Hard Rock	141
Hard Rock	142
Hard Rock	143
Hard Rock	144
Hard Rock	145
Hard Rock	146
Hard Rock	147
Hard Rock	148
Hard Rock	149
Hard Rock	150
Inglese	137
Inglese	138
Inglese	139
Inglese	140
Inglese	141
Inglese	142
Inglese	143
Inglese	144
Inglese	145
Inglese	146
Inglese	147
Inglese	148
Inglese	149
Inglese	150
Inglese	151
Inglese	152
Inglese	153
Inglese	154
Inglese	155
Inglese	156
Inglese	157
Inglese	158
Inglese	159
Inglese	160
Inglese	161
Inglese	162
Punk Rock	151
Punk Rock	152
Punk Rock	153
Punk Rock	154
Punk Rock	155
Punk Rock	156
Punk Rock	157
Punk Rock	158
Punk Rock	159
Punk Rock	160
Punk Rock	161
Punk Rock	162
Heavy Metal	151
Heavy Metal	152
Heavy Metal	153
Heavy Metal	154
Heavy Metal	155
Heavy Metal	156
Heavy Metal	157
Heavy Metal	158
Heavy Metal	159
Heavy Metal	160
Heavy Metal	161
Heavy Metal	162
Hard Rock	151
Hard Rock	152
Hard Rock	153
Hard Rock	154
Hard Rock	155
Hard Rock	156
Hard Rock	157
Hard Rock	158
Hard Rock	159
Hard Rock	160
Hard Rock	161
Hard Rock	162
Italiano	163
Italiano	164
Italiano	165
Italiano	166
Italiano	167
Italiano	168
Italiano	169
Italiano	170
Italiano	171
Italiano	172
Italiano	173
Pop Rock	163
Pop Rock	164
Pop Rock	165
Pop Rock	166
Pop Rock	167
Pop Rock	168
Pop Rock	169
Pop Rock	170
Pop Rock	171
Pop Rock	172
Pop Rock	173
Rock	174
Rock	175
Rock	176
Rock	177
Rock	178
Rock	179
Rock	180
Rock	181
Rock	182
Rock	183
Rock	184
Rock	185
Rock	186
Rock	187
Italiano	174
Italiano	175
Italiano	176
Italiano	177
Italiano	178
Italiano	179
Italiano	180
Italiano	181
Italiano	182
Italiano	183
Italiano	184
Italiano	185
Italiano	186
Italiano	187
Pop	188
Pop	189
Pop	190
Pop	191
Pop	192
Pop	193
Pop	194
Pop	195
Pop	196
Pop	197
Pop	198
Pop	199
Pop	200
Pop	201
Pop Rock	188
Pop Rock	189
Pop Rock	190
Pop Rock	191
Pop Rock	192
Pop Rock	193
Pop Rock	194
Pop Rock	195
Pop Rock	196
Pop Rock	197
Pop Rock	198
Pop Rock	199
Pop Rock	200
Pop Rock	201
Alternative Country	188
Alternative Country	189
Alternative Country	190
Alternative Country	191
Alternative Country	192
Alternative Country	193
Alternative Country	194
Alternative Country	195
Alternative Country	196
Alternative Country	197
Alternative Country	198
Alternative Country	199
Alternative Country	200
Alternative Country	201
Rock And Roll	188
Rock And Roll	189
Rock And Roll	190
Rock And Roll	191
Rock And Roll	192
Rock And Roll	193
Rock And Roll	194
Rock And Roll	195
Rock And Roll	196
Rock And Roll	197
Rock And Roll	198
Rock And Roll	199
Rock And Roll	200
Rock And Roll	201
Italiano	188
Italiano	189
Italiano	190
Italiano	191
Italiano	192
Italiano	193
Italiano	194
Italiano	195
Italiano	196
Italiano	197
Italiano	198
Italiano	199
Italiano	200
Italiano	201
Grunge	202
Grunge	203
Grunge	204
Grunge	205
Grunge	206
Grunge	207
Grunge	208
Grunge	209
Grunge	210
Grunge	211
Grunge	212
Grunge	213
Grunge	214
Pop Rock	202
Pop Rock	203
Pop Rock	204
Pop Rock	205
Pop Rock	206
Pop Rock	207
Pop Rock	208
Pop Rock	209
Pop Rock	210
Pop Rock	211
Pop Rock	212
Pop Rock	213
Pop Rock	214
Pop	202
Pop	203
Pop	204
Pop	205
Pop	206
Pop	207
Pop	208
Pop	209
Pop	210
Pop	211
Pop	212
Pop	213
Pop	214
Italiano	202
Italiano	203
Italiano	204
Italiano	205
Italiano	206
Italiano	207
Italiano	208
Italiano	209
Italiano	210
Italiano	211
Italiano	212
Italiano	213
Italiano	214
Italiano	215
Italiano	216
Italiano	217
Italiano	218
Italiano	219
Italiano	220
Italiano	221
Italiano	222
Italiano	223
Italiano	224
Italiano	225
Pop Rock	215
Pop Rock	216
Pop Rock	217
Pop Rock	218
Pop Rock	219
Pop Rock	220
Pop Rock	221
Pop Rock	222
Pop Rock	223
Pop Rock	224
Pop Rock	225
Musica D'Autore	226
Musica D'Autore	227
Musica D'Autore	228
Musica D'Autore	229
Musica D'Autore	230
Musica D'Autore	231
Musica D'Autore	232
Musica D'Autore	233
Pop Rock	226
Pop Rock	227
Pop Rock	228
Pop Rock	229
Pop Rock	230
Pop Rock	231
Pop Rock	232
Pop Rock	233
Italiano	226
Italiano	227
Italiano	228
Italiano	229
Italiano	230
Italiano	231
Italiano	232
Italiano	233
Italiano	234
Italiano	235
Italiano	236
Italiano	237
Italiano	238
Italiano	239
Italiano	240
Italiano	241
Italiano	242
Pop Rock	234
Pop Rock	235
Pop Rock	236
Pop Rock	237
Pop Rock	238
Pop Rock	239
Pop Rock	240
Pop Rock	241
Pop Rock	242
Rock	234
Rock	235
Rock	236
Rock	237
Rock	238
Rock	239
Rock	240
Rock	241
Rock	242
Italiano	243
Italiano	244
Italiano	245
Italiano	246
Italiano	247
Italiano	248
Italiano	249
Italiano	250
Rock	243
Rock	244
Rock	245
Rock	246
Rock	247
Rock	248
Rock	249
Rock	250
Italiano	251
Italiano	252
Italiano	253
Italiano	254
Italiano	255
Italiano	256
Italiano	257
Italiano	258
Rock	251
Rock	252
Rock	253
Rock	254
Rock	255
Rock	256
Rock	257
Rock	258
Rock	259
Rock	260
Rock	261
Rock	262
Rock	263
Rock	264
Rock	265
Rock	266
Rock	267
Pop Rock	259
Pop Rock	260
Pop Rock	261
Pop Rock	262
Pop Rock	263
Pop Rock	264
Pop Rock	265
Pop Rock	266
Pop Rock	267
Italiano	259
Italiano	260
Italiano	261
Italiano	262
Italiano	263
Italiano	264
Italiano	265
Italiano	266
Italiano	267
Tedesco	268
Tedesco	269
Tedesco	270
Tedesco	271
Tedesco	272
Tedesco	273
Tedesco	274
Tedesco	275
Tedesco	276
Tedesco	277
Tedesco	278
Industrial Metal	268
Industrial Metal	269
Industrial Metal	270
Industrial Metal	271
Industrial Metal	272
Industrial Metal	273
Industrial Metal	274
Industrial Metal	275
Industrial Metal	276
Industrial Metal	277
Industrial Metal	278
Alternative Metal	268
Alternative Metal	269
Alternative Metal	270
Alternative Metal	271
Alternative Metal	272
Alternative Metal	273
Alternative Metal	274
Alternative Metal	275
Alternative Metal	276
Alternative Metal	277
Alternative Metal	278
Neue Deutsche Harte	268
Neue Deutsche Harte	269
Neue Deutsche Harte	270
Neue Deutsche Harte	271
Neue Deutsche Harte	272
Neue Deutsche Harte	273
Neue Deutsche Harte	274
Neue Deutsche Harte	275
Neue Deutsche Harte	276
Neue Deutsche Harte	277
Neue Deutsche Harte	278
Tedesco	279
Tedesco	280
Tedesco	281
Tedesco	282
Tedesco	283
Tedesco	284
Tedesco	285
Tedesco	286
Tedesco	287
Tedesco	288
Tedesco	289
Industrial Metal	279
Industrial Metal	280
Industrial Metal	281
Industrial Metal	282
Industrial Metal	283
Industrial Metal	284
Industrial Metal	285
Industrial Metal	286
Industrial Metal	287
Industrial Metal	288
Industrial Metal	289
Alternative Metal	279
Alternative Metal	280
Alternative Metal	281
Alternative Metal	282
Alternative Metal	283
Alternative Metal	284
Alternative Metal	285
Alternative Metal	286
Alternative Metal	287
Alternative Metal	288
Alternative Metal	289
Neue Deutsche Harte	279
Neue Deutsche Harte	280
Neue Deutsche Harte	281
Neue Deutsche Harte	282
Neue Deutsche Harte	283
Neue Deutsche Harte	284
Neue Deutsche Harte	285
Neue Deutsche Harte	286
Neue Deutsche Harte	287
Neue Deutsche Harte	288
Neue Deutsche Harte	289
Tedesco	290
Tedesco	291
Tedesco	292
Tedesco	293
Tedesco	294
Tedesco	295
Tedesco	296
Tedesco	297
Tedesco	298
Tedesco	299
Tedesco	300
Industrial Metal	290
Industrial Metal	291
Industrial Metal	292
Industrial Metal	293
Industrial Metal	294
Industrial Metal	295
Industrial Metal	296
Industrial Metal	297
Industrial Metal	298
Industrial Metal	299
Industrial Metal	300
Tedesco	301
Tedesco	302
Tedesco	303
Tedesco	304
Tedesco	305
Tedesco	306
Tedesco	307
Tedesco	308
Tedesco	309
Tedesco	310
Tedesco	311
Industrial Metal	301
Industrial Metal	302
Industrial Metal	303
Industrial Metal	304
Industrial Metal	305
Industrial Metal	306
Industrial Metal	307
Industrial Metal	308
Industrial Metal	309
Industrial Metal	310
Industrial Metal	311
Gothic Metal	301
Gothic Metal	302
Gothic Metal	303
Gothic Metal	304
Gothic Metal	305
Gothic Metal	306
Gothic Metal	307
Gothic Metal	308
Gothic Metal	309
Gothic Metal	310
Gothic Metal	311
Tedesco	312
Tedesco	313
Tedesco	314
Tedesco	315
Tedesco	316
Tedesco	317
Tedesco	318
Tedesco	319
Tedesco	320
Tedesco	321
Tedesco	322
Industrial Metal	312
Industrial Metal	313
Industrial Metal	314
Industrial Metal	315
Industrial Metal	316
Industrial Metal	317
Industrial Metal	318
Industrial Metal	319
Industrial Metal	320
Industrial Metal	321
Industrial Metal	322
Gothic Metal	312
Gothic Metal	313
Gothic Metal	314
Gothic Metal	315
Gothic Metal	316
Gothic Metal	317
Gothic Metal	318
Gothic Metal	319
Gothic Metal	320
Gothic Metal	321
Gothic Metal	322
Nu Metal	323
Nu Metal	324
Nu Metal	325
Nu Metal	326
Nu Metal	327
Nu Metal	328
Nu Metal	329
Nu Metal	330
Nu Metal	331
Nu Metal	332
Nu Metal	333
Nu Metal	334
Inglese	323
Inglese	324
Inglese	325
Inglese	326
Inglese	327
Inglese	328
Inglese	329
Inglese	330
Inglese	331
Inglese	332
Inglese	333
Inglese	334
Rap Metal	323
Rap Metal	324
Rap Metal	325
Rap Metal	326
Rap Metal	327
Rap Metal	328
Rap Metal	329
Rap Metal	330
Rap Metal	331
Rap Metal	332
Rap Metal	333
Rap Metal	334
Alternative Metal	323
Alternative Metal	324
Alternative Metal	325
Alternative Metal	326
Alternative Metal	327
Alternative Metal	328
Alternative Metal	329
Alternative Metal	330
Alternative Metal	331
Alternative Metal	332
Alternative Metal	333
Alternative Metal	334
Nu Metal	335
Nu Metal	336
Nu Metal	337
Nu Metal	338
Nu Metal	339
Nu Metal	340
Nu Metal	341
Nu Metal	342
Nu Metal	343
Nu Metal	344
Nu Metal	345
Nu Metal	346
Nu Metal	347
Pop	540
Inglese	335
Inglese	336
Inglese	337
Inglese	338
Inglese	339
Inglese	340
Inglese	341
Inglese	342
Inglese	343
Inglese	344
Inglese	345
Inglese	346
Inglese	347
Rap Rock	335
Rap Rock	336
Rap Rock	337
Rap Rock	338
Rap Rock	339
Rap Rock	340
Rap Rock	341
Rap Rock	342
Rap Rock	343
Rap Rock	344
Rap Rock	345
Rap Rock	346
Rap Rock	347
Alternative Metal	335
Alternative Metal	336
Alternative Metal	337
Alternative Metal	338
Alternative Metal	339
Alternative Metal	340
Alternative Metal	341
Alternative Metal	342
Alternative Metal	343
Alternative Metal	344
Alternative Metal	345
Alternative Metal	346
Alternative Metal	347
Alternative Rock	348
Alternative Rock	349
Alternative Rock	350
Alternative Rock	351
Alternative Rock	352
Alternative Rock	353
Alternative Rock	354
Alternative Rock	355
Alternative Rock	356
Alternative Rock	357
Alternative Rock	358
Alternative Rock	359
Inglese	348
Inglese	349
Inglese	350
Inglese	351
Inglese	352
Inglese	353
Inglese	354
Inglese	355
Inglese	356
Inglese	357
Inglese	358
Inglese	359
Experimental Rock	360
Experimental Rock	361
Experimental Rock	362
Experimental Rock	363
Experimental Rock	364
Experimental Rock	365
Experimental Rock	366
Experimental Rock	367
Experimental Rock	368
Experimental Rock	369
Experimental Rock	370
Experimental Rock	371
Experimental Rock	372
Experimental Rock	373
Experimental Rock	374
Rap Rock	360
Rap Rock	361
Rap Rock	362
Rap Rock	363
Rap Rock	364
Rap Rock	365
Rap Rock	366
Rap Rock	367
Rap Rock	368
Rap Rock	369
Rap Rock	370
Rap Rock	371
Rap Rock	372
Rap Rock	373
Rap Rock	374
Inglese	360
Inglese	361
Inglese	362
Inglese	363
Inglese	364
Inglese	365
Inglese	366
Inglese	367
Inglese	368
Inglese	369
Inglese	370
Inglese	371
Inglese	372
Inglese	373
Inglese	374
Alternative Rock	360
Alternative Rock	361
Alternative Rock	362
Alternative Rock	363
Alternative Rock	364
Alternative Rock	365
Alternative Rock	366
Alternative Rock	367
Alternative Rock	368
Alternative Rock	369
Alternative Rock	370
Alternative Rock	371
Alternative Rock	372
Alternative Rock	373
Alternative Rock	374
Electronic Rock	360
Electronic Rock	361
Electronic Rock	362
Electronic Rock	363
Electronic Rock	364
Electronic Rock	365
Electronic Rock	366
Electronic Rock	367
Electronic Rock	368
Electronic Rock	369
Electronic Rock	370
Electronic Rock	371
Electronic Rock	372
Electronic Rock	373
Electronic Rock	374
Inglese	375
Inglese	376
Inglese	377
Inglese	378
Inglese	379
Inglese	380
Inglese	381
Inglese	382
Inglese	383
Inglese	384
Inglese	385
Inglese	386
Alternative Rock	375
Alternative Rock	376
Alternative Rock	377
Alternative Rock	378
Alternative Rock	379
Alternative Rock	380
Alternative Rock	381
Alternative Rock	382
Alternative Rock	383
Alternative Rock	384
Alternative Rock	385
Alternative Rock	386
Electronic Rock	375
Electronic Rock	376
Electronic Rock	377
Electronic Rock	378
Electronic Rock	379
Electronic Rock	380
Electronic Rock	381
Electronic Rock	382
Electronic Rock	383
Electronic Rock	384
Electronic Rock	385
Electronic Rock	386
Rap Rock	375
Rap Rock	376
Rap Rock	377
Rap Rock	378
Rap Rock	379
Rap Rock	380
Rap Rock	381
Rap Rock	382
Rap Rock	383
Rap Rock	384
Rap Rock	385
Rap Rock	386
Pop	387
Pop	388
Pop	389
Pop	390
Pop	391
Pop	392
Pop	393
Pop	394
Italiano	387
Italiano	388
Italiano	389
Italiano	390
Italiano	391
Italiano	392
Italiano	393
Italiano	394
Italiano	395
Italiano	396
Italiano	397
Italiano	398
Italiano	399
Italiano	400
Italiano	401
Italiano	402
Italiano	403
Italiano	404
Pop	395
Pop	396
Pop	397
Pop	398
Pop	399
Pop	400
Pop	401
Pop	402
Pop	403
Pop	404
Italiano	405
Italiano	406
Italiano	407
Italiano	408
Italiano	409
Italiano	410
Italiano	411
Italiano	412
Italiano	413
Italiano	414
Italiano	415
Italiano	416
Pop	405
Pop	406
Pop	407
Pop	408
Pop	409
Pop	410
Pop	411
Pop	412
Pop	413
Pop	414
Pop	415
Pop	416
Italiano	417
Italiano	418
Italiano	419
Italiano	420
Italiano	421
Italiano	422
Italiano	423
Italiano	424
Italiano	425
Italiano	426
Italiano	427
Italiano	428
Inglese	429
Pop	417
Pop	418
Pop	419
Pop	420
Pop	421
Pop	422
Pop	423
Pop	424
Pop	425
Pop	426
Pop	427
Pop	428
Pop	429
Italiano	430
Italiano	431
Italiano	432
Italiano	433
Italiano	434
Italiano	435
Italiano	436
Italiano	437
Italiano	438
Italiano	439
Italiano	440
Italiano	441
Italiano	442
Inglese	443
Pop	430
Pop	431
Pop	432
Pop	433
Pop	434
Pop	435
Pop	436
Pop	437
Pop	438
Pop	439
Pop	440
Pop	441
Pop	442
Pop	443
Pop	444
Pop	445
Pop	446
Pop	447
Pop	448
Pop	449
Pop	450
Pop	451
Pop	452
Pop	453
Pop	454
Pop	455
Pop	456
Musica Classica	444
Musica Classica	445
Musica Classica	446
Musica Classica	447
Musica Classica	448
Musica Classica	449
Musica Classica	450
Musica Classica	451
Musica Classica	452
Musica Classica	453
Musica Classica	454
Musica Classica	455
Musica Classica	456
Italiano	444
Italiano	445
Italiano	446
Italiano	447
Italiano	448
Italiano	449
Italiano	450
Italiano	451
Italiano	452
Italiano	453
Italiano	454
Italiano	455
Italiano	456
Italiano	457
Italiano	458
Italiano	459
Italiano	460
Italiano	461
Inglese	462
Italiano	463
Italiano	464
Italiano	465
Italiano	466
Italiano	467
Pop	457
Pop	458
Pop	459
Pop	460
Pop	461
Pop	462
Pop	463
Pop	464
Pop	465
Pop	466
Pop	467
Musica Classica	468
Musica Classica	469
Musica Classica	470
Musica Classica	471
Musica Classica	472
Musica Classica	473
Musica Classica	474
Musica Classica	475
Musica Classica	476
Musica Classica	477
Musica Classica	478
Musica Classica	479
Musica Classica	480
Musica Classica	481
Musica Classica	482
Musica Classica	483
Italiano	468
Italiano	469
Italiano	470
Italiano	471
Italiano	472
Italiano	473
Italiano	474
Italiano	475
Italiano	476
Italiano	477
Italiano	478
Italiano	479
Italiano	480
Italiano	481
Italiano	482
Italiano	483
Italiano	484
Italiano	485
Italiano	486
Italiano	487
Italiano	488
Italiano	489
Italiano	490
Italiano	491
Italiano	492
Italiano	493
Italiano	494
Italiano	495
Italiano	496
Italiano	497
Italiano	498
Italiano	499
Italiano	500
Opera Lirica	484
Opera Lirica	485
Opera Lirica	486
Opera Lirica	487
Opera Lirica	488
Opera Lirica	489
Opera Lirica	490
Opera Lirica	491
Opera Lirica	492
Opera Lirica	493
Opera Lirica	494
Opera Lirica	495
Opera Lirica	496
Opera Lirica	497
Opera Lirica	498
Opera Lirica	499
Opera Lirica	500
Pop	501
Pop	502
Pop	503
Pop	504
Pop	505
Pop	506
Pop	507
Pop	508
Pop	509
Pop	510
Pop	511
Pop	512
Pop	513
Pop	514
Italiano	501
Inglese	502
Italiano	503
Italiano	504
Italiano	505
Italiano	506
Italiano	507
Italiano	508
Italiano	509
Italiano	510
Inglese	511
Italiano	512
Italiano	513
Italiano	514
Spagnolo	515
Spagnolo	516
Spagnolo	517
Spagnolo	518
Spagnolo	519
Spagnolo	520
Spagnolo	521
Spagnolo	522
Spagnolo	523
Spagnolo	524
Spagnolo	525
Musica Latina	515
Musica Latina	516
Musica Latina	517
Musica Latina	518
Musica Latina	519
Musica Latina	520
Musica Latina	521
Musica Latina	522
Musica Latina	523
Musica Latina	524
Musica Latina	525
Pop	515
Pop	516
Pop	517
Pop	518
Pop	519
Pop	520
Pop	521
Pop	522
Pop	523
Pop	524
Pop	525
Pop	526
Pop	527
Pop	528
Pop	529
Pop	530
Pop	531
Pop	532
Pop	533
Pop	534
Pop	535
Spagnolo	526
Spagnolo	527
Spagnolo	528
Spagnolo	529
Spagnolo	530
Spagnolo	531
Spagnolo	532
Spagnolo	533
Spagnolo	534
Inglese	535
Musica Latina	526
Musica Latina	527
Musica Latina	528
Musica Latina	529
Musica Latina	530
Musica Latina	531
Musica Latina	532
Musica Latina	533
Musica Latina	534
Musica Latina	535
Musica Latina	536
Musica Latina	537
Musica Latina	538
Musica Latina	539
Musica Latina	540
Musica Latina	541
Musica Latina	542
Musica Latina	543
Musica Latina	544
Musica Latina	545
Musica Latina	546
Musica Latina	547
Spagnolo	536
Spagnolo	537
Spagnolo	538
Spagnolo	539
Spagnolo	540
Spagnolo	541
Spagnolo	542
Spagnolo	543
Spagnolo	544
Spagnolo	545
Spagnolo	546
Spagnolo	547
Pop	536
Pop	537
Pop	538
Pop	539
Pop	541
Pop	542
Pop	543
Pop	544
Pop	545
Pop	546
Pop	547
Musica Latina	548
Musica Latina	549
Musica Latina	550
Musica Latina	551
Musica Latina	552
Musica Latina	553
Musica Latina	554
Musica Latina	555
Musica Latina	556
Musica Latina	557
Musica Latina	558
Musica Latina	559
Spagnolo	548
Spagnolo	549
Spagnolo	550
Spagnolo	551
Spagnolo	552
Spagnolo	553
Spagnolo	554
Spagnolo	555
Spagnolo	556
Spagnolo	557
Spagnolo	558
Spagnolo	559
Pop	548
Pop	549
Pop	550
Pop	551
Pop	552
Pop	553
Pop	554
Pop	555
Pop	556
Pop	557
Pop	558
Pop	559
Inglese	560
Inglese	561
Inglese	562
Inglese	563
Inglese	564
Spagnolo	565
Spagnolo	566
Inglese	567
Inglese	568
Spagnolo	569
Inglese	570
Spagnolo	571
Inglese	572
Spagnolo	573
Spagnolo	574
Pop Latino	560
Pop Latino	561
Pop Latino	562
Pop Latino	563
Pop Latino	564
Pop Latino	565
Pop Latino	566
Pop Latino	567
Pop Latino	568
Pop Latino	569
Pop Latino	570
Pop Latino	571
Pop Latino	572
Pop Latino	573
Pop Latino	574
\.


--
-- TOC entry 3426 (class 0 OID 16419)
-- Dependencies: 215
-- Data for Name: canzoni; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.canzoni (id_canzone, titolo, rilascio, durata, colore, id_artista) FROM stdin;
1	Hit the lights	1983-07-25	257	#ff0000	2
2	The four horsemen	1983-07-25	433	#ff0000	2
3	Motorbreath	1983-07-25	188	#ff0000	2
4	Jump in the fire	1983-07-25	281	#ff0000	2
5	(Anesthesia)-Pulling teeth	1983-07-25	254	#ff0000	2
6	Whiplash	1983-07-25	249	#ff0000	2
7	Phantom lord	1983-07-25	301	#ff0000	2
8	No remorse	1983-07-25	386	#ff0000	2
9	Seek & destroy	1983-07-25	415	#ff0000	2
10	Metal militia	1983-07-25	311	#ff0000	2
11	Fight fire with fire	1984-07-27	284	#ff4000	2
12	Ride the lightning	1984-07-27	397	#ff4000	2
13	For whom the bell tolls	1984-07-27	311	#ff4000	2
14	Fade to black	1984-07-27	415	#ff4000	2
15	Trapped under ice	1984-07-27	244	#ff4000	2
16	Escape	1984-07-27	264	#ff4000	2
17	Creeping death	1984-07-27	396	#ff4000	2
18	The call of ktulu	1984-07-27	535	#ff4000	2
19	Battery	1986-03-03	312	#ff8000	2
20	Master of puppets	1986-03-03	515	#ff8000	2
21	The thing that should not be	1986-03-03	396	#ff8000	2
22	Welcome home (Sanitarium)	1986-03-03	387	#ff8000	2
23	Disposable heroes	1986-03-03	496	#ff8000	2
24	Leper messiah	1986-03-03	340	#ff8000	2
25	Orion	1986-03-03	507	#ff8000	2
26	Damage, Inc.	1986-03-03	332	#ff8000	2
27	Blackened	1988-08-25	400	#ffbf00	2
28	... And justice for all	1988-08-25	586	#ffbf00	2
29	Eye of the beholder	1988-08-25	390	#ffbf00	2
30	One	1988-08-25	447	#ffbf00	2
31	The shortest straw	1988-08-25	395	#ffbf00	2
32	Harvester of sorrow	1988-08-25	345	#ffbf00	2
33	The frayed ends of sanity	1988-08-25	764	#ffbf00	2
34	To live is to die	1988-08-25	588	#ffbf00	2
35	Dyers eve	1988-08-25	313	#ffbf00	2
36	Enter sandman	1991-08-12	329	#ffff00	2
37	Sad but true	1991-08-12	324	#ffff00	2
38	Holler than thou	1991-08-12	227	#ffff00	2
39	The unforgiven	1991-08-12	386	#ffff00	2
40	Wherever I may roam	1991-08-12	402	#ffff00	2
41	Don't tread on me	1991-08-12	239	#ffff00	2
42	Through the never	1991-08-12	241	#ffff00	2
43	Nothing else matters	1991-08-12	389	#ffff00	2
44	Of wolf and man	1991-08-12	256	#ffff00	2
45	The god that failed	1991-08-12	305	#ffff00	2
46	My friend of misery	1991-08-12	407	#ffff00	2
47	The struggle within	1991-08-12	231	#ffff00	2
48	It's a beautiful day	1995-11-06	152	#bfff00	3
49	Made in heaven	1995-11-06	325	#bfff00	3
50	Let me live	1995-11-06	285	#bfff00	3
51	Mother love	1995-11-06	286	#bfff00	3
52	My life has been saved	1995-11-06	195	#bfff00	3
53	I was born to love you	1995-11-06	289	#bfff00	3
54	Heaven for everyone	1995-11-06	336	#bfff00	3
55	Too much love will kill you	1995-11-06	258	#bfff00	3
56	You don't fool me	1995-11-06	323	#bfff00	3
57	A winter's tale	1995-11-06	229	#bfff00	3
58	Party	1989-05-22	144	#80ff00	3
59	Khashoggi's ship	1989-05-22	148	#80ff00	3
60	The miracle	1989-05-22	302	#80ff00	3
61	I want it all	1989-05-22	281	#80ff00	3
62	The invisible man	1989-05-22	237	#80ff00	3
63	Breakthru	1989-05-22	248	#80ff00	3
64	Rain must fall	1989-05-22	263	#80ff00	3
65	Scandal	1989-05-22	282	#80ff00	3
66	My baby does me	1989-05-22	203	#80ff00	3
67	Was it all worth it	1989-05-22	345	#80ff00	3
68	Death on two legs (Dedicated to...)	1975-11-21	223	#40ff00	3
69	Lazing on a sunday afternoon	1975-11-21	67	#40ff00	3
70	I'm in love with my car	1975-11-21	185	#40ff00	3
71	You're my best friend	1975-11-21	172	#40ff00	3
72	'39	1975-11-21	211	#40ff00	3
73	Sweet lady	1975-11-21	244	#40ff00	3
74	Seaside rendezvous	1975-11-21	196	#40ff00	3
75	The prophet's song	1975-11-21	501	#40ff00	3
76	Love of my life	1975-11-21	219	#40ff00	3
77	Good company	1975-11-21	203	#40ff00	3
78	Bohemian rhapsody	1975-11-21	355	#40ff00	3
79	God save the queen	1975-11-21	75	#40ff00	3
80	We will rock you	1977-10-28	121	#00ff00	3
81	We are the champions	1977-10-28	177	#00ff00	3
82	Sheer heart attack	1977-10-28	204	#00ff00	3
83	All dead, all dead	1977-10-28	191	#00ff00	3
84	Spread your wings	1977-10-28	266	#00ff00	3
85	Fight from the inside	1977-10-28	183	#00ff00	3
86	Get down, aake love	1977-10-28	231	#00ff00	3
87	Sleeping on the sidewalk	1977-10-28	188	#00ff00	3
88	Who needs you	1977-10-28	186	#00ff00	3
89	It's late	1977-10-28	387	#00ff00	3
90	My melancholy blues	1977-10-28	209	#00ff00	3
91	Play the game	1980-06-30	213	#00ff40	3
92	Dragon attack	1980-06-30	259	#00ff40	3
93	Another one bites the dust	1980-06-30	212	#00ff40	3
94	Need your loving tonight	1980-06-30	169	#00ff40	3
95	Crazy little thing aalled love	1980-06-30	168	#00ff40	3
96	Rock it (Prime jive)	1980-06-30	273	#00ff40	3
97	Don't try suicide	1980-06-30	232	#00ff40	3
98	Sail away sweet sister (To the sister I never had)	1980-06-30	213	#00ff40	3
99	Coming soon	1980-06-30	171	#00ff40	3
100	Save me	1980-06-30	229	#00ff40	3
101	Welcome to the jungle	1987-07-21	281	#00ff80	4
102	It's so easy	1987-07-21	201	#00ff80	4
103	Nightrain	1987-07-21	266	#00ff80	4
104	Out ta get me	1987-07-21	260	#00ff80	4
105	Mr. Brownstone	1987-07-21	226	#00ff80	4
106	Paradise city	1987-07-21	406	#00ff80	4
107	My Michelle	1987-07-21	219	#00ff80	4
108	Think about you	1987-07-21	230	#00ff80	4
109	Sweet child o' mine	1987-07-21	355	#00ff80	4
110	You're crazy	1987-07-21	205	#00ff80	4
111	Anything goes	1987-07-21	205	#00ff80	4
112	Rocket queen	1987-07-21	373	#00ff80	4
113	Reckless life	1988-11-29	200	#00ffbf	4
114	Nice boys	1988-11-29	183	#00ffbf	4
115	Move to the city	1988-11-29	222	#00ffbf	4
116	Mama kin	1988-11-29	237	#00ffbf	4
117	Patience	1988-11-29	356	#00ffbf	4
118	Used to love her	1988-11-29	193	#00ffbf	4
119	You're crazy	1988-11-29	250	#00ffbf	4
120	One in a million	1988-11-29	370	#00ffbf	4
121	Right next door to hell	1991-09-17	182	#00ffff	4
122	Dust N' Bones	1991-09-17	298	#00ffff	4
123	Live and let die	1991-09-17	184	#00ffff	4
124	Don't cry	1991-09-17	284	#00ffff	4
125	Perfect crime	1991-09-17	143	#00ffff	4
126	You ain't the first	1991-09-17	156	#00ffff	4
127	Bad obsession	1991-09-17	328	#00ffff	4
128	Back off bitch	1991-09-17	303	#00ffff	4
129	Double talkin' jive	1991-09-17	203	#00ffff	4
130	November rain	1991-09-17	537	#00ffff	4
131	The garden	1991-09-17	322	#00ffff	4
132	Garden of Eden	1991-09-17	281	#00ffff	4
133	Don't damn me	1991-09-17	318	#00ffff	4
134	Bad apples	1991-09-17	268	#00ffff	4
135	Dead horse	1991-09-17	257	#00ffff	4
136	Coma	1991-09-17	613	#00ffff	4
137	Civil war	1991-09-17	463	#00bfff	4
138	14 years	1991-09-17	261	#00bfff	4
139	Yesterdays	1991-09-17	196	#00bfff	4
140	Knockin' on heaven's door	1991-09-17	337	#00bfff	4
141	Get in the ring	1991-09-17	341	#00bfff	4
142	Shotgun blues	1991-09-17	203	#00bfff	4
143	Breakdown	1991-09-17	424	#00bfff	4
144	Pretty tied up	1991-09-17	288	#00bfff	4
145	Locomotive	1991-09-17	522	#00bfff	4
146	So fine	1991-09-17	247	#00bfff	4
147	Estranged	1991-09-17	563	#00bfff	4
148	You could be mine	1991-09-17	344	#00bfff	4
149	Don't cry - Alternate lyrics	1991-09-17	284	#00bfff	4
150	My world	1991-09-17	84	#00bfff	4
151	Since I don't have you	1993-11-23	258	#0080ff	4
152	New rose	1993-11-23	158	#0080ff	4
153	Down on the farm	1993-11-23	208	#0080ff	4
154	Human being	1993-11-23	408	#0080ff	4
155	Raw power	1993-11-23	191	#0080ff	4
156	Ain't it fun	1993-11-23	305	#0080ff	4
157	Buick Makane	1993-11-23	160	#0080ff	4
158	Hair on the dog	1993-11-23	234	#0080ff	4
159	Attitude	1993-11-23	86	#0080ff	4
160	Black leather	1993-11-23	248	#0080ff	4
161	You can't put your arms around a memory	1993-11-23	215	#0080ff	4
162	I don't care about you	1993-11-23	291	#0080ff	4
163	Balliamo sul mondo	1990-05-11	273	#0040ff	5
164	Bambolina e barracuda	1990-05-11	314	#0040ff	5
165	Piccola stella senza cielo	1990-05-11	237	#0040ff	5
166	Marlon Brando e' sempre lui	1990-05-11	252	#0040ff	5
167	Non e' tempo per noi	1990-05-11	210	#0040ff	5
168	Bar Mario	1990-05-11	234	#0040ff	5
169	Sogni di Rock 'N' Roll	1990-05-11	237	#0040ff	5
170	Radio radianti	1990-05-11	206	#0040ff	5
171	Freddo come in questa palude	1990-05-11	66	#0040ff	5
172	Angelo nella nebbia	1990-05-11	299	#0040ff	5
173	Figlio d'un cane	1990-05-11	173	#0040ff	5
174	Il muro del suono	2013-11-26	270	#0000ff	5
175	Siamo chi siamo	2013-11-26	256	#0000ff	5
176	Il volume delle tue bugie	2013-11-26	240	#0000ff	5
177	La neve se ne frega	2013-11-26	212	#0000ff	5
178	Il sale della terra	2013-11-26	238	#0000ff	5
179	Capo spartivento	2013-11-26	41	#0000ff	5
180	Tu sei lei	2013-11-26	263	#0000ff	5
181	Nati per vivere (Adesso e qui)	2013-11-26	231	#0000ff	5
182	La terra trema, amore mio	2013-11-26	240	#0000ff	5
183	Per sempre	2013-11-26	232	#0000ff	5
184	Cio' che rimane di noi	2013-11-26	280	#0000ff	5
185	Il suono, il brutto e il cattivo	2013-11-26	40	#0000ff	5
186	Con la scusa del Rock'N'Roll	2013-11-26	207	#0000ff	5
187	Sono sempre i sogni a dare forma al mondo	2013-11-26	274	#0000ff	5
188	Vivo Morto o X	1995-09-21	257	#4000ff	5
189	Seduto in riva al fosso	1995-09-21	269	#4000ff	5
190	Buon compleanno, Elvis!	1995-09-21	246	#4000ff	5
191	La forza della banda	1995-09-21	261	#4000ff	5
192	Hai un momento, Dio?	1995-09-21	280	#4000ff	5
193	Rane a Rubiera blues	1995-09-21	63	#4000ff	5
194	Certe notti	1995-09-21	260	#4000ff	5
195	Viva!	1995-09-21	219	#4000ff	5
196	I ''ragazzi'' sono in giro	1995-09-21	262	#4000ff	5
197	Quella che non sei	1995-09-21	241	#4000ff	5
198	Non dovete badare al cantante	1995-09-21	216	#4000ff	5
199	Un figlio di nome Elvis	1995-09-21	241	#4000ff	5
200	Il cielo e' vuoto o il cielo e' pieno	1995-09-21	213	#4000ff	5
201	Leggero	1995-09-21	254	#4000ff	5
202	Ancora in piedi	1993-01-22	257	#8000ff	5
203	A.A.A. Qualcuno cercasi	1993-01-22	296	#8000ff	5
204	Ho messo via	1993-01-22	287	#8000ff	5
205	Dove fermano i treni	1993-01-22	204	#8000ff	5
206	I duri hanno due cuori	1993-01-22	249	#8000ff	5
207	La ballerina del carillon	1993-01-22	224	#8000ff	5
208	Prezoo	1993-01-22	40	#8000ff	5
209	Lo zoo e' qui	1993-01-22	239	#8000ff	5
210	Piccola citta' eterna	1993-01-22	305	#8000ff	5
211	Walter il mago	1993-01-22	259	#8000ff	5
212	Pane al pane	1993-01-22	216	#8000ff	5
213	Quando tocca a te	1993-01-22	334	#8000ff	5
214	Sopravvissuti e sopravviventi - Tema	1993-01-22	95	#8000ff	5
215	Intro	2005-09-16	67	#bf00ff	5
216	Il giorno dei giorni	2005-09-16	261	#bf00ff	5
217	Happy Hour	2005-09-16	254	#bf00ff	5
218	L'amore conta	2005-09-16	265	#bf00ff	5
219	Cosa vuoi che sia	2005-09-16	216	#bf00ff	5
220	Le donne lo sanno	2005-09-16	268	#bf00ff	5
221	Lettera a G	2005-09-16	321	#bf00ff	5
222	Vivere a orecchio	2005-09-16	240	#bf00ff	5
223	Giorno per giorno	2005-09-16	290	#bf00ff	5
224	E' piu' forte di me	2005-09-16	242	#bf00ff	5
225	Sono qui per l'amore	2005-09-16	288	#bf00ff	5
226	La nostra relazione	1978-05-25	180	#ff00ff	6
227	...E poi mi parli di una vita insieme	1978-05-25	267	#ff00ff	6
228	Silvia	1978-05-25	211	#ff00ff	6
229	Tu che dormivi piano (Volo' via)	1978-05-25	257	#ff00ff	6
230	Jenny e' pazza	1978-05-25	431	#ff00ff	6
231	Ambarabaciccicocco'	1978-05-25	240	#ff00ff	6
232	Ed il tempo crea noi	1978-05-25	208	#ff00ff	6
233	Ciao	1978-05-25	82	#ff00ff	6
234	Io non so piu' cosa fare	1979-04-30	238	#ff00bf	6
235	Fregato, fegato spappolato	1979-04-30	195	#ff00bf	6
236	Sballi ravvicinati del terzo tipo	1979-04-30	309	#ff00bf	6
237	(Per quello che ho da fare) faccio il militare	1979-04-30	271	#ff00bf	6
238	(Per quello che ho da fare) faccio il militare - Reprise	1979-04-30	36	#ff00bf	6
239	La strega (La diva del sabato sera)	1979-04-30	282	#ff00bf	6
240	Albachiara	1979-04-30	245	#ff00bf	6
241	Quindici anni fa	1979-04-30	310	#ff00bf	6
242	Va be' (Se proprio lo devo dire)	1979-04-30	189	#ff00bf	6
243	Non l'hai mica capito	1980-04-03	231	#ff0080	6
244	Colpa d'Alfredo	1980-04-03	297	#ff0080	6
245	Susanna	1980-04-03	207	#ff0080	6
246	Anima fragile	1980-04-03	224	#ff0080	6
247	Alibi	1980-04-03	330	#ff0080	6
248	Sensazioni forti	1980-04-03	241	#ff0080	6
249	Tropico del cancro	1980-04-03	324	#ff0080	6
250	Asilo ''Republic''	1980-04-03	108	#ff0080	6
251	Siamo solo noi	1981-04-09	355	#ff0040	6
252	Incredibile romantica	1981-04-09	260	#ff0040	6
253	Dimentichiamoci questa citta'	1981-04-09	260	#ff0040	6
254	Voglio andare al mare	1981-04-09	220	#ff0040	6
255	Brava	1981-04-09	278	#ff0040	6
256	Ieri ho sgozzato mio figlio	1981-04-09	202	#ff0040	6
257	Che ironia	1981-04-09	229	#ff0040	6
258	Valium	1981-04-09	216	#ff0040	6
259	Sono ancora in coma	1982-04-13	178	#ff0000	6
260	Cosa ti fai	1982-04-13	168	#ff0000	6
261	Ogni volta	1982-04-13	256	#ff0000	6
262	Vado al massimo	1982-04-13	251	#ff0000	6
263	Credi davvero	1982-04-13	290	#ff0000	6
264	Amore... Aiuto	1982-04-13	282	#ff0000	6
265	Canzone	1982-04-13	257	#ff0000	6
266	Splendida giornata	1982-04-13	263	#ff0000	6
267	La noia	1982-04-13	250	#ff0000	6
268	Wollt ihr das bett In flammen sehen?	1995-09-25	317	#ff4000	7
269	Der meister	1995-09-25	250	#ff4000	7
270	Weisses fleisch	1995-09-25	215	#ff4000	7
271	Asche zu asche	1995-09-25	231	#ff4000	7
272	Seemann	1995-09-25	288	#ff4000	7
273	Du riechst so gut	1995-09-25	289	#ff4000	7
274	Das alte leid	1995-09-25	344	#ff4000	7
275	Heirate mich	1995-09-25	284	#ff4000	7
276	Herzeleid	1995-09-25	221	#ff4000	7
277	Laichzeit	1995-09-25	260	#ff4000	7
278	Rammstein	1995-09-25	265	#ff4000	7
279	Sehnsucht	1997-08-22	246	#ff8000	7
280	Engel	1997-08-22	266	#ff8000	7
281	Tier	1997-08-22	229	#ff8000	7
282	Bestrafe mich	1997-08-22	217	#ff8000	7
283	Du hast	1997-08-22	237	#ff8000	7
284	Buck dich	1997-08-22	204	#ff8000	7
285	Spiel mit mir	1997-08-22	285	#ff8000	7
286	Klavier	1997-08-22	266	#ff8000	7
287	Alter mann	1997-08-22	266	#ff8000	7
288	Eifersucht	1997-08-22	217	#ff8000	7
289	Kuss mich (Fellfrosch)	1997-08-22	209	#ff8000	7
290	Mein herz brennt	2001-04-02	279	#ffbf00	7
291	Links	2001-04-02	216	#ffbf00	7
292	Sonne	2001-04-02	272	#ffbf00	7
293	Ich will	2001-04-02	217	#ffbf00	7
294	Feuer frei!	2001-04-02	188	#ffbf00	7
295	Mutter	2001-04-02	286	#ffbf00	7
296	Spieluhr	2001-04-02	286	#ffbf00	7
297	Zwitter	2001-04-02	257	#ffbf00	7
298	Rein raus	2001-04-02	189	#ffbf00	7
299	Adios	2001-04-02	228	#ffbf00	7
300	Nebel	2001-04-02	294	#ffbf00	7
301	Reise, reise	2004-09-27	285	#ffff00	7
302	Mein teil	2004-09-27	272	#ffff00	7
303	Dalai Lama	2004-09-27	338	#ffff00	7
304	Keine lust	2004-09-27	222	#ffff00	7
305	Los	2004-09-27	265	#ffff00	7
306	Amerika	2004-09-27	226	#ffff00	7
307	Moskau	2004-09-27	256	#ffff00	7
308	Morgenstern	2004-09-27	239	#ffff00	7
309	Stein um stein	2004-09-27	236	#ffff00	7
310	Ohne dich	2004-09-27	272	#ffff00	7
311	Amou	2004-09-27	290	#ffff00	7
312	Benzin	2005-08-28	226	#bfff00	7
313	Mann gegen mann	2005-08-28	231	#bfff00	7
314	Rosenrot	2005-08-28	235	#bfff00	7
315	Spring	2005-08-28	325	#bfff00	7
316	Wo bist du?	2005-08-28	236	#bfff00	7
317	Stirb nicht vor mir (Don't die before I do)	2005-08-28	246	#bfff00	7
318	Zerstoren	2005-08-28	329	#bfff00	7
319	Hilf mir	2005-08-28	284	#bfff00	7
320	Te quiero puta!	2005-08-28	236	#bfff00	7
321	Feuer und wasser	2005-08-28	313	#bfff00	7
322	Ein leid	2005-08-28	224	#bfff00	7
323	Papercut	2001-10-24	185	#80ff00	8
324	One step closer	2001-10-24	146	#80ff00	8
325	With you	2001-10-24	203	#80ff00	8
326	Points of authority	2001-10-24	200	#80ff00	8
327	Crawling	2001-10-24	209	#80ff00	8
328	Runaway	2001-10-24	184	#80ff00	8
329	By myself	2001-10-24	190	#80ff00	8
330	In the end	2001-10-24	216	#80ff00	8
331	A place for my head	2001-10-24	185	#80ff00	8
332	Forgotten	2001-10-24	195	#80ff00	8
333	Cure for the itch	2001-10-24	157	#80ff00	8
334	Pushing me away	2001-10-24	192	#80ff00	8
335	Foreword	2003-03-25	13	#40ff00	8
336	Don't stay	2003-03-25	187	#40ff00	8
337	Somewhere I belong	2003-03-25	213	#40ff00	8
338	Lying from you	2003-03-25	175	#40ff00	8
339	Hit the floor	2003-03-25	164	#40ff00	8
340	Easier to run	2003-03-25	204	#40ff00	8
341	Faint	2003-03-25	162	#40ff00	8
342	Figure 09	2003-03-25	197	#40ff00	8
343	Breaking the habit	2003-03-25	196	#40ff00	8
344	From the inside	2003-03-25	173	#40ff00	8
345	Nobody's listening	2003-03-25	178	#40ff00	8
346	Session	2003-03-25	143	#40ff00	8
347	Numb	2003-03-25	185	#40ff00	8
348	Wake	2007-05-15	103	#00ff00	8
349	Given up	2007-05-15	189	#00ff00	8
350	Leave out all the rest	2007-05-15	209	#00ff00	8
351	Bleed it out	2007-05-15	164	#00ff00	8
352	Shadow of the day	2007-05-15	249	#00ff00	8
353	What I've done	2007-05-15	205	#00ff00	8
354	Hands held high	2007-05-15	233	#00ff00	8
355	No more sorrow	2007-05-15	221	#00ff00	8
356	Valentine's day	2007-05-15	196	#00ff00	8
357	In between	2007-05-15	196	#00ff00	8
358	In pieces	2007-05-15	218	#00ff00	8
359	The little things give you away	2007-05-15	383	#00ff00	8
360	The requiem	2010-09-14	121	#00ff40	8
361	The radiance	2010-09-14	57	#00ff40	8
362	Burning in the skies	2010-09-14	253	#00ff40	8
363	Empty spaces	2010-09-14	18	#00ff40	8
364	When they come for me	2010-09-14	293	#00ff40	8
365	Robot boy	2010-09-14	269	#00ff40	8
366	Jornada del muerto	2010-09-14	94	#00ff40	8
367	Waiting for the end	2010-09-14	231	#00ff40	8
368	Blackout	2010-09-14	279	#00ff40	8
369	Wretches and kings	2010-09-14	250	#00ff40	8
370	Wisdom, justice, and love	2010-09-14	98	#00ff40	8
371	Iridescent	2010-09-14	296	#00ff40	8
372	Fallout	2010-09-14	83	#00ff40	8
373	The catalyst	2010-09-14	339	#00ff40	8
374	The messenger	2010-09-14	181	#00ff40	8
375	Lost in the echo	2012-06-26	205	#00ff80	8
376	In my remains	2012-06-26	200	#00ff80	8
377	Burn it down	2012-06-26	230	#00ff80	8
378	Lies greed misery	2012-06-26	146	#00ff80	8
379	I'll be gone	2012-06-26	211	#00ff80	8
380	Castle of glass	2012-06-26	205	#00ff80	8
381	Victimized	2012-06-26	106	#00ff80	8
382	Roads untraveled	2012-06-26	230	#00ff80	8
383	Skin to bone	2012-06-26	168	#00ff80	8
384	Until it breaks	2012-06-26	223	#00ff80	8
385	Tinfoil	2012-06-26	71	#00ff80	8
386	Powerless	2012-06-26	224	#00ff80	8
387	Non c'e'	1993-04-26	278	#00ffbf	9
388	Mi rubi l'anima	1993-04-26	199	#00ffbf	9
389	Dove sei	1993-04-26	217	#00ffbf	9
390	Baci che si rubano	1993-04-26	240	#00ffbf	9
391	Tutt'al piu'	1993-04-26	269	#00ffbf	9
392	La solitudine	1993-04-26	237	#00ffbf	9
393	Perche' non torna piu'	1993-04-26	277	#00ffbf	9
394	Il cuore non si arrende	1993-04-26	233	#00ffbf	9
395	Gente	1994-02-26	274	#00ffff	9
396	Lui non sta con te	1994-02-26	228	#00ffff	9
397	Strani amori	1994-02-26	256	#00ffff	9
398	Ragazze che	1994-02-26	260	#00ffff	9
399	Il coraggio che non c'e'	1994-02-26	278	#00ffff	9
400	Un amico e' cosi'	1994-02-26	246	#00ffff	9
401	Amori infiniti	1994-02-26	220	#00ffff	9
402	Cani e gatti	1994-02-26	305	#00ffff	9
403	Anni miei	1994-02-26	284	#00ffff	9
404	Lettera	1994-02-26	225	#00ffff	9
405	Le cose che vivi	1996-09-12	271	#00bfff	9
406	Ascolta il tuo cuore	1996-09-12	280	#00bfff	9
407	Incancellabile	1996-09-12	229	#00bfff	9
408	Seamisai	1996-09-12	218	#00bfff	9
409	Angeli nel blu	1996-09-12	317	#00bfff	9
410	Mi dispiace	1996-09-12	362	#00bfff	9
411	Due innamorati come noi	1996-09-12	281	#00bfff	9
412	Che storia e'	1996-09-12	253	#00bfff	9
413	16/5/74	1996-09-12	286	#00bfff	9
414	Un giorno senza te	1996-09-12	299	#00bfff	9
415	La voce	1996-09-12	295	#00bfff	9
416	Il mondo che vorrei	1996-09-12	253	#00bfff	9
417	La mia risposta	1998-10-15	222	#0080ff	9
418	Stanotte stai con me	1998-10-15	249	#0080ff	9
419	Un'emergenza d'amore	1998-10-15	270	#0080ff	9
420	Anna dimmi si'	1998-10-15	238	#0080ff	9
421	Una storia seria	1998-10-15	280	#0080ff	9
422	Come una danza	1998-10-15	319	#0080ff	9
423	Che bene mi fai	1998-10-15	261	#0080ff	9
424	In assenza di te	1998-10-15	271	#0080ff	9
425	Succede al cuore	1998-10-15	221	#0080ff	9
426	Tu cosa sogni?	1998-10-15	231	#0080ff	9
427	Buone verita'	1998-10-15	241	#0080ff	9
428	La felicita'	1998-10-15	236	#0080ff	9
429	Looking For An Angel	1998-10-15	254	#0080ff	9
430	Siamo noi	2000-09-15	235	#0040ff	9
431	Volevo dirti che ti amo	2000-09-16	244	#0040ff	9
432	Il mio sbaglio piu' grande	2000-09-17	185	#0040ff	9
433	Tra te e il mare	2000-09-18	229	#0040ff	9
434	Viaggio con te	2000-09-19	229	#0040ff	9
435	Musica sara'	2000-09-20	203	#0040ff	9
436	Anche se non mi vuoi	2000-09-21	236	#0040ff	9
437	Fidati di me	2000-09-22	229	#0040ff	9
438	Ricordami	2000-09-23	248	#0040ff	9
439	Per vivere	2000-09-24	245	#0040ff	9
440	Mentre la notte va	2000-09-25	210	#0040ff	9
441	Come si fa	2000-09-26	250	#0040ff	9
442	Jenny	2000-09-27	266	#0040ff	9
443	The Extra Mile	2000-09-28	248	#0040ff	9
444	Il mare calmo della sera	1994-01-01	343	#0000ff	10
445	Ave Maria No Morro	1994-01-01	340	#0000ff	10
446	Vivere	1994-01-01	242	#0000ff	10
447	Rapsodia	1994-01-01	322	#0000ff	10
448	La Luna che non c'e'	1994-01-01	275	#0000ff	10
449	Caruso	1994-01-01	304	#0000ff	10
450	Miserere	1994-01-01	249	#0000ff	10
451	Panis Angelicus	1994-01-01	287	#0000ff	10
452	Ah, la paterna mano	1994-01-01	325	#0000ff	10
453	E lucevan le stelle	1994-01-01	252	#0000ff	10
454	La fleur que tu m'avais jetee	1994-01-01	326	#0000ff	10
455	L'anima ho stanca	1994-01-01	336	#0000ff	10
456	Sogno	1994-01-01	295	#0000ff	10
457	Con te partiro'	1995-11-13	249	#4000ff	10
458	Per amore	1995-11-13	281	#4000ff	10
459	Macchina da guerra	1995-11-13	248	#4000ff	10
460	E chiove	1995-11-13	261	#4000ff	10
461	Romanza	1995-11-13	221	#4000ff	10
462	The Power Of Love	1995-11-13	321	#4000ff	10
463	Vivo per lei	1995-11-13	263	#4000ff	10
464	Le tue parole	1995-11-13	237	#4000ff	10
465	Sempre sempre	1995-11-13	258	#4000ff	10
466	Voglio restare cosi'	1995-11-13	231	#4000ff	10
467	Vivo per lei - Ich lebe fur sie	1995-11-13	334	#4000ff	10
468	Nessun dorma	1996-01-01	307	#8000ff	10
469	Il lamento di Federico	1996-01-01	249	#8000ff	10
470	Ah, la paterna mano	1996-01-01	325	#8000ff	10
471	La donna e' mobile	1996-01-01	260	#8000ff	10
472	Una furtiva lagrima	1996-01-01	351	#8000ff	10
473	Panis Angelicus	1996-01-01	287	#8000ff	10
474	Ave Maria	1996-01-01	254	#8000ff	10
475	O sole mio	1996-01-01	274	#8000ff	10
476	Core 'ngrato	1996-01-01	331	#8000ff	10
477	Santa Lucia luntana	1996-01-01	353	#8000ff	10
478	I te vurria vasa'	1996-01-01	263	#8000ff	10
479	Tu, ca nun chiagne	1996-01-01	355	#8000ff	10
480	O marenariello	1996-01-01	241	#8000ff	10
481	Piscatore 'e Pusilleco	1996-01-01	265	#8000ff	10
482	Messaggio Bocelli	1996-01-01	291	#8000ff	10
483	Adeste fidelis	1996-01-01	267	#8000ff	10
484	Questa o quella	1998-01-01	249	#bf00ff	10
485	Che gelida manina	1998-01-01	341	#bf00ff	10
486	Recondita armonia	1998-01-01	331	#bf00ff	10
487	E lucevan le stelle	1998-01-01	252	#bf00ff	10
488	Addio, fiorito asil	1998-01-01	344	#bf00ff	10
489	Come un bel di' di maggio	1998-01-01	249	#bf00ff	10
490	A te, o cara	1998-01-01	288	#bf00ff	10
491	Di rigori armato il seno	1998-01-01	267	#bf00ff	10
492	Amor ti vieta	1998-01-01	257	#bf00ff	10
493	Ch'ella mi creda libero	1998-01-01	306	#bf00ff	10
494	Cielo e mar!	1998-01-01	335	#bf00ff	10
495	La dolcissima effige	1998-01-01	354	#bf00ff	10
496	Musetta!... Testa adorata	1998-01-01	300	#bf00ff	10
497	Tombe degli avi miei	1998-01-01	290	#bf00ff	10
498	Puourquoi me reveiller	1998-01-01	304	#bf00ff	10
499	La fleur que tu m'avais jetee	1998-01-01	326	#bf00ff	10
500	Pour mon ame	1998-01-01	329	#bf00ff	10
501	Canto della Terra	1999-04-06	242	#ff00ff	10
502	The prayer	1999-04-06	250	#ff00ff	10
503	Sogno	1999-04-06	243	#ff00ff	10
504	O mare e tu	1999-04-06	276	#ff00ff	10
505	A volte il cuore	1999-04-06	284	#ff00ff	10
506	Cantico	1999-04-06	241	#ff00ff	10
507	Mai piu' cosi' lontano	1999-04-06	260	#ff00ff	10
508	Immenso	1999-04-06	291	#ff00ff	10
509	Nel cuore lei	1999-04-06	228	#ff00ff	10
510	Tremo e t'amo	1999-04-06	291	#ff00ff	10
511	I Love Rossini	1999-04-06	236	#ff00ff	10
512	Un canto	1999-04-06	275	#ff00ff	10
513	Come un fiume tu	1999-04-06	287	#ff00ff	10
514	A mio padre (6 maggio 1992)	1999-04-06	240	#ff00ff	10
515	Fuego contra fuego	1991-11-26	255	#ff00bf	11
516	Dime que me quires	1991-11-26	196	#ff00bf	11
517	Vuelo	1991-11-26	231	#ff00bf	11
518	Conmigo nadie puede	1991-11-26	198	#ff00bf	11
519	Te voy a conquistar	1991-11-26	255	#ff00bf	11
520	Juego de Ajedrez	1991-11-26	163	#ff00bf	11
521	Corazon entre nubes	1991-11-26	219	#ff00bf	11
522	Ser Feliz	1991-11-26	278	#ff00bf	11
523	El amor de mi vida	1991-11-26	297	#ff00bf	11
524	Susana	1991-11-26	294	#ff00bf	11
525	Popotitos	1991-11-26	198	#ff00bf	11
526	No me pidas mas	1993-05-25	209	#ff0080	11
527	Es mejor decirse adios	1993-05-25	205	#ff0080	11
528	Entre el amor y los Halagos	1993-05-25	258	#ff0080	11
529	Lo que nos pase, pasara	1993-05-25	232	#ff0080	11
530	Ella es	1993-05-25	282	#ff0080	11
531	Me amaras	1993-05-25	269	#ff0080	11
532	Ayudame	1993-05-25	250	#ff0080	11
533	Eres come el aire	1993-05-25	246	#ff0080	11
534	Que dia es hoy	1993-05-25	265	#ff0080	11
535	Hooray! Hooray! It's a Holi-Holiday	1993-05-25	190	#ff0080	11
536	Por arriba, por abajo	1998-02-10	358	#ff0000	11
537	Lola, lola	1998-02-10	326	#ff0000	11
538	Casi un bolero	1998-02-10	357	#ff0000	11
539	Corazonado	1998-02-10	339	#ff0000	11
540	La bomba	1998-02-10	349	#ff0000	11
541	Vuelve	1998-02-10	298	#ff0000	11
542	Hagamos el amor	1998-02-10	354	#ff0000	11
543	La copa de la vida	1998-02-10	342	#ff0000	11
544	Perdido sin ti	1998-02-10	266	#ff0000	11
545	Asi es la vida	1998-02-10	308	#ff0000	11
546	Marcia baila	1998-02-10	338	#ff0000	11
547	No importa la distancia	1998-02-10	242	#ff0000	11
548	Fuego de noche, nieve de dia	1995-09-12	330	#ff0040	11
549	A medio vivir	1995-09-12	282	#ff0040	11
550	(Un, dos, tres) Maria	1995-09-12	263	#ff0040	11
551	Te extrano, te olvido, te amo	1995-09-12	281	#ff0040	11
552	Donde estaras?	1995-09-12	232	#ff0040	11
553	Volveras	1995-09-12	292	#ff0040	11
554	Revolucion	1995-09-12	230	#ff0040	11
555	Somos la semilla	1995-09-12	236	#ff0040	11
556	Como decirte adios?	1995-09-12	180	#ff0040	11
557	Bombon de azucar	1995-09-12	298	#ff0040	11
558	Corazon	1995-09-12	260	#ff0040	11
559	Nada es imposible	1995-09-12	262	#ff0040	11
560	She bangs	2000-12-26	281	#ff4000	11
561	Saint Tropez	2000-12-26	288	#ff4000	11
562	Come to me	2000-12-26	273	#ff4000	11
563	Loaded	2000-12-26	233	#ff4000	11
564	Nobody wants to be lonely	2000-12-26	305	#ff4000	11
565	Amor	2000-12-26	207	#ff4000	11
566	Jezabel	2000-12-26	229	#ff4000	11
567	The touch	2000-12-26	267	#ff4000	11
568	One night man	2000-12-26	228	#ff4000	11
569	She Bangs (Spanish Version)	2000-12-26	277	#ff4000	11
570	Are you in it for love	2000-12-26	246	#ff4000	11
571	Ven a mi	2000-12-26	274	#ff4000	11
572	If you ever saw her	2000-12-26	229	#ff4000	11
573	Dame mas	2000-12-26	233	#ff4000	11
574	Cambia la pie!	2000-12-26	313	#ff4000	11
\.


--
-- TOC entry 3427 (class 0 OID 16425)
-- Dependencies: 216
-- Data for Name: contenuto; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.contenuto (id_album, id_canzone) FROM stdin;
1	1
1	2
1	3
1	4
1	5
1	6
1	7
1	8
1	9
1	10
2	11
2	12
2	13
2	14
2	15
2	16
2	17
2	18
3	19
3	20
3	21
3	22
3	23
3	24
3	25
3	26
4	27
4	28
4	29
4	30
4	31
4	32
4	33
4	34
4	35
5	36
5	37
5	38
5	39
5	40
5	41
5	42
5	43
5	44
5	45
5	46
5	47
6	48
6	49
6	50
6	51
6	52
6	53
6	54
6	55
6	56
6	57
7	58
7	59
7	60
7	61
7	62
7	63
7	64
7	65
7	66
7	67
8	68
8	69
8	70
8	71
8	72
8	73
8	74
8	75
8	76
8	77
8	78
8	79
9	80
9	81
9	82
9	83
9	84
9	85
9	86
9	87
9	88
9	89
9	90
10	91
10	92
10	93
10	94
10	95
10	96
10	97
10	98
10	99
10	100
11	101
11	102
11	103
11	104
11	105
11	106
11	107
11	108
11	109
11	110
11	111
11	112
12	113
12	114
12	115
12	116
12	117
12	118
12	119
12	120
13	121
13	122
13	123
13	124
13	125
13	126
13	127
13	128
13	129
13	130
13	131
13	132
13	133
13	134
13	135
13	136
14	137
14	138
14	139
14	140
14	141
14	142
14	143
14	144
14	145
14	146
14	147
14	148
14	149
14	150
15	151
15	152
15	153
15	154
15	155
15	156
15	157
15	158
15	159
15	160
15	161
15	162
16	163
16	164
16	165
16	166
16	167
16	168
16	169
16	170
16	171
16	172
16	173
17	174
17	175
17	176
17	177
17	178
17	179
17	180
17	181
17	182
17	183
17	184
17	185
17	186
17	187
18	188
18	189
18	190
18	191
18	192
18	193
18	194
18	195
18	196
18	197
18	198
18	199
18	200
18	201
19	202
19	203
19	204
19	205
19	206
19	207
19	208
19	209
19	210
19	211
19	212
19	213
19	214
20	215
20	216
20	217
20	218
20	219
20	220
20	221
20	222
20	223
20	224
20	225
21	226
21	227
21	228
21	229
21	230
21	231
21	232
21	233
22	234
22	235
22	236
22	237
22	238
22	239
22	240
22	241
22	242
23	243
23	244
23	245
23	246
23	247
23	248
23	249
23	250
24	251
24	252
24	253
24	254
24	255
24	256
24	257
24	258
25	259
25	260
25	261
25	262
25	263
25	264
25	265
25	266
25	267
26	268
26	269
26	270
26	271
26	272
26	273
26	274
26	275
26	276
26	277
26	278
27	279
27	280
27	281
27	282
27	283
27	284
27	285
27	286
27	287
27	288
27	289
28	290
28	291
28	292
28	293
28	294
28	295
28	296
28	297
28	298
28	299
28	300
29	301
29	302
29	303
29	304
29	305
29	306
29	307
29	308
29	309
29	310
29	311
30	312
30	313
30	314
30	315
30	316
30	317
30	318
30	319
30	320
30	321
30	322
31	323
31	324
31	325
31	326
31	327
31	328
31	329
31	330
31	331
31	332
31	333
31	334
32	335
32	336
32	337
32	338
32	339
32	340
32	341
32	342
32	343
32	344
32	345
32	346
32	347
33	348
33	349
33	350
33	351
33	352
33	353
33	354
33	355
33	356
33	357
33	358
33	359
34	360
34	361
34	362
34	363
34	364
34	365
34	366
34	367
34	368
34	369
34	370
34	371
34	372
34	373
34	374
35	375
35	376
35	377
35	378
35	379
35	380
35	381
35	382
35	383
35	384
35	385
35	386
36	387
36	388
36	389
36	390
36	391
36	392
36	393
36	394
37	395
37	396
37	397
37	398
37	399
37	400
37	401
37	402
37	403
37	404
38	405
38	406
38	407
38	408
38	409
38	410
38	411
38	412
38	413
38	414
38	415
38	416
39	417
39	418
39	419
39	420
39	421
39	422
39	423
39	424
39	425
39	426
39	427
39	428
39	429
40	430
40	431
40	432
40	433
40	434
40	435
40	436
40	437
40	438
40	439
40	440
40	441
40	442
40	443
41	444
41	445
41	446
41	447
41	448
41	449
41	450
41	451
41	452
41	453
41	454
41	455
41	456
42	457
42	458
42	459
42	460
42	461
42	462
42	463
42	464
42	465
42	466
42	467
43	468
43	469
43	470
43	471
43	472
43	473
43	474
43	475
43	476
43	477
43	478
43	479
43	480
43	481
43	482
43	483
44	484
44	485
44	486
44	487
44	488
44	489
44	490
44	491
44	492
44	493
44	494
44	495
44	496
44	497
44	498
44	499
44	500
45	501
45	502
45	503
45	504
45	505
45	506
45	507
45	508
45	509
45	510
45	511
45	512
45	513
45	514
46	515
46	516
46	517
46	518
46	519
46	520
46	521
46	522
46	523
46	524
46	525
47	526
47	527
47	528
47	529
47	530
47	531
47	532
47	533
47	534
47	535
48	536
48	537
48	538
48	539
48	540
48	541
48	542
48	543
48	544
48	545
48	546
48	547
49	548
49	549
49	550
49	551
49	552
49	553
49	554
49	555
49	556
49	557
49	558
49	559
50	560
50	561
50	562
50	563
50	564
50	565
50	566
50	567
50	568
50	569
50	570
50	571
50	572
50	573
50	574
\.


--
-- TOC entry 3429 (class 0 OID 16429)
-- Dependencies: 218
-- Data for Name: playlist; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.playlist (id_utente, nome, descrizione, n_canzoni, id_playlist) FROM stdin;
12	Metallo	Void	47	1
\.


--
-- TOC entry 3430 (class 0 OID 16436)
-- Dependencies: 219
-- Data for Name: raccolte; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.raccolte (id_playlist, id_canzone) FROM stdin;
1	1
1	2
1	3
1	4
1	5
1	6
1	7
1	8
1	9
1	10
1	11
1	12
1	13
1	14
1	15
1	16
1	17
1	18
1	19
1	20
1	21
1	22
1	23
1	24
1	25
1	26
1	27
1	28
1	29
1	30
1	31
1	32
1	33
1	34
1	35
1	36
1	37
1	38
1	39
1	40
1	41
1	42
1	43
1	44
1	45
1	46
1	47
\.


--
-- TOC entry 3432 (class 0 OID 16440)
-- Dependencies: 221
-- Data for Name: statistiche; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.statistiche (id_statistica, _13_19, _20_29, _30_39, _40_49, _50_65, _65piu, n_riproduzioni_totali, n_riproduzioni_settimanali) FROM stdin;
1	0	1	0	0	0	0	766898	162040
2	0	1	0	0	0	0	531479	812583
3	0	1	0	0	0	0	110956	13730
4	0	1	0	0	0	0	245976	741346
5	0	1	0	0	0	0	421629	853187
6	0	1	0	0	0	0	963745	399264
7	0	1	0	0	0	0	663607	626004
8	0	1	0	0	0	0	29788	639495
9	0	1	0	0	0	0	24625	660685
10	0	1	0	0	0	0	509691	211069
11	0	1	0	0	0	0	613339	867879
12	0	1	0	0	0	0	401971	97565
13	0	1	0	0	0	0	996372	675959
14	0	1	0	0	0	0	907880	386762
15	0	1	0	0	0	0	262786	427410
16	0	1	0	0	0	0	321060	799821
17	0	1	0	0	0	0	860654	551074
18	0	1	0	0	0	0	752609	289511
19	0	1	0	0	0	0	872222	19850
20	0	1	0	0	0	0	989120	481258
21	0	1	0	0	0	0	585275	788396
22	0	1	0	0	0	0	710192	828549
23	0	1	0	0	0	0	167719	648732
24	0	1	0	0	0	0	2463	518609
25	0	1	0	0	0	0	54244	747435
26	0	1	0	0	0	0	500281	587174
27	0	1	0	0	0	0	487968	483978
28	0	1	0	0	0	0	249805	422606
29	0	1	0	0	0	0	427605	366460
30	0	1	0	0	0	0	422616	550701
31	0	1	0	0	0	0	709405	768784
32	0	1	0	0	0	0	285410	287464
33	0	1	0	0	0	0	37952	770138
34	0	1	0	0	0	0	617079	636289
35	0	1	0	0	0	0	514557	548360
36	0	1	0	0	0	0	537011	77708
37	0	1	0	0	0	0	50561	802361
38	0	1	0	0	0	0	526104	764032
39	0	1	0	0	0	0	904427	65552
40	0	1	0	0	0	0	19308	588384
41	0	1	0	0	0	0	279348	758145
42	0	1	0	0	0	0	586926	724387
43	0	1	0	0	0	0	817243	597599
44	0	1	0	0	0	0	251756	566244
45	0	1	0	0	0	0	297778	527997
46	0	1	0	0	0	0	707514	691588
47	0	1	0	0	0	0	491897	788567
48	0	0	0	0	0	0	389658	461682
49	0	0	0	0	0	0	811379	154905
50	0	0	0	0	0	0	480237	874257
51	0	0	0	0	0	0	244864	417960
52	0	0	0	0	0	0	356805	26870
53	0	0	0	0	0	0	495742	846188
54	0	0	0	0	0	0	77130	184269
55	0	0	0	0	0	0	256132	443341
56	0	0	0	0	0	0	686295	907869
57	0	0	0	0	0	0	817351	719265
58	0	0	0	0	0	0	713824	14205
59	0	0	0	0	0	0	120845	395972
60	0	0	0	0	0	0	919645	450025
61	0	0	0	0	0	0	654338	715800
62	0	0	0	0	0	0	611107	476809
63	0	0	0	0	0	0	982382	103052
64	0	0	0	0	0	0	131640	555464
65	0	0	0	0	0	0	655664	11307
66	0	0	0	0	0	0	988770	966064
67	0	0	0	0	0	0	855868	797552
68	0	0	0	0	0	0	681261	714050
69	0	0	0	0	0	0	352956	417841
70	0	0	0	0	0	0	203290	766970
71	0	0	0	0	0	0	402667	199899
72	0	0	0	0	0	0	149251	850409
73	0	0	0	0	0	0	641929	853136
74	0	0	0	0	0	0	564127	827831
75	0	0	0	0	0	0	63412	468191
76	0	0	0	0	0	0	456612	560756
77	0	0	0	0	0	0	91196	218
78	0	0	0	0	0	0	549379	619146
79	0	0	0	0	0	0	334708	392523
80	0	0	0	0	0	0	349961	502915
81	0	0	0	0	0	0	190265	420461
82	0	0	0	0	0	0	535571	43923
83	0	0	0	0	0	0	115498	836729
84	0	0	0	0	0	0	309521	91871
85	0	0	0	0	0	0	434965	76024
86	0	0	0	0	0	0	938282	666291
87	0	0	0	0	0	0	113737	571112
88	0	0	0	0	0	0	427196	173778
89	0	0	0	0	0	0	612184	527351
90	0	0	0	0	0	0	472632	699002
91	0	0	0	0	0	0	562100	905748
92	0	0	0	0	0	0	672649	791316
93	0	0	0	0	0	0	898821	39269
94	0	0	0	0	0	0	320779	322871
95	0	0	0	0	0	0	778813	722982
96	0	0	0	0	0	0	567162	901419
97	0	0	0	0	0	0	757400	536840
98	0	0	0	0	0	0	483951	33321
99	0	0	0	0	0	0	813357	98960
100	0	0	0	0	0	0	47505	651465
101	0	0	0	0	0	0	19798	261213
102	0	0	0	0	0	0	609097	840461
103	0	0	0	0	0	0	177523	991904
104	0	0	0	0	0	0	941523	547785
105	0	0	0	0	0	0	17915	581150
106	0	0	0	0	0	0	838302	390118
107	0	0	0	0	0	0	971002	161067
108	0	0	0	0	0	0	842197	750327
109	0	0	0	0	0	0	275371	529524
110	0	0	0	0	0	0	337414	984042
111	0	0	0	0	0	0	801870	879977
112	0	0	0	0	0	0	992017	17896
113	0	0	0	0	0	0	187017	381316
114	0	0	0	0	0	0	691476	110762
115	0	0	0	0	0	0	736660	929853
116	0	0	0	0	0	0	605977	74560
117	0	0	0	0	0	0	74520	52907
118	0	0	0	0	0	0	768044	366982
119	0	0	0	0	0	0	266153	82217
120	0	0	0	0	0	0	903788	593980
121	0	0	0	0	0	0	518509	81781
122	0	0	0	0	0	0	571099	672942
123	0	0	0	0	0	0	900739	572886
124	0	0	0	0	0	0	392056	85994
125	0	0	0	0	0	0	264139	666717
126	0	0	0	0	0	0	173456	345603
127	0	0	0	0	0	0	589061	351833
128	0	0	0	0	0	0	384779	691803
129	0	0	0	0	0	0	103292	167820
130	0	0	0	0	0	0	75783	267888
131	0	0	0	0	0	0	481088	530063
132	0	0	0	0	0	0	844230	671584
133	0	0	0	0	0	0	583079	673380
134	0	0	0	0	0	0	285217	845607
135	0	0	0	0	0	0	697555	750964
136	0	0	0	0	0	0	787920	492198
137	0	0	0	0	0	0	132032	653025
138	0	0	0	0	0	0	734507	778120
139	0	0	0	0	0	0	531598	534691
140	0	0	0	0	0	0	707014	114496
141	0	0	0	0	0	0	295943	945552
142	0	0	0	0	0	0	476231	313813
143	0	0	0	0	0	0	438697	144449
144	0	0	0	0	0	0	739772	56878
145	0	0	0	0	0	0	348170	333309
146	0	0	0	0	0	0	864495	138286
147	0	0	0	0	0	0	587814	919506
148	0	0	0	0	0	0	635555	99548
149	0	0	0	0	0	0	94623	805608
150	0	0	0	0	0	0	776983	486802
151	0	0	0	0	0	0	229073	796456
152	0	0	0	0	0	0	578401	252513
153	0	0	0	0	0	0	563171	180927
154	0	0	0	0	0	0	716877	445620
155	0	0	0	0	0	0	638195	31452
156	0	0	0	0	0	0	139100	139523
157	0	0	0	0	0	0	988782	469302
158	0	0	0	0	0	0	932648	647449
159	0	0	0	0	0	0	98755	143913
160	0	0	0	0	0	0	163543	98285
161	0	0	0	0	0	0	977011	249140
162	0	0	0	0	0	0	244333	633243
163	0	0	0	0	0	0	25362	604757
164	0	0	0	0	0	0	403224	95541
165	0	0	0	0	0	0	242760	83187
166	0	0	0	0	0	0	647723	606444
167	0	0	0	0	0	0	6582	366852
168	0	0	0	0	0	0	903528	898053
169	0	0	0	0	0	0	65245	256285
170	0	0	0	0	0	0	759418	722957
171	0	0	0	0	0	0	941376	219669
172	0	0	0	0	0	0	450323	668427
173	0	0	0	0	0	0	456681	158133
174	0	0	0	0	0	0	572182	230475
175	0	0	0	0	0	0	233659	126815
176	0	0	0	0	0	0	779503	309128
177	0	0	0	0	0	0	49874	501068
178	0	0	0	0	0	0	193868	559745
179	0	0	0	0	0	0	513404	112221
180	0	0	0	0	0	0	367442	64362
181	0	0	0	0	0	0	972096	942441
182	0	0	0	0	0	0	312222	506689
183	0	0	0	0	0	0	962281	740898
184	0	0	0	0	0	0	524708	900485
185	0	0	0	0	0	0	194398	226269
186	0	0	0	0	0	0	65490	872355
187	0	0	0	0	0	0	442043	298115
188	0	0	0	0	0	0	165509	261006
189	0	0	0	0	0	0	275458	206912
190	0	0	0	0	0	0	745694	75229
191	0	0	0	0	0	0	818766	201996
192	0	0	0	0	0	0	330419	61724
193	0	0	0	0	0	0	729485	146613
194	0	0	0	0	0	0	851598	441738
195	0	0	0	0	0	0	959252	920306
196	0	0	0	0	0	0	113485	373562
197	0	0	0	0	0	0	105986	742549
198	0	0	0	0	0	0	112022	763323
199	0	0	0	0	0	0	175736	526934
200	0	0	0	0	0	0	296598	893607
201	0	0	0	0	0	0	292715	613816
202	0	0	0	0	0	0	493382	696699
203	0	0	0	0	0	0	529798	500315
204	0	0	0	0	0	0	875055	926571
205	0	0	0	0	0	0	736098	907167
206	0	0	0	0	0	0	752014	441636
207	0	0	0	0	0	0	98270	308268
208	0	0	0	0	0	0	258454	767831
209	0	0	0	0	0	0	827536	451200
210	0	0	0	0	0	0	748923	248687
211	0	0	0	0	0	0	677330	536165
212	0	0	0	0	0	0	254888	385129
213	0	0	0	0	0	0	626899	700230
214	0	0	0	0	0	0	36658	757788
215	0	0	0	0	0	0	61388	811958
216	0	0	0	0	0	0	660737	478626
217	0	0	0	0	0	0	276414	71878
218	0	0	0	0	0	0	699960	743775
219	0	0	0	0	0	0	267204	669755
220	0	0	0	0	0	0	156335	698555
221	0	0	0	0	0	0	874042	475859
222	0	0	0	0	0	0	716786	436243
223	0	0	0	0	0	0	808072	458059
224	0	0	0	0	0	0	618811	327676
225	0	0	0	0	0	0	993537	655917
226	0	0	0	0	0	0	261986	492708
227	0	0	0	0	0	0	503622	645622
228	0	0	0	0	0	0	147254	896093
229	0	0	0	0	0	0	355563	73480
230	0	0	0	0	0	0	384508	984587
231	0	0	0	0	0	0	169723	101133
232	0	0	0	0	0	0	220965	964893
233	0	0	0	0	0	0	844409	443220
234	0	0	0	0	0	0	384700	3051
235	0	0	0	0	0	0	740702	201641
236	0	0	0	0	0	0	745168	897571
237	0	0	0	0	0	0	368083	879315
238	0	0	0	0	0	0	578594	96572
239	0	0	0	0	0	0	638377	921506
240	0	0	0	0	0	0	15703	129713
241	0	0	0	0	0	0	533376	555119
242	0	0	0	0	0	0	946550	396453
243	0	0	0	0	0	0	247852	298466
244	0	0	0	0	0	0	688285	579669
245	0	0	0	0	0	0	716570	29457
246	0	0	0	0	0	0	891689	606804
247	0	0	0	0	0	0	783156	478958
248	0	0	0	0	0	0	776790	320492
249	0	0	0	0	0	0	583850	178950
250	0	0	0	0	0	0	199455	271840
251	0	0	0	0	0	0	196454	921529
252	0	0	0	0	0	0	30728	885226
253	0	0	0	0	0	0	279973	321995
254	0	0	0	0	0	0	109542	992834
255	0	0	0	0	0	0	941092	505022
256	0	0	0	0	0	0	36554	50514
257	0	0	0	0	0	0	2893	244201
258	0	0	0	0	0	0	179347	98535
259	0	0	0	0	0	0	540655	384820
260	0	0	0	0	0	0	770833	529284
261	0	0	0	0	0	0	271161	727813
262	0	0	0	0	0	0	227928	842709
263	0	0	0	0	0	0	214898	674666
264	0	0	0	0	0	0	107392	260337
265	0	0	0	0	0	0	137284	509612
266	0	0	0	0	0	0	398390	604018
267	0	0	0	0	0	0	184454	548844
268	0	0	0	0	0	0	974593	529956
269	0	0	0	0	0	0	880130	13019
270	0	0	0	0	0	0	979539	665584
271	0	0	0	0	0	0	450463	324490
272	0	0	0	0	0	0	440968	452087
273	0	0	0	0	0	0	121758	592027
274	0	0	0	0	0	0	632773	235430
275	0	0	0	0	0	0	797824	561465
276	0	0	0	0	0	0	185011	281595
277	0	0	0	0	0	0	521329	277927
278	0	0	0	0	0	0	482212	293868
279	0	0	0	0	0	0	770551	80640
280	0	0	0	0	0	0	476037	801792
281	0	0	0	0	0	0	386745	714028
282	0	0	0	0	0	0	464632	776346
283	0	0	0	0	0	0	673524	92217
284	0	0	0	0	0	0	334919	664157
285	0	0	0	0	0	0	239261	648809
286	0	0	0	0	0	0	955576	296159
287	0	0	0	0	0	0	396404	635792
288	0	0	0	0	0	0	506554	191951
289	0	0	0	0	0	0	492072	407493
290	0	0	0	0	0	0	431790	261247
291	0	0	0	0	0	0	458509	8719
292	0	0	0	0	0	0	8353	348451
293	0	0	0	0	0	0	549763	819900
294	0	0	0	0	0	0	109728	975565
295	0	0	0	0	0	0	612647	484503
296	0	0	0	0	0	0	241928	712097
297	0	0	0	0	0	0	640423	762345
298	0	0	0	0	0	0	914316	705527
299	0	0	0	0	0	0	756985	89461
300	0	0	0	0	0	0	361616	434996
301	0	0	0	0	0	0	808607	505142
302	0	0	0	0	0	0	82669	943057
303	0	0	0	0	0	0	69889	30867
304	0	0	0	0	0	0	535840	613140
305	0	0	0	0	0	0	17076	572323
306	0	0	0	0	0	0	148566	267478
307	0	0	0	0	0	0	79268	944109
308	0	0	0	0	0	0	318761	431047
309	0	0	0	0	0	0	514960	241817
310	0	0	0	0	0	0	120250	942546
311	0	0	0	0	0	0	741903	858996
312	0	0	0	0	0	0	334574	687991
313	0	0	0	0	0	0	32676	598852
314	0	0	0	0	0	0	393475	468077
315	0	0	0	0	0	0	849245	468173
316	0	0	0	0	0	0	424576	635768
317	0	0	0	0	0	0	345290	835773
318	0	0	0	0	0	0	957604	57550
319	0	0	0	0	0	0	671274	116035
320	0	0	0	0	0	0	549463	886256
321	0	0	0	0	0	0	614043	870181
322	0	0	0	0	0	0	566801	479617
323	0	0	0	0	0	0	459267	12118
324	0	0	0	0	0	0	607377	594152
325	0	0	0	0	0	0	805725	291622
326	0	0	0	0	0	0	969664	94596
327	0	0	0	0	0	0	986956	182543
328	0	0	0	0	0	0	327281	499523
329	0	0	0	0	0	0	406064	863446
330	0	0	0	0	0	0	282337	60268
331	0	0	0	0	0	0	352025	815111
332	0	0	0	0	0	0	838182	675950
333	0	0	0	0	0	0	85408	290311
334	0	0	0	0	0	0	427899	942203
335	0	0	0	0	0	0	784182	66855
336	0	0	0	0	0	0	552503	747778
337	0	0	0	0	0	0	672803	403951
338	0	0	0	0	0	0	731946	593748
339	0	0	0	0	0	0	313191	511680
340	0	0	0	0	0	0	15852	354891
341	0	0	0	0	0	0	814909	158884
342	0	0	0	0	0	0	836990	730994
343	0	0	0	0	0	0	607101	379759
344	0	0	0	0	0	0	844548	732052
345	0	0	0	0	0	0	226924	185509
346	0	0	0	0	0	0	507252	867477
347	0	0	0	0	0	0	34731	575693
348	0	0	0	0	0	0	48394	880355
349	0	0	0	0	0	0	644947	926614
350	0	0	0	0	0	0	11709	583857
351	0	0	0	0	0	0	994271	955626
352	0	0	0	0	0	0	718720	543352
353	0	0	0	0	0	0	444507	667582
354	0	0	0	0	0	0	632174	467303
355	0	0	0	0	0	0	511863	338774
356	0	0	0	0	0	0	120861	846614
357	0	0	0	0	0	0	497647	794716
358	0	0	0	0	0	0	341657	637424
359	0	0	0	0	0	0	485767	674603
360	0	0	0	0	0	0	597448	232330
361	0	0	0	0	0	0	731804	648316
362	0	0	0	0	0	0	203277	373627
363	0	0	0	0	0	0	510390	765141
364	0	0	0	0	0	0	676886	161519
365	0	0	0	0	0	0	69043	538766
366	0	0	0	0	0	0	497830	154888
367	0	0	0	0	0	0	143053	667144
368	0	0	0	0	0	0	691128	131336
369	0	0	0	0	0	0	66314	733740
370	0	0	0	0	0	0	482008	221517
371	0	0	0	0	0	0	385920	915443
372	0	0	0	0	0	0	13144	126499
373	0	0	0	0	0	0	977410	189292
374	0	0	0	0	0	0	665048	442322
375	0	0	0	0	0	0	285190	660738
376	0	0	0	0	0	0	511735	845934
377	0	0	0	0	0	0	619389	314651
378	0	0	0	0	0	0	768541	755401
379	0	0	0	0	0	0	435136	905712
380	0	0	0	0	0	0	839224	639404
381	0	0	0	0	0	0	558684	818908
382	0	0	0	0	0	0	617614	581981
383	0	0	0	0	0	0	334302	398269
384	0	0	0	0	0	0	286263	733845
385	0	0	0	0	0	0	326973	666861
386	0	0	0	0	0	0	548451	319011
387	0	0	0	0	0	0	423108	18386
388	0	0	0	0	0	0	226532	588497
389	0	0	0	0	0	0	833305	342888
390	0	0	0	0	0	0	89373	762677
391	0	0	0	0	0	0	549343	658043
392	0	0	0	0	0	0	179882	35177
393	0	0	0	0	0	0	971240	45300
394	0	0	0	0	0	0	942269	998819
395	0	0	0	0	0	0	908925	617410
396	0	0	0	0	0	0	146531	515909
397	0	0	0	0	0	0	577313	855070
398	0	0	0	0	0	0	112230	242389
399	0	0	0	0	0	0	244826	621822
400	0	0	0	0	0	0	114128	602382
401	0	0	0	0	0	0	961947	386798
402	0	0	0	0	0	0	301115	699495
403	0	0	0	0	0	0	134584	631142
404	0	0	0	0	0	0	698759	808688
405	0	0	0	0	0	0	465041	532578
406	0	0	0	0	0	0	765002	503491
407	0	0	0	0	0	0	285774	327960
408	0	0	0	0	0	0	616203	622677
409	0	0	0	0	0	0	128646	109576
410	0	0	0	0	0	0	778738	679437
411	0	0	0	0	0	0	844690	504453
412	0	0	0	0	0	0	815954	596391
413	0	0	0	0	0	0	498903	473075
414	0	0	0	0	0	0	172098	354353
415	0	0	0	0	0	0	389516	774058
416	0	0	0	0	0	0	787385	736338
417	0	0	0	0	0	0	105394	112328
418	0	0	0	0	0	0	416020	275898
419	0	0	0	0	0	0	232091	852380
420	0	0	0	0	0	0	212056	68014
421	0	0	0	0	0	0	177983	889280
422	0	0	0	0	0	0	232095	138591
423	0	0	0	0	0	0	280971	758745
424	0	0	0	0	0	0	182006	811198
425	0	0	0	0	0	0	709565	195618
426	0	0	0	0	0	0	700953	840416
427	0	0	0	0	0	0	745322	571731
428	0	0	0	0	0	0	704009	543035
429	0	0	0	0	0	0	680914	257622
430	0	0	0	0	0	0	836052	98527
431	0	0	0	0	0	0	880183	384751
432	0	0	0	0	0	0	355444	163077
433	0	0	0	0	0	0	45603	60770
434	0	0	0	0	0	0	679874	384085
435	0	0	0	0	0	0	367564	488387
436	0	0	0	0	0	0	374299	828208
437	0	0	0	0	0	0	196649	132283
438	0	0	0	0	0	0	625224	883241
439	0	0	0	0	0	0	60933	820777
440	0	0	0	0	0	0	144418	193000
441	0	0	0	0	0	0	239760	28741
442	0	0	0	0	0	0	430794	22747
443	0	0	0	0	0	0	932552	938155
444	0	0	0	0	0	0	64908	35307
445	0	0	0	0	0	0	332253	192348
446	0	0	0	0	0	0	832853	14622
447	0	0	0	0	0	0	571573	974320
448	0	0	0	0	0	0	795762	798935
449	0	0	0	0	0	0	645323	951318
450	0	0	0	0	0	0	581519	10587
451	0	0	0	0	0	0	700107	4845
452	0	0	0	0	0	0	250036	946223
453	0	0	0	0	0	0	748045	389353
454	0	0	0	0	0	0	70114	355626
455	0	0	0	0	0	0	376725	480945
456	0	0	0	0	0	0	232732	607750
457	0	0	0	0	0	0	432850	58664
458	0	0	0	0	0	0	745872	538665
459	0	0	0	0	0	0	777679	705847
460	0	0	0	0	0	0	523819	928949
461	0	0	0	0	0	0	795554	550754
462	0	0	0	0	0	0	847953	527204
463	0	0	0	0	0	0	607371	13571
464	0	0	0	0	0	0	616408	196777
465	0	0	0	0	0	0	481932	112979
466	0	0	0	0	0	0	325231	227907
467	0	0	0	0	0	0	984410	713670
468	0	0	0	0	0	0	215943	970559
469	0	0	0	0	0	0	151270	95228
470	0	0	0	0	0	0	259762	682555
471	0	0	0	0	0	0	220972	481307
472	0	0	0	0	0	0	440221	628519
473	0	0	0	0	0	0	178151	565699
474	0	0	0	0	0	0	336247	391370
475	0	0	0	0	0	0	107105	516097
476	0	0	0	0	0	0	756674	845498
477	0	0	0	0	0	0	490704	508533
478	0	0	0	0	0	0	91313	851963
479	0	0	0	0	0	0	846963	897167
480	0	0	0	0	0	0	777456	520841
481	0	0	0	0	0	0	598108	484407
482	0	0	0	0	0	0	269404	192916
483	0	0	0	0	0	0	397381	425448
484	0	0	0	0	0	0	272734	634057
485	0	0	0	0	0	0	279774	724632
486	0	0	0	0	0	0	881264	902915
487	0	0	0	0	0	0	656552	857732
488	0	0	0	0	0	0	31985	170052
489	0	0	0	0	0	0	966274	797268
490	0	0	0	0	0	0	335717	868743
491	0	0	0	0	0	0	48548	583583
492	0	0	0	0	0	0	492629	741790
493	0	0	0	0	0	0	159570	998727
494	0	0	0	0	0	0	377164	765413
495	0	0	0	0	0	0	17938	824544
496	0	0	0	0	0	0	728700	388720
497	0	0	0	0	0	0	268840	99421
498	0	0	0	0	0	0	287078	872106
499	0	0	0	0	0	0	860720	66969
500	0	0	0	0	0	0	918950	800684
501	0	0	0	0	0	0	18041	69903
502	0	0	0	0	0	0	303756	986481
503	0	0	0	0	0	0	142920	984688
504	0	0	0	0	0	0	280122	707019
505	0	0	0	0	0	0	211273	480039
506	0	0	0	0	0	0	542642	194177
507	0	0	0	0	0	0	866527	35704
508	0	0	0	0	0	0	314205	904578
509	0	0	0	0	0	0	40896	648494
510	0	0	0	0	0	0	778941	371879
511	0	0	0	0	0	0	849219	185115
512	0	0	0	0	0	0	927964	803321
513	0	0	0	0	0	0	581709	831125
514	0	0	0	0	0	0	689957	967903
515	0	0	0	0	0	0	191404	779325
516	0	0	0	0	0	0	579524	445642
517	0	0	0	0	0	0	442878	843465
518	0	0	0	0	0	0	989619	535155
519	0	0	0	0	0	0	670208	256750
520	0	0	0	0	0	0	475222	378899
521	0	0	0	0	0	0	124236	170122
522	0	0	0	0	0	0	543834	541089
523	0	0	0	0	0	0	185825	721270
524	0	0	0	0	0	0	504604	740076
525	0	0	0	0	0	0	261757	118414
526	0	0	0	0	0	0	937066	320861
527	0	0	0	0	0	0	473322	805224
528	0	0	0	0	0	0	55167	212830
529	0	0	0	0	0	0	544927	498005
530	0	0	0	0	0	0	586036	553618
531	0	0	0	0	0	0	847047	702765
532	0	0	0	0	0	0	320331	962549
533	0	0	0	0	0	0	588084	792538
534	0	0	0	0	0	0	228412	649987
535	0	0	0	0	0	0	375665	841209
536	0	0	0	0	0	0	642163	931492
537	0	0	0	0	0	0	914434	521181
538	0	0	0	0	0	0	278911	149883
539	0	0	0	0	0	0	193179	629268
540	0	0	0	0	0	0	991139	832555
541	0	0	0	0	0	0	668569	274301
542	0	0	0	0	0	0	758464	473316
543	0	0	0	0	0	0	991325	848840
544	0	0	0	0	0	0	923206	487372
545	0	0	0	0	0	0	751558	557913
546	0	0	0	0	0	0	24976	454245
547	0	0	0	0	0	0	523572	20194
548	0	0	0	0	0	0	156009	538517
549	0	0	0	0	0	0	444323	681403
550	0	0	0	0	0	0	129294	615748
551	0	0	0	0	0	0	683398	120234
552	0	0	0	0	0	0	919657	237712
553	0	0	0	0	0	0	960726	900541
554	0	0	0	0	0	0	154979	735800
555	0	0	0	0	0	0	777940	686062
556	0	0	0	0	0	0	800637	555492
557	0	0	0	0	0	0	572890	943461
558	0	0	0	0	0	0	179495	850797
559	0	0	0	0	0	0	165605	465927
560	0	0	0	0	0	0	640589	875945
561	0	0	0	0	0	0	529850	928778
562	0	0	0	0	0	0	830899	83225
563	0	0	0	0	0	0	743909	198350
564	0	0	0	0	0	0	93597	42332
565	0	0	0	0	0	0	816458	683967
566	0	0	0	0	0	0	267181	910511
567	0	0	0	0	0	0	34001	982760
568	0	0	0	0	0	0	758699	567949
569	0	0	0	0	0	0	887036	257869
570	0	0	0	0	0	0	787594	250592
571	0	0	0	0	0	0	463132	526374
572	0	0	0	0	0	0	376567	629841
573	0	0	0	0	0	0	814469	365082
574	0	0	0	0	0	0	279616	567911
\.


--
-- TOC entry 3433 (class 0 OID 16452)
-- Dependencies: 222
-- Data for Name: statistiche_canzoni; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.statistiche_canzoni (id_statistica, id_canzone) FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
11	11
12	12
13	13
14	14
15	15
16	16
17	17
18	18
19	19
20	20
21	21
22	22
23	23
24	24
25	25
26	26
27	27
28	28
29	29
30	30
31	31
32	32
33	33
34	34
35	35
36	36
37	37
38	38
39	39
40	40
41	41
42	42
43	43
44	44
45	45
46	46
47	47
48	48
49	49
50	50
51	51
52	52
53	53
54	54
55	55
56	56
57	57
58	58
59	59
60	60
61	61
62	62
63	63
64	64
65	65
66	66
67	67
68	68
69	69
70	70
71	71
72	72
73	73
74	74
75	75
76	76
77	77
78	78
79	79
80	80
81	81
82	82
83	83
84	84
85	85
86	86
87	87
88	88
89	89
90	90
91	91
92	92
93	93
94	94
95	95
96	96
97	97
98	98
99	99
100	100
101	101
102	102
103	103
104	104
105	105
106	106
107	107
108	108
109	109
110	110
111	111
112	112
113	113
114	114
115	115
116	116
117	117
118	118
119	119
120	120
121	121
122	122
123	123
124	124
125	125
126	126
127	127
128	128
129	129
130	130
131	131
132	132
133	133
134	134
135	135
136	136
137	137
138	138
139	139
140	140
141	141
142	142
143	143
144	144
145	145
146	146
147	147
148	148
149	149
150	150
151	151
152	152
153	153
154	154
155	155
156	156
157	157
158	158
159	159
160	160
161	161
162	162
163	163
164	164
165	165
166	166
167	167
168	168
169	169
170	170
171	171
172	172
173	173
174	174
175	175
176	176
177	177
178	178
179	179
180	180
181	181
182	182
183	183
184	184
185	185
186	186
187	187
188	188
189	189
190	190
191	191
192	192
193	193
194	194
195	195
196	196
197	197
198	198
199	199
200	200
201	201
202	202
203	203
204	204
205	205
206	206
207	207
208	208
209	209
210	210
211	211
212	212
213	213
214	214
215	215
216	216
217	217
218	218
219	219
220	220
221	221
222	222
223	223
224	224
225	225
226	226
227	227
228	228
229	229
230	230
231	231
232	232
233	233
234	234
235	235
236	236
237	237
238	238
239	239
240	240
241	241
242	242
243	243
244	244
245	245
246	246
247	247
248	248
249	249
250	250
251	251
252	252
253	253
254	254
255	255
256	256
257	257
258	258
259	259
260	260
261	261
262	262
263	263
264	264
265	265
266	266
267	267
268	268
269	269
270	270
271	271
272	272
273	273
274	274
275	275
276	276
277	277
278	278
279	279
280	280
281	281
282	282
283	283
284	284
285	285
286	286
287	287
288	288
289	289
290	290
291	291
292	292
293	293
294	294
295	295
296	296
297	297
298	298
299	299
300	300
301	301
302	302
303	303
304	304
305	305
306	306
307	307
308	308
309	309
310	310
311	311
312	312
313	313
314	314
315	315
316	316
317	317
318	318
319	319
320	320
321	321
322	322
323	323
324	324
325	325
326	326
327	327
328	328
329	329
330	330
331	331
332	332
333	333
334	334
335	335
336	336
337	337
338	338
339	339
340	340
341	341
342	342
343	343
344	344
345	345
346	346
347	347
348	348
349	349
350	350
351	351
352	352
353	353
354	354
355	355
356	356
357	357
358	358
359	359
360	360
361	361
362	362
363	363
364	364
365	365
366	366
367	367
368	368
369	369
370	370
371	371
372	372
373	373
374	374
375	375
376	376
377	377
378	378
379	379
380	380
381	381
382	382
383	383
384	384
385	385
386	386
387	387
388	388
389	389
390	390
391	391
392	392
393	393
394	394
395	395
396	396
397	397
398	398
399	399
400	400
401	401
402	402
403	403
404	404
405	405
406	406
407	407
408	408
409	409
410	410
411	411
412	412
413	413
414	414
415	415
416	416
417	417
418	418
419	419
420	420
421	421
422	422
423	423
424	424
425	425
426	426
427	427
428	428
429	429
430	430
431	431
432	432
433	433
434	434
435	435
436	436
437	437
438	438
439	439
440	440
441	441
442	442
443	443
444	444
445	445
446	446
447	447
448	448
449	449
450	450
451	451
452	452
453	453
454	454
455	455
456	456
457	457
458	458
459	459
460	460
461	461
462	462
463	463
464	464
465	465
466	466
467	467
468	468
469	469
470	470
471	471
472	472
473	473
474	474
475	475
476	476
477	477
478	478
479	479
480	480
481	481
482	482
483	483
484	484
485	485
486	486
487	487
488	488
489	489
490	490
491	491
492	492
493	493
494	494
495	495
496	496
497	497
498	498
499	499
500	500
501	501
502	502
503	503
504	504
505	505
506	506
507	507
508	508
509	509
510	510
511	511
512	512
513	513
514	514
515	515
516	516
517	517
518	518
519	519
520	520
521	521
522	522
523	523
524	524
525	525
526	526
527	527
528	528
529	529
530	530
531	531
532	532
533	533
534	534
535	535
536	536
537	537
538	538
539	539
540	540
541	541
542	542
543	543
544	544
545	545
546	546
547	547
548	548
549	549
550	550
551	551
552	552
553	553
554	554
555	555
556	556
557	557
558	558
559	559
560	560
561	561
562	562
563	563
564	564
565	565
566	566
567	567
568	568
569	569
570	570
571	571
572	572
573	573
574	574
\.


--
-- TOC entry 3434 (class 0 OID 16455)
-- Dependencies: 223
-- Data for Name: tag; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.tag (tag) FROM stdin;
Speed Metal
Thrash Metal
Hard Rock
Pop Rock
Progressive Metal
Heavy Metal
Progressive Rock
Pop
Arena Rock
Inglese
Megaforce
Elektra
EMI
Hollywood Records
Sleaze Metal
Geffen
Musica Acustica
Punk Rock
Italiano
WEA Italiana
Zoo Aperto
Rock
Alternative Country
Rock And Roll
Grunge
Warner Bros.
Musica D'Autore
Lotus LOP
Lotus Records
Targa
Carosello
Industrial Metal
Alternative Metal
Neue Deutsche Harte
Motor Music
Tedesco
Gothic Metal
Universal
Nu Metal
Rap Metal
Rap Rock
Alternative Rock
Electronic Rock
Experimental Rock
CGD
Musica Classica
Sugar
Polygram International
Opera Lirica
Philips Records
Musica Latina
Pop Latino
Sony Music
Spagnolo
\.


--
-- TOC entry 3436 (class 0 OID 16461)
-- Dependencies: 225
-- Data for Name: utenti; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.utenti (id_utente, email, nome, cognome, nickname, bio, data_nascita, password, ruolo, premium) FROM stdin;
1	admin@admin	admin	admin	admin		2000-01-01	pbkdf2:sha256:260000$RQUZJYUgtToE8y1V$63d08b33a7c2202881fcf720e65829dd3cd53ce12a167d397e4deca1f597814e	3	t
2	metallica@gmail.com	James	Hetfield	Metallica	I Metallica sono un gruppo musicale heavy metal statunitense, formatosi a Los Angeles nel 1981.	1963-08-03	pbkdf2:sha256:260000$wBBaFAz12JifKhZk$50c148201c3a5b55dd65f2f1433fcc31b96e81feb1df6a6dbc692d9eb3a60622	2	f
3	queen@gmail.com	Freddie	Mercury	Queen	I Queen sono un gruppo musicale rock britannico, formatosi a Londra nel 1970 dall'incontro del cantante e pianista Freddie Mercury con il chitarrista Brian May e con il batterista Roger Taylor.	1946-09-05	pbkdf2:sha256:260000$cfE4jvECgFhwN4Cp$3866a653bbe1b2d88a13c456dc2cb309d7bc45578c7a7bc49e88d3deb94530f9	2	f
4	gunsnroses@gmail.com	Guns N' Roses	Guns N' Roses	Guns N' Roses	I Guns N' Roses sono un gruppo musicale hard rock statunitense, formatosi a Los Angeles nel 1985.	1962-02-06	pbkdf2:sha256:260000$6yNdPKIUGJ3wX1Im$da38b3764a625965ebe2068fb94cbcd9763a53b7d7cd9e0791a74fe88013ae0a	2	f
5	ligabue@gmail.com	Luciano Riccardo	Ligabue	Ligabue	Luciano Riccardo Ligabue, noto con il solo cognome Ligabue, e' un cantautore, chitarrista, regista, scrittore, sceneggiatore e produttore discografico italiano.	1960-03-13	pbkdf2:sha256:260000$hagdx8uDgJZbOoAE$432f418c4a213859d290735bc65efa9916aa655ed6af543985c1142cffc439a0	2	t
6	vasco@gmail.com	Vasco	Rossi	Vasco	Vasco Rossi, noto anche semplicemente come Vasco o con l'appellativo Blasco, e' un cantautore italiano.	1952-02-07	pbkdf2:sha256:260000$Z9Y8Pi6xlgWBHbj3$7254a4ce2e0bcf9a6f40cebeef81d6b3afc1b537adb16e77517d2da562cbfca8	2	t
7	rammstein@gmail.com	Rammstein	Rammstein	Rammstein	I Rammstein sono un gruppo musicale industrial metal tedesco formatosi a Berlino nel 1993 appartenente alla corrente della Neue Deutsche Harte.	1963-01-04	pbkdf2:sha256:260000$vmnxm9w339FrEwwk$657862a6efd61476bb6a211ee368c3aa39b4d04d87fda8c4b5ada4b0ae60be25	2	f
8	linkinpark@gmail.com	Linkin Park	Linkin Park	Linkin Park	I Linkin Park sono un gruppo musicale statunitense formatosi a Los Angeles nel 1996.	1977-02-11	pbkdf2:sha256:260000$OCwBLTrW0OmbCGfe$2cbdb58b58e4c754e4bd2909f6f313edb40b0aae30a7271631faefe73cf32f64	2	t
9	pausini@gmail.com	Laura	Pausini	Laura Pausini	Laura Pausini e' una cantautrice italiana.	1974-05-16	pbkdf2:sha256:260000$xTBqjKGjKNdGfOAh$a52230c513211da81d577afbf72555717647994d2297b85d2c63f5f2861657c8	2	f
10	bocelli@gmail.com	Andrea	Bocelli	Andrea Bocelli	Andrea Bocelli e' un tenore e cantante pop italiano.	1958-09-22	pbkdf2:sha256:260000$rTwCh8gU8593xhBP$49b7b7f4b2d4496c3acb8ece0e39c6c091667198ecadca5ed3f675f288de3de5	2	f
11	rickymartin@gmail.com	Enrique Martin	Morales	Ricky Martin	Ricky Martin, all'anagrafe Enrique Martin Morales, e' un cantante, attore e personaggio televisivo portoricano.	1971-12-24	pbkdf2:sha256:260000$KQDVQ0eUgYQAhWNH$7a56c7601f555238fdb2fff86b25247ea7731f60403c25568888306a9b0e9b03	2	t
12	massimiliano@gmail.com	Massimiliano	Zuin	Massimiliano Zuin		1996-07-23	pbkdf2:sha256:260000$ViQqVy81119f4zZE$c808677742150eb8590ffb7330d0c8d633ffa9aaafee4424563f46092b64b3d3	1	t
13	marco@gmail.com	Marco	Quarta	Marco Quarta		1997-12-17	pbkdf2:sha256:260000$2CAHlypHrVRm1n5o$17a5bf5b8b7bad14d90ec71a0fb430f296e327ed528696f9665d6b5dde45582b	1	t
14	michele@gmail.com	Michele	Lattanzi	Michele Lattanzi		1998-05-04	pbkdf2:sha256:260000$flaeYw5A9CWoYwHI$8fb51d1f8f4917ca4bab3a5e7e6423008155cc65e2dc2e8dd79e4090831f351f	1	t
\.


--
-- TOC entry 3442 (class 0 OID 0)
-- Dependencies: 209
-- Name: album_id_album_seq; Type: SEQUENCE SET; Schema: unive_music; Owner: postgres
--

SELECT pg_catalog.setval('unive_music.album_id_album_seq', 50, true);


--
-- TOC entry 3443 (class 0 OID 0)
-- Dependencies: 214
-- Name: canzoni_id_canzone_seq; Type: SEQUENCE SET; Schema: unive_music; Owner: postgres
--

SELECT pg_catalog.setval('unive_music.canzoni_id_canzone_seq', 574, true);


--
-- TOC entry 3444 (class 0 OID 0)
-- Dependencies: 217
-- Name: playlist_id_playlist_seq; Type: SEQUENCE SET; Schema: unive_music; Owner: postgres
--

SELECT pg_catalog.setval('unive_music.playlist_id_playlist_seq', 1, true);


--
-- TOC entry 3445 (class 0 OID 0)
-- Dependencies: 220
-- Name: statistiche_id_statistica_seq; Type: SEQUENCE SET; Schema: unive_music; Owner: postgres
--

SELECT pg_catalog.setval('unive_music.statistiche_id_statistica_seq', 574, true);


--
-- TOC entry 3446 (class 0 OID 0)
-- Dependencies: 224
-- Name: utenti_id_utenti_seq; Type: SEQUENCE SET; Schema: unive_music; Owner: postgres
--

SELECT pg_catalog.setval('unive_music.utenti_id_utenti_seq', 14, true);


--
-- TOC entry 3217 (class 2606 OID 16468)
-- Name: canzoni check_durata; Type: CHECK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE unive_music.canzoni
    ADD CONSTRAINT check_durata CHECK ((durata > 0)) NOT VALID;


--
-- TOC entry 3220 (class 2606 OID 16469)
-- Name: playlist check_n_canzoni; Type: CHECK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE unive_music.playlist
    ADD CONSTRAINT check_n_canzoni CHECK ((n_canzoni >= 0)) NOT VALID;


--
-- TOC entry 3215 (class 2606 OID 16470)
-- Name: album check_n_canzoni_album; Type: CHECK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE unive_music.album
    ADD CONSTRAINT check_n_canzoni_album CHECK ((n_canzoni >= 0)) NOT VALID;


--
-- TOC entry 3233 (class 2606 OID 16471)
-- Name: utenti check_ruolo; Type: CHECK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE unive_music.utenti
    ADD CONSTRAINT check_ruolo CHECK (((ruolo > 0) AND (ruolo < 4))) NOT VALID;


--
-- TOC entry 3235 (class 2606 OID 16473)
-- Name: album key_album; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.album
    ADD CONSTRAINT key_album UNIQUE (titolo, rilascio, id_artista);


--
-- TOC entry 3245 (class 2606 OID 16475)
-- Name: canzoni key_canzone; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.canzoni
    ADD CONSTRAINT key_canzone UNIQUE (titolo, rilascio, id_artista);


--
-- TOC entry 3261 (class 2606 OID 16477)
-- Name: utenti key_email; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.utenti
    ADD CONSTRAINT key_email UNIQUE (email);


--
-- TOC entry 3263 (class 2606 OID 16479)
-- Name: utenti key_nickname; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.utenti
    ADD CONSTRAINT key_nickname UNIQUE (nickname);


--
-- TOC entry 3241 (class 2606 OID 16481)
-- Name: attributo_album pk_attributo_album; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.attributo_album
    ADD CONSTRAINT pk_attributo_album PRIMARY KEY (id_tag, id_album);


--
-- TOC entry 3243 (class 2606 OID 16483)
-- Name: attributo_canzone pk_attributo_canzone; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.attributo_canzone
    ADD CONSTRAINT pk_attributo_canzone PRIMARY KEY (id_tag, id_canzone);


--
-- TOC entry 3249 (class 2606 OID 16485)
-- Name: contenuto pk_contenuto; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.contenuto
    ADD CONSTRAINT pk_contenuto PRIMARY KEY (id_album, id_canzone);


--
-- TOC entry 3237 (class 2606 OID 16487)
-- Name: album pk_id_album; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.album
    ADD CONSTRAINT pk_id_album PRIMARY KEY (id_album);


--
-- TOC entry 3239 (class 2606 OID 16489)
-- Name: artisti pk_id_artista; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.artisti
    ADD CONSTRAINT pk_id_artista PRIMARY KEY (id_utente);


--
-- TOC entry 3247 (class 2606 OID 16491)
-- Name: canzoni pk_id_canzone; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.canzoni
    ADD CONSTRAINT pk_id_canzone PRIMARY KEY (id_canzone);


--
-- TOC entry 3255 (class 2606 OID 16493)
-- Name: statistiche pk_id_statistica; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.statistiche
    ADD CONSTRAINT pk_id_statistica PRIMARY KEY (id_statistica);


--
-- TOC entry 3265 (class 2606 OID 16495)
-- Name: utenti pk_id_utente; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.utenti
    ADD CONSTRAINT pk_id_utente PRIMARY KEY (id_utente);


--
-- TOC entry 3251 (class 2606 OID 16497)
-- Name: playlist pk_playlist; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.playlist
    ADD CONSTRAINT pk_playlist PRIMARY KEY (id_playlist);


--
-- TOC entry 3253 (class 2606 OID 16499)
-- Name: raccolte pk_raccolte; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.raccolte
    ADD CONSTRAINT pk_raccolte PRIMARY KEY (id_playlist, id_canzone);


--
-- TOC entry 3257 (class 2606 OID 16501)
-- Name: statistiche_canzoni pk_statistiche_canzoni; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.statistiche_canzoni
    ADD CONSTRAINT pk_statistiche_canzoni PRIMARY KEY (id_statistica, id_canzone);


--
-- TOC entry 3259 (class 2606 OID 16503)
-- Name: tag pk_tag; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.tag
    ADD CONSTRAINT pk_tag PRIMARY KEY (tag);


--
-- TOC entry 3280 (class 2620 OID 16504)
-- Name: canzoni debutto; Type: TRIGGER; Schema: unive_music; Owner: postgres
--

CREATE TRIGGER debutto AFTER INSERT OR UPDATE OF rilascio ON unive_music.canzoni FOR EACH ROW EXECUTE FUNCTION unive_music.check_debutto();


--
-- TOC entry 3273 (class 2606 OID 16505)
-- Name: contenuto fk_album; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.contenuto
    ADD CONSTRAINT fk_album FOREIGN KEY (id_album) REFERENCES unive_music.album(id_album) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 3268 (class 2606 OID 16510)
-- Name: attributo_album fk_album; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.attributo_album
    ADD CONSTRAINT fk_album FOREIGN KEY (id_album) REFERENCES unive_music.album(id_album) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3272 (class 2606 OID 16515)
-- Name: canzoni fk_artista; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.canzoni
    ADD CONSTRAINT fk_artista FOREIGN KEY (id_artista) REFERENCES unive_music.artisti(id_utente) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3266 (class 2606 OID 16520)
-- Name: album fk_artista; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.album
    ADD CONSTRAINT fk_artista FOREIGN KEY (id_artista) REFERENCES unive_music.artisti(id_utente) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3276 (class 2606 OID 16525)
-- Name: raccolte fk_canzone; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.raccolte
    ADD CONSTRAINT fk_canzone FOREIGN KEY (id_canzone) REFERENCES unive_music.canzoni(id_canzone) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3274 (class 2606 OID 16530)
-- Name: contenuto fk_canzone; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.contenuto
    ADD CONSTRAINT fk_canzone FOREIGN KEY (id_canzone) REFERENCES unive_music.canzoni(id_canzone) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 3270 (class 2606 OID 16535)
-- Name: attributo_canzone fk_canzone; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.attributo_canzone
    ADD CONSTRAINT fk_canzone FOREIGN KEY (id_canzone) REFERENCES unive_music.canzoni(id_canzone) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3278 (class 2606 OID 16540)
-- Name: statistiche_canzoni fk_canzone; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.statistiche_canzoni
    ADD CONSTRAINT fk_canzone FOREIGN KEY (id_canzone) REFERENCES unive_music.canzoni(id_canzone) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3277 (class 2606 OID 16545)
-- Name: raccolte fk_playlist; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.raccolte
    ADD CONSTRAINT fk_playlist FOREIGN KEY (id_playlist) REFERENCES unive_music.playlist(id_playlist) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3279 (class 2606 OID 16550)
-- Name: statistiche_canzoni fk_statistica; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.statistiche_canzoni
    ADD CONSTRAINT fk_statistica FOREIGN KEY (id_statistica) REFERENCES unive_music.statistiche(id_statistica) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3271 (class 2606 OID 16555)
-- Name: attributo_canzone fk_tag; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.attributo_canzone
    ADD CONSTRAINT fk_tag FOREIGN KEY (id_tag) REFERENCES unive_music.tag(tag) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3269 (class 2606 OID 16560)
-- Name: attributo_album fk_tag; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.attributo_album
    ADD CONSTRAINT fk_tag FOREIGN KEY (id_tag) REFERENCES unive_music.tag(tag) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3267 (class 2606 OID 16565)
-- Name: artisti fk_utenti; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.artisti
    ADD CONSTRAINT fk_utenti FOREIGN KEY (id_utente) REFERENCES unive_music.utenti(id_utente) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3275 (class 2606 OID 16570)
-- Name: playlist fk_utenti; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.playlist
    ADD CONSTRAINT fk_utenti FOREIGN KEY (id_utente) REFERENCES unive_music.utenti(id_utente) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


-- Completed on 2022-08-14 17:08:20

--
-- PostgreSQL database dump complete
--

