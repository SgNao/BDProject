--
-- PostgreSQL database dump
--

-- Dumped from database version 14.2
-- Dumped by pg_dump version 14.2

-- Started on 2022-07-02 16:19:58

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
-- TOC entry 4 (class 2615 OID 16651)
-- Name: unive_music; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA unive_music;


ALTER SCHEMA unive_music OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 210 (class 1259 OID 16701)
-- Name: utenti; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.utenti (
    id_utente integer NOT NULL,
    email text NOT NULL,
    nome text NOT NULL,
    cognome text NOT NULL,
    nickname text,
    bio text,
    data_nascita date NOT NULL,
    password text NOT NULL,
    ruolo integer DEFAULT 1 NOT NULL
);


ALTER TABLE unive_music.utenti OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 16700)
-- Name: Utenti_IdUtenti_seq; Type: SEQUENCE; Schema: unive_music; Owner: postgres
--

CREATE SEQUENCE unive_music."Utenti_IdUtenti_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE unive_music."Utenti_IdUtenti_seq" OWNER TO postgres;

--
-- TOC entry 3447 (class 0 OID 0)
-- Dependencies: 209
-- Name: Utenti_IdUtenti_seq; Type: SEQUENCE OWNED BY; Schema: unive_music; Owner: postgres
--

ALTER SEQUENCE unive_music."Utenti_IdUtenti_seq" OWNED BY unive_music.utenti.id_utente;


--
-- TOC entry 217 (class 1259 OID 16765)
-- Name: album; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.album (
    id_album integer NOT NULL,
    titolo text NOT NULL,
    rilascio date NOT NULL,
    colore text NOT NULL,
    n_canzoni integer DEFAULT 0 NOT NULL,
    id_artista integer NOT NULL
);


ALTER TABLE unive_music.album OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16764)
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

--
-- TOC entry 3448 (class 0 OID 0)
-- Dependencies: 216
-- Name: album_id_album_seq; Type: SEQUENCE OWNED BY; Schema: unive_music; Owner: postgres
--

ALTER SEQUENCE unive_music.album_id_album_seq OWNED BY unive_music.album.id_album;


--
-- TOC entry 211 (class 1259 OID 16716)
-- Name: artisti; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.artisti (
    id_utente integer NOT NULL,
    debutto date
);


ALTER TABLE unive_music.artisti OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16850)
-- Name: attributo_album; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.attributo_album (
    id_tag text NOT NULL,
    id_album integer NOT NULL
);


ALTER TABLE unive_music.attributo_album OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16833)
-- Name: attributo_canzone; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.attributo_canzone (
    id_tag text NOT NULL,
    id_canzone integer NOT NULL
);


ALTER TABLE unive_music.attributo_canzone OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16867)
-- Name: attributo_playlist; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.attributo_playlist (
    id_playlist integer NOT NULL,
    id_tag text NOT NULL
);


ALTER TABLE unive_music.attributo_playlist OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 16740)
-- Name: canzoni; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.canzoni (
    id_canzone integer NOT NULL,
    titolo text NOT NULL,
    rilascio date NOT NULL,
    durata integer NOT NULL,
    colore text NOT NULL,
    id_artista integer NOT NULL
);


ALTER TABLE unive_music.canzoni OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 16739)
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
-- TOC entry 3449 (class 0 OID 0)
-- Dependencies: 213
-- Name: canzoni_id_canzone_seq; Type: SEQUENCE OWNED BY; Schema: unive_music; Owner: postgres
--

ALTER SEQUENCE unive_music.canzoni_id_canzone_seq OWNED BY unive_music.canzoni.id_canzone;


--
-- TOC entry 222 (class 1259 OID 16818)
-- Name: contenuto; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.contenuto (
    id_album integer NOT NULL,
    id_canzone integer NOT NULL
);


ALTER TABLE unive_music.contenuto OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 16726)
-- Name: playlist; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.playlist (
    id_utente integer NOT NULL,
    nome text NOT NULL,
    descrizione text,
    n_canzoni integer DEFAULT 0 NOT NULL,
    id_playlist integer NOT NULL
);


ALTER TABLE unive_music.playlist OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16755)
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
-- TOC entry 3450 (class 0 OID 0)
-- Dependencies: 215
-- Name: playlist_id_playlist_seq; Type: SEQUENCE OWNED BY; Schema: unive_music; Owner: postgres
--

