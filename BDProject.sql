--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4
-- Dumped by pg_dump version 14.4

-- Started on 2022-08-16 18:04:51

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


-- Completed on 2022-08-16 18:04:51

--
-- PostgreSQL database dump complete
--

