--
-- PostgreSQL database dump
--

-- Dumped from database version 14.2
-- Dumped by pg_dump version 14.2

-- Started on 2022-07-02 16:41:30

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
-- TOC entry 3429 (class 0 OID 0)
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
-- TOC entry 3430 (class 0 OID 0)
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
-- TOC entry 3431 (class 0 OID 0)
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
-- TOC entry 3432 (class 0 OID 0)
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
-- TOC entry 3433 (class 0 OID 0)
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


-- Completed on 2022-07-02 16:41:31

--
-- PostgreSQL database dump complete
--