ALTER SEQUENCE unive_music.playlist_id_playlist_seq OWNED BY unive_music.playlist.id_playlist;


--
-- TOC entry 221 (class 1259 OID 16803)
-- Name: raccolte; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.raccolte (
    id_playlist integer NOT NULL,
    id_canzone integer NOT NULL
);


ALTER TABLE unive_music.raccolte OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16782)
-- Name: statistiche; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.statistiche (
    id_statistica integer NOT NULL,
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
-- TOC entry 226 (class 1259 OID 16885)
-- Name: statistiche_canzoni; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.statistiche_canzoni (
    id_statistica integer NOT NULL,
    id_canzone integer NOT NULL
);


ALTER TABLE unive_music.statistiche_canzoni OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16781)
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
-- TOC entry 3451 (class 0 OID 0)
-- Dependencies: 218
-- Name: statistiche_id_statistica_seq; Type: SEQUENCE OWNED BY; Schema: unive_music; Owner: postgres
--

ALTER SEQUENCE unive_music.statistiche_id_statistica_seq OWNED BY unive_music.statistiche.id_statistica;


--
-- TOC entry 220 (class 1259 OID 16796)
-- Name: tag; Type: TABLE; Schema: unive_music; Owner: postgres
--

CREATE TABLE unive_music.tag (
    tag text NOT NULL
);


ALTER TABLE unive_music.tag OWNER TO postgres;

--
-- TOC entry 3223 (class 2604 OID 16768)
-- Name: album id_album; Type: DEFAULT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.album ALTER COLUMN id_album SET DEFAULT nextval('unive_music.album_id_album_seq'::regclass);


--
-- TOC entry 3222 (class 2604 OID 16743)
-- Name: canzoni id_canzone; Type: DEFAULT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.canzoni ALTER COLUMN id_canzone SET DEFAULT nextval('unive_music.canzoni_id_canzone_seq'::regclass);


--
-- TOC entry 3220 (class 2604 OID 16756)
-- Name: playlist id_playlist; Type: DEFAULT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.playlist ALTER COLUMN id_playlist SET DEFAULT nextval('unive_music.playlist_id_playlist_seq'::regclass);


--
-- TOC entry 3226 (class 2604 OID 16785)
-- Name: statistiche id_statistica; Type: DEFAULT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.statistiche ALTER COLUMN id_statistica SET DEFAULT nextval('unive_music.statistiche_id_statistica_seq'::regclass);


--
-- TOC entry 3216 (class 2604 OID 16704)
-- Name: utenti id_utente; Type: DEFAULT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.utenti ALTER COLUMN id_utente SET DEFAULT nextval('unive_music."Utenti_IdUtenti_seq"'::regclass);


--
-- TOC entry 3432 (class 0 OID 16765)
-- Dependencies: 217
-- Data for Name: album; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.album (id_album, titolo, rilascio, colore, n_canzoni, id_artista) FROM stdin;
1	Kill 'Em All	1983-07-25	#ff0000	10	2
2	Ride the Lightning	1984-07-27	#ff4000	8	2
3	Master of puppets	1986-03-03	#ff8000	8	2
4	... And Justice for All	1988-08-25	#ffbf00	9	2
5	Metallica	1991-08-12	#ffff00	12	2
6	Made in Heaven	1995-11-06	#bfff00	10	3
7	The Miracle	1989-05-22	#80ff00	10	3
8	A Night At The Opera	1975-11-21	#40ff00	12	3
9	News of the World	1977-10-28	#00ff00	11	3
10	The Game	1980-06-30	#00ff40	10	3
\.


--
-- TOC entry 3426 (class 0 OID 16716)
-- Dependencies: 211
-- Data for Name: artisti; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.artisti (id_utente, debutto) FROM stdin;
2	1981-10-28
3	1968-10-26
\.


--
-- TOC entry 3439 (class 0 OID 16850)
-- Dependencies: 224
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
\.


--
-- TOC entry 3438 (class 0 OID 16833)
-- Dependencies: 223
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
\.


--
-- TOC entry 3440 (class 0 OID 16867)
-- Dependencies: 225
-- Data for Name: attributo_playlist; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.attributo_playlist (id_playlist, id_tag) FROM stdin;
1	Speed Metal
1	Thrash Metal
1	Hard Rock
1	Progressive Metal
1	Heavy Metal
\.


--
-- TOC entry 3429 (class 0 OID 16740)
-- Dependencies: 214
-- Data for Name: canzoni; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.canzoni (id_canzone, titolo, rilascio, durata, colore, id_artista) FROM stdin;
1	Hit the Lights	1983-07-25	257	#ff0000	2
2	The Four Horsemen	1983-07-25	433	#ff0000	2
3	Motorbreath	1983-07-25	188	#ff0000	2
4	Jump in the Fire	1983-07-25	281	#ff0000	2
5	(Anesthesia)-Pulling Teeth	1983-07-25	254	#ff0000	2
6	Whiplash	1983-07-25	249	#ff0000	2
7	Phantom Lord	1983-07-25	301	#ff0000	2
8	No Remorse	1983-07-25	386	#ff0000	2
9	Seek & Destroy	1983-07-25	415	#ff0000	2
10	Metal Militia	1983-07-25	311	#ff0000	2
11	Fight Fire with Fire	1984-07-27	284	#ff4000	2
12	Ride the Lightning	1984-07-27	397	#ff4000	2
13	For Whom the Bell Tolls	1984-07-27	311	#ff4000	2
14	Fade to Black	1984-07-27	415	#ff4000	2
15	Trapped Under Ice	1984-07-27	244	#ff4000	2
16	Escape	1984-07-27	264	#ff4000	2
17	Creeping Death	1984-07-27	396	#ff4000	2
18	The Call of Ktulu	1984-07-27	535	#ff4000	2
19	Battery	1986-03-03	312	#ff8000	2
20	Master of Puppets	1986-03-03	515	#ff8000	2
21	The Thing That Should Not Be	1986-03-03	396	#ff8000	2
22	Welcome Home (Sanitarium)	1986-03-03	387	#ff8000	2
23	Disposable Heroes	1986-03-03	496	#ff8000	2
24	Leper Messiah	1986-03-03	340	#ff8000	2
25	Orion	1986-03-03	507	#ff8000	2
26	Damage, Inc.	1986-03-03	332	#ff8000	2
27	Blackened	1988-08-25	400	#ffbf00	2
28	... And Justice for All	1988-08-25	586	#ffbf00	2
29	Eye of the Beholder	1988-08-25	390	#ffbf00	2
30	One	1988-08-25	447	#ffbf00	2
31	The Shortest Straw	1988-08-25	395	#ffbf00	2
32	Harvester of Sorrow	1988-08-25	345	#ffbf00	2
33	The Frayed Ends of Sanity	1988-08-25	764	#ffbf00	2
34	To Live Is to Die	1988-08-25	588	#ffbf00	2
35	Dyers Eve	1988-08-25	313	#ffbf00	2
36	Enter Sandman	1991-08-12	329	#ffff00	2
37	Sad but True	1991-08-12	324	#ffff00	2
38	Holler than Thou	1991-08-12	227	#ffff00	2
39	The Unforgiven	1991-08-12	386	#ffff00	2
40	Wherever I May Roam	1991-08-12	402	#ffff00	2
41	Don't Tread on Me	1991-08-12	239	#ffff00	2
42	Through the Never	1991-08-12	241	#ffff00	2
43	Nothing Else Matters	1991-08-12	389	#ffff00	2
44	Of Wolf and Man	1991-08-12	256	#ffff00	2
45	The God That Failed	1991-08-12	305	#ffff00	2
46	My Friend of Misery	1991-08-12	407	#ffff00	2
47	The Struggle Within	1991-08-12	231	#ffff00	2
48	It's a Beautiful Day	1995-11-06	152	#bfff00	3
49	Made in Heaven	1995-11-06	325	#bfff00	3
50	Let Me Live	1995-11-06	285	#bfff00	3
51	Mother Love	1995-11-06	286	#bfff00	3
52	My Life Has Been Saved	1995-11-06	195	#bfff00	3
53	I Was Born to Love You	1995-11-06	289	#bfff00	3
54	Heaven for Everyone	1995-11-06	336	#bfff00	3
55	Too Much Love Will Kill You	1995-11-06	258	#bfff00	3
56	You Don't Fool Me	1995-11-06	323	#bfff00	3
57	A Winter's Tale	1995-11-06	229	#bfff00	3
58	Party	1989-05-22	144	#80ff00	3
59	Khashoggi's Ship	1989-05-22	148	#80ff00	3
60	The Miracle	1989-05-22	302	#80ff00	3
61	I Want It All	1989-05-22	281	#80ff00	3
62	The Invisible Man	1989-05-22	237	#80ff00	3
63	Breathru	1989-05-22	248	#80ff00	3
64	Rain Must Fall	1989-05-22	263	#80ff00	3
65	Scandal	1989-05-22	282	#80ff00	3
66	My Baby Does Me	1989-05-22	203	#80ff00	3
67	Was It All Worth It	1989-05-22	345	#80ff00	3
68	Death on Two Legs (Dedicated to...)	1975-11-21	223	#40ff00	3
69	Lazing on a Sunday Afternoon	1975-11-21	67	#40ff00	3
70	I'm in Love with My Car	1975-11-21	185	#40ff00	3
71	You're My Best Friend	1975-11-21	172	#40ff00	3
72	'39	1975-11-21	211	#40ff00	3
73	Sweet Lady	1975-11-21	244	#40ff00	3
74	Seaside Rendezvous	1975-11-21	196	#40ff00	3
75	The Prophet's Song	1975-11-21	501	#40ff00	3
76	Love of My Life	1975-11-21	219	#40ff00	3
77	Good Company	1975-11-21	203	#40ff00	3
78	Bohemian Rhapsody	1975-11-21	355	#40ff00	3
79	God Save The Queen	1975-11-21	75	#40ff00	3
80	We Will Rock You	1977-10-28	121	#00ff00	3
81	We Are The Champions	1977-10-28	177	#00ff00	3
82	Sheer Heart Attack	1977-10-28	204	#00ff00	3
83	All Dead, All Dead	1977-10-28	191	#00ff00	3
84	Spread Your Wings	1977-10-28	266	#00ff00	3
85	Fight from the Inside	1977-10-28	183	#00ff00	3
86	Get Down, Make Love	1977-10-28	231	#00ff00	3
87	Sleeping on the Sidewalk	1977-10-28	188	#00ff00	3
88	Who Needs You	1977-10-28	186	#00ff00	3
89	It's Late	1977-10-28	387	#00ff00	3
90	My Melancholy Blues	1977-10-28	209	#00ff00	3
91	Play The Game	1980-06-30	213	#00ff40	3
92	Dragon Attack	1980-06-30	259	#00ff40	3
93	Another One Bites The Dust	1980-06-30	212	#00ff40	3
94	Need Your Loving Tonight	1980-06-30	169	#00ff40	3
95	Crazy Little Thing Called Love	1980-06-30	168	#00ff40	3
96	Rock It (Prime Jive)	1980-06-30	273	#00ff40	3
97	Don't Try Suicide	1980-06-30	232	#00ff40	3
98	Sail Away Sweet Sister (To the Siste I Never Had)	1980-06-30	213	#00ff40	3
99	Coming Soon	1980-06-30	171	#00ff40	3
100	Save Me	1980-06-30	229	#00ff40	3
\.


--
-- TOC entry 3437 (class 0 OID 16818)
-- Dependencies: 222
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
\.


--
-- TOC entry 3427 (class 0 OID 16726)
-- Dependencies: 212
-- Data for Name: playlist; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.playlist (id_utente, nome, descrizione, n_canzoni, id_playlist) FROM stdin;
15	Metallo	Void	47	1
\.


--
-- TOC entry 3436 (class 0 OID 16803)
-- Dependencies: 221
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
-- TOC entry 3434 (class 0 OID 16782)
-- Dependencies: 219
-- Data for Name: statistiche; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.statistiche (id_statistica, _13_19, _20_29, _30_39, _40_49, _50_65, _65piu, n_riproduzioni_totali, n_riproduzioni_settimanali) FROM stdin;
1	0	1	0	0	0	0	1500	37
2	0	1	0	0	0	0	3005	39
3	0	1	0	0	0	0	15000	41
4	0	1	0	0	0	0	100000	43
5	0	1	0	0	0	0	1500	45
6	0	1	0	0	0	0	3005	47
7	0	1	0	0	0	0	15000	49
8	0	1	0	0	0	0	100000	51
9	0	1	0	0	0	0	1500	53
10	0	1	0	0	0	0	3005	55
11	0	1	0	0	0	0	15000	57
12	0	1	0	0	0	0	100000	59
13	0	1	0	0	0	0	1500	61
14	0	1	0	0	0	0	3005	63
15	0	1	0	0	0	0	15000	65
16	0	1	0	0	0	0	100000	67
17	0	1	0	0	0	0	1500	69
18	0	1	0	0	0	0	3005	71
19	0	1	0	0	0	0	15000	73
20	0	1	0	0	0	0	100000	75
21	0	1	0	0	0	0	1500	77
22	0	1	0	0	0	0	3005	79
23	0	1	0	0	0	0	15000	81
24	0	1	0	0	0	0	100000	83
25	0	1	0	0	0	0	1500	85
26	0	1	0	0	0	0	3005	87
27	0	1	0	0	0	0	15000	89
28	0	1	0	0	0	0	100000	91
29	0	1	0	0	0	0	1500	93
30	0	1	0	0	0	0	3005	95
31	0	1	0	0	0	0	15000	97
32	0	1	0	0	0	0	100000	99
33	0	1	0	0	0	0	1500	101
34	0	1	0	0	0	0	3005	103
35	0	1	0	0	0	0	15000	105
36	0	1	0	0	0	0	100000	107
37	0	1	0	0	0	0	1500	109
38	0	1	0	0	0	0	3005	111
39	0	1	0	0	0	0	15000	113
40	0	1	0	0	0	0	100000	115
41	0	1	0	0	0	0	1500	117
42	0	1	0	0	0	0	3005	119
43	0	1	0	0	0	0	15000	121
44	0	1	0	0	0	0	100000	123
45	0	1	0	0	0	0	1500	125
46	0	1	0	0	0	0	3005	127
47	0	1	0	0	0	0	15000	129
\.


--
-- TOC entry 3441 (class 0 OID 16885)
-- Dependencies: 226
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
\.


--
-- TOC entry 3435 (class 0 OID 16796)
-- Dependencies: 220
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
\.


--
-- TOC entry 3425 (class 0 OID 16701)
-- Dependencies: 210
-- Data for Name: utenti; Type: TABLE DATA; Schema: unive_music; Owner: postgres
--

COPY unive_music.utenti (id_utente, email, nome, cognome, nickname, bio, data_nascita, password, ruolo) FROM stdin;
1	admin@admin	admin	admin	admin		2022-05-06	pbkdf2:sha256:260000$HyITCi2RzlpcYFEd$4d6cf16e30c50b11e8c43cc3cd8cbdb83c5212d0a43f0b53ef3b48a721acdcb3	3
2	metallica@gmail.com	James	Hetfield	Metallica	I Metallica sono un gruppo musicale heavy metal statunitense, formatosi a Los Angeles nel 1981.	2022-05-06	pbkdf2:sha256:260000$TKgmXkoQ7EqJy8UP$e6c26b664737fe0738063e84da6100a58ec0f0c02324c05b2c4aa67a1ea822bf	2
3	queen@gmail.com	Freddie	Mercury	Queen	I Queen sono un gruppo musicale rock britannico, formatosi a Londra nel 1970 dall'incontro del cantante e pianista Freddie Mercury con il chitarrista Brian May e con il batterista Roger Taylor.	2022-05-06	pbkdf2:sha256:260000$2zKkxjj9oDQQ2E2w$863c39830294a752c0b06c33ec815f04d6265531682bec37d0ace0f8f37f699f	2
4	gunsnroses@gmail.com	Guns'n'Roses	Guns'n'Roses	Guns'n'Roses		2022-05-06	pbkdf2:sha256:260000$6G2a8uJWPr5zZSJw$cadf347d88323211cba8f22d78a843855782a372aabc134434a5ca2cfc7f717a	2
5	ligabue@gmail.com	Luciano	Ligabue	Ligabue		2022-05-06	pbkdf2:sha256:260000$4yii8iBkz4qdftZW$568d515e5cef30771b5edaae23a83d8dca7cb51c39ca94c0c0375f04b98954d9	2
6	vasco@gmail.com	Vasco	Rossi	Vasco		2022-05-06	pbkdf2:sha256:260000$QFdPjh2nwxamVckr$dc50c35d43905bad09a506c6f4a809ff5bb3cc1dd2c43a72f909ecd47c7c0b59	2
7	rammstein@gmail.com	Rammstein	Rammstein	Rammstein		2022-05-06	pbkdf2:sha256:260000$gKAECUhyTC7F2AkX$5fda6d9b965bf7191cceed5fcb73b201a9afc158dcca8ff40fc30e9c4b1cd30e	2
8	sabaton@gmail.com	Sabaton	Sabaton	Sabaton		2022-05-06	pbkdf2:sha256:260000$cUgueIuKsPl60etz$174d07c94c636bbb2f628802066f947fdafcb2b1dd998a0743c02db01fb3df9c	2
9	linkinpark@gmail.com	Linkin Park	Linkin Park	Linkin Park		2022-05-06	pbkdf2:sha256:260000$GuL4xMK4x61H7I7L$b000160889e5a108ce6cdda59ea06ccf2f43c0b5424c4853156bcc0401aa5095	2
10	pausini@gmail.com	Laura	Pausini	Laura Pausini		2022-05-06	pbkdf2:sha256:260000$te2B9b9TaMTesRJZ$8810f7e8706e081db705ec1929e94019fbf1e19389136a1ae2e78d04d9e86917	2
11	mahmood@gmail.com	Alessandro	Mahmoud	Mahmood		2022-05-06	pbkdf2:sha256:260000$xc8fUhijFCtgfrFA$833c24330a94f977641a4623318c4df637d3fdc94573a61c93a5d276b41075f8	2
12	bocelli@gmail.com	Andrea	Bocelli	Andrea Bocelli		2022-05-06	pbkdf2:sha256:260000$Xud1zVIaa60VMM78$22d6c010517041f9ece1cb10d0ffbe0d649c3d3cceed5a495e8582d4a5749b24	2
13	elisa@gmail.com	Elisa	Toffoli	Elisa		2022-05-06	pbkdf2:sha256:260000$asYEUrzfdC9qpuHt$21f61c19431766fb5b73e5a8ba95462bb25b4e0f95d2f0238a324f3c5599c0ef	2
14	rickymartin@gmail.com	Enrique Martin	Morales	Ricky Martin		2022-05-06	pbkdf2:sha256:260000$Rv9uKQn5bOwEMVIl$eebec1a15f9d6196e66a547ac7db0a195ca87cb431943d1007a216fab6ea256b	2
15	massimiliano@gmail.com	Massimiliano	Zuin	Massimiliano Zuin		1996-07-23	pbkdf2:sha256:260000$babUZeqTUvUIAWJS$3ccd7db746e1fae861010a75e5782ac0bb468774649b33c583dbabd7c08ba11d	1
16	marco@gmail.com	Marco	Quarta	Marco Quarta		2022-05-06	pbkdf2:sha256:260000$E9m40HGcxW9pam50$eb4a2c352c9a2d9c1b099711ee5688915f9b7dee4065f55d5361b5b5292f4c86	1
17	michele@gmail.com	Michele	Lattanzi	Michele Lattanzi		2022-05-06	pbkdf2:sha256:260000$83qlZp5n3w1SWIWj$96cc0d189f597a83afeb11b8775b9771fd1f2225565986cdfc66432356662f60	1
\.


--
-- TOC entry 3452 (class 0 OID 0)
-- Dependencies: 209
-- Name: Utenti_IdUtenti_seq; Type: SEQUENCE SET; Schema: unive_music; Owner: postgres
--

SELECT pg_catalog.setval('unive_music."Utenti_IdUtenti_seq"', 1, false);


--
-- TOC entry 3453 (class 0 OID 0)
-- Dependencies: 216
-- Name: album_id_album_seq; Type: SEQUENCE SET; Schema: unive_music; Owner: postgres
--

SELECT pg_catalog.setval('unive_music.album_id_album_seq', 1, false);


--
-- TOC entry 3454 (class 0 OID 0)
-- Dependencies: 213
-- Name: canzoni_id_canzone_seq; Type: SEQUENCE SET; Schema: unive_music; Owner: postgres
--

SELECT pg_catalog.setval('unive_music.canzoni_id_canzone_seq', 1, false);


--
-- TOC entry 3455 (class 0 OID 0)
-- Dependencies: 215
-- Name: playlist_id_playlist_seq; Type: SEQUENCE SET; Schema: unive_music; Owner: postgres
--

SELECT pg_catalog.setval('unive_music.playlist_id_playlist_seq', 1, false);


--
-- TOC entry 3456 (class 0 OID 0)
-- Dependencies: 218
-- Name: statistiche_id_statistica_seq; Type: SEQUENCE SET; Schema: unive_music; Owner: postgres
--

SELECT pg_catalog.setval('unive_music.statistiche_id_statistica_seq', 1, false);


--
-- TOC entry 3221 (class 2606 OID 16900)
-- Name: playlist check_n_canzoni; Type: CHECK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE unive_music.playlist
    ADD CONSTRAINT check_n_canzoni CHECK ((n_canzoni >= 0)) NOT VALID;


--
-- TOC entry 3225 (class 2606 OID 16901)
-- Name: album check_n_canzoni_album; Type: CHECK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE unive_music.album
    ADD CONSTRAINT check_n_canzoni_album CHECK ((n_canzoni >= 0)) NOT VALID;


--
-- TOC entry 3218 (class 2606 OID 16715)
-- Name: utenti check_ruolo; Type: CHECK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE unive_music.utenti
    ADD CONSTRAINT check_ruolo CHECK (((ruolo > 0) AND (ruolo < 4))) NOT VALID;


--
-- TOC entry 3250 (class 2606 OID 16775)
-- Name: album key_album; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.album
    ADD CONSTRAINT key_album UNIQUE (titolo, rilascio, id_artista);


--
-- TOC entry 3246 (class 2606 OID 16749)
-- Name: canzoni key_canzone; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.canzoni
    ADD CONSTRAINT key_canzone UNIQUE (titolo, rilascio, id_artista);


--
-- TOC entry 3236 (class 2606 OID 16711)
-- Name: utenti key_email; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.utenti
    ADD CONSTRAINT key_email UNIQUE (email);


--
-- TOC entry 3238 (class 2606 OID 16713)
-- Name: utenti key_nickname; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.utenti
    ADD CONSTRAINT key_nickname UNIQUE (nickname);


--
-- TOC entry 3264 (class 2606 OID 16856)
-- Name: attributo_album pk_attributo_album; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.attributo_album
    ADD CONSTRAINT pk_attributo_album PRIMARY KEY (id_tag, id_album);


--
-- TOC entry 3262 (class 2606 OID 16839)
-- Name: attributo_canzone pk_attributo_canzone; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.attributo_canzone
    ADD CONSTRAINT pk_attributo_canzone PRIMARY KEY (id_tag, id_canzone);


--
-- TOC entry 3266 (class 2606 OID 16873)
-- Name: attributo_playlist pk_attributo_playlist; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.attributo_playlist
    ADD CONSTRAINT pk_attributo_playlist PRIMARY KEY (id_playlist, id_tag);


--
-- TOC entry 3260 (class 2606 OID 16822)
-- Name: contenuto pk_contenuto; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.contenuto
    ADD CONSTRAINT pk_contenuto PRIMARY KEY (id_album, id_canzone);


--
-- TOC entry 3252 (class 2606 OID 16773)
-- Name: album pk_id_album; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.album
    ADD CONSTRAINT pk_id_album PRIMARY KEY (id_album);


--
-- TOC entry 3242 (class 2606 OID 16720)
-- Name: artisti pk_id_artista; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.artisti
    ADD CONSTRAINT pk_id_artista PRIMARY KEY (id_utente);


--
-- TOC entry 3248 (class 2606 OID 16747)
-- Name: canzoni pk_id_canzone; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.canzoni
    ADD CONSTRAINT pk_id_canzone PRIMARY KEY (id_canzone);


--
-- TOC entry 3254 (class 2606 OID 16795)
-- Name: statistiche pk_id_statistica; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.statistiche
    ADD CONSTRAINT pk_id_statistica PRIMARY KEY (id_statistica);


--
-- TOC entry 3240 (class 2606 OID 16709)
-- Name: utenti pk_id_utente; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.utenti
    ADD CONSTRAINT pk_id_utente PRIMARY KEY (id_utente);


--
-- TOC entry 3244 (class 2606 OID 16763)
-- Name: playlist pk_playlist; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.playlist
    ADD CONSTRAINT pk_playlist PRIMARY KEY (id_playlist);


--
-- TOC entry 3258 (class 2606 OID 16807)
-- Name: raccolte pk_raccolte; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.raccolte
    ADD CONSTRAINT pk_raccolte PRIMARY KEY (id_playlist, id_canzone);


--
-- TOC entry 3268 (class 2606 OID 16889)
-- Name: statistiche_canzoni pk_statistiche_canzoni; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.statistiche_canzoni
    ADD CONSTRAINT pk_statistiche_canzoni PRIMARY KEY (id_statistica, id_canzone);


--
-- TOC entry 3256 (class 2606 OID 16802)
-- Name: tag pk_tag; Type: CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.tag
    ADD CONSTRAINT pk_tag PRIMARY KEY (tag);


--
-- TOC entry 3275 (class 2606 OID 16823)
-- Name: contenuto fk_album; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.contenuto
    ADD CONSTRAINT fk_album FOREIGN KEY (id_album) REFERENCES unive_music.album(id_album) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 3280 (class 2606 OID 16862)
-- Name: attributo_album fk_album; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.attributo_album
    ADD CONSTRAINT fk_album FOREIGN KEY (id_album) REFERENCES unive_music.album(id_album) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3271 (class 2606 OID 16750)
-- Name: canzoni fk_artista; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.canzoni
    ADD CONSTRAINT fk_artista FOREIGN KEY (id_artista) REFERENCES unive_music.artisti(id_utente) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3272 (class 2606 OID 16776)
-- Name: album fk_artista; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.album
    ADD CONSTRAINT fk_artista FOREIGN KEY (id_artista) REFERENCES unive_music.artisti(id_utente) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3274 (class 2606 OID 16813)
-- Name: raccolte fk_canzone; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.raccolte
    ADD CONSTRAINT fk_canzone FOREIGN KEY (id_canzone) REFERENCES unive_music.canzoni(id_canzone) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3276 (class 2606 OID 16828)
-- Name: contenuto fk_canzone; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.contenuto
    ADD CONSTRAINT fk_canzone FOREIGN KEY (id_canzone) REFERENCES unive_music.canzoni(id_canzone) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 3278 (class 2606 OID 16845)
-- Name: attributo_canzone fk_canzone; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.attributo_canzone
    ADD CONSTRAINT fk_canzone FOREIGN KEY (id_canzone) REFERENCES unive_music.canzoni(id_canzone) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3284 (class 2606 OID 16895)
-- Name: statistiche_canzoni fk_canzone; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.statistiche_canzoni
    ADD CONSTRAINT fk_canzone FOREIGN KEY (id_canzone) REFERENCES unive_music.canzoni(id_canzone) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3273 (class 2606 OID 16808)
-- Name: raccolte fk_playlist; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.raccolte
    ADD CONSTRAINT fk_playlist FOREIGN KEY (id_playlist) REFERENCES unive_music.playlist(id_playlist) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3282 (class 2606 OID 16879)
-- Name: attributo_playlist fk_playlist; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.attributo_playlist
    ADD CONSTRAINT fk_playlist FOREIGN KEY (id_playlist) REFERENCES unive_music.playlist(id_playlist) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3283 (class 2606 OID 16890)
-- Name: statistiche_canzoni fk_statistica; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.statistiche_canzoni
    ADD CONSTRAINT fk_statistica FOREIGN KEY (id_statistica) REFERENCES unive_music.statistiche(id_statistica) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3277 (class 2606 OID 16840)
-- Name: attributo_canzone fk_tag; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.attributo_canzone
    ADD CONSTRAINT fk_tag FOREIGN KEY (id_tag) REFERENCES unive_music.tag(tag) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3279 (class 2606 OID 16857)
-- Name: attributo_album fk_tag; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.attributo_album
    ADD CONSTRAINT fk_tag FOREIGN KEY (id_tag) REFERENCES unive_music.tag(tag) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3281 (class 2606 OID 16874)
-- Name: attributo_playlist fk_tag; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.attributo_playlist
    ADD CONSTRAINT fk_tag FOREIGN KEY (id_tag) REFERENCES unive_music.tag(tag) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3269 (class 2606 OID 16721)
-- Name: artisti fk_utenti; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.artisti
    ADD CONSTRAINT fk_utenti FOREIGN KEY (id_utente) REFERENCES unive_music.utenti(id_utente) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3270 (class 2606 OID 16734)
-- Name: playlist fk_utenti; Type: FK CONSTRAINT; Schema: unive_music; Owner: postgres
--

ALTER TABLE ONLY unive_music.playlist
    ADD CONSTRAINT fk_utenti FOREIGN KEY (id_utente) REFERENCES unive_music.utenti(id_utente) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


-- Completed on 2022-07-02 16:19:59

--
-- PostgreSQL database dump complete
--

