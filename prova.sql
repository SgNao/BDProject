--
-- PostgreSQL database dump
--

-- Dumped from database version 14.2
-- Dumped by pg_dump version 14.2

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

DROP DATABASE "DBProject";
--
-- Name: DBProject; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "DBProject" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_United States.1252';


ALTER DATABASE "DBProject" OWNER TO postgres;

\connect "DBProject"

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
-- Name: BDProject; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA "BDProject";


ALTER SCHEMA "BDProject" OWNER TO postgres;

SET default_tablespace = "BDProject";

SET default_table_access_method = heap;

--
-- Name: Album; Type: TABLE; Schema: BDProject; Owner: postgres; Tablespace: BDProject
--

CREATE TABLE "BDProject"."Album" (
    "IdAlbum" integer NOT NULL,
    "Titolo" text NOT NULL,
    "Rilascio" date NOT NULL,
    "Colore" text NOT NULL,
    "NCanzoni" integer DEFAULT 0,
    "CasaDiscografica" text,
    "IdArtista" integer NOT NULL
);


ALTER TABLE "BDProject"."Album" OWNER TO postgres;

--
-- Name: Album_IdAlbum_seq; Type: SEQUENCE; Schema: BDProject; Owner: postgres
--

CREATE SEQUENCE "BDProject"."Album_IdAlbum_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "BDProject"."Album_IdAlbum_seq" OWNER TO postgres;

--
-- Name: Album_IdAlbum_seq; Type: SEQUENCE OWNED BY; Schema: BDProject; Owner: postgres
--

ALTER SEQUENCE "BDProject"."Album_IdAlbum_seq" OWNED BY "BDProject"."Album"."IdAlbum";


--
-- Name: Artisti; Type: TABLE; Schema: BDProject; Owner: postgres; Tablespace: BDProject
--

CREATE TABLE "BDProject"."Artisti" (
    "IdUtente" integer NOT NULL,
    "Debutto" date
);


ALTER TABLE "BDProject"."Artisti" OWNER TO postgres;

--
-- Name: Canzoni; Type: TABLE; Schema: BDProject; Owner: postgres; Tablespace: BDProject
--

CREATE TABLE "BDProject"."Canzoni" (
    "IdCanzone" integer NOT NULL,
    "Titolo" text NOT NULL,
    "Rilascio" date NOT NULL,
    "Durata" integer NOT NULL,
    "Colore" text NOT NULL,
    "Lingua" text NOT NULL,
    "IdArtista" integer NOT NULL
);


ALTER TABLE "BDProject"."Canzoni" OWNER TO postgres;

--
-- Name: Canzoni_IdCanzone_seq; Type: SEQUENCE; Schema: BDProject; Owner: postgres
--

CREATE SEQUENCE "BDProject"."Canzoni_IdCanzone_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "BDProject"."Canzoni_IdCanzone_seq" OWNER TO postgres;

--
-- Name: Canzoni_IdCanzone_seq; Type: SEQUENCE OWNED BY; Schema: BDProject; Owner: postgres
--

ALTER SEQUENCE "BDProject"."Canzoni_IdCanzone_seq" OWNED BY "BDProject"."Canzoni"."IdCanzone";


--
-- Name: Playlist; Type: TABLE; Schema: BDProject; Owner: postgres; Tablespace: BDProject
--

CREATE TABLE "BDProject"."Playlist" (
    "IdPlaylist" integer NOT NULL,
    "IdUtente" integer NOT NULL,
    "Nome" text NOT NULL,
    "Descrizione" text,
    "NCanzoni" integer
);


ALTER TABLE "BDProject"."Playlist" OWNER TO postgres;

--
-- Name: Playlist_IdPlaylist_seq; Type: SEQUENCE; Schema: BDProject; Owner: postgres
--

CREATE SEQUENCE "BDProject"."Playlist_IdPlaylist_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "BDProject"."Playlist_IdPlaylist_seq" OWNER TO postgres;

--
-- Name: Playlist_IdPlaylist_seq; Type: SEQUENCE OWNED BY; Schema: BDProject; Owner: postgres
--

ALTER SEQUENCE "BDProject"."Playlist_IdPlaylist_seq" OWNED BY "BDProject"."Playlist"."IdPlaylist";


--
-- Name: Statistiche; Type: TABLE; Schema: BDProject; Owner: postgres; Tablespace: BDProject
--

CREATE TABLE "BDProject"."Statistiche" (
    "IdStatistica" integer NOT NULL,
    "13-19" integer DEFAULT 0 NOT NULL,
    "20-29" integer DEFAULT 0 NOT NULL,
    "30-39" integer DEFAULT 0 NOT NULL,
    "40-49" integer DEFAULT 0 NOT NULL,
    "50-65" integer DEFAULT 0 NOT NULL,
    "65+" integer DEFAULT 0 NOT NULL,
    "NRiproduzioniTotali" integer DEFAULT 0 NOT NULL,
    "NRiproduzioniSettimanali" integer DEFAULT 0 NOT NULL
);


ALTER TABLE "BDProject"."Statistiche" OWNER TO postgres;

--
-- Name: Statistiche_IdStatistica_seq; Type: SEQUENCE; Schema: BDProject; Owner: postgres
--

CREATE SEQUENCE "BDProject"."Statistiche_IdStatistica_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "BDProject"."Statistiche_IdStatistica_seq" OWNER TO postgres;

--
-- Name: Statistiche_IdStatistica_seq; Type: SEQUENCE OWNED BY; Schema: BDProject; Owner: postgres
--

ALTER SEQUENCE "BDProject"."Statistiche_IdStatistica_seq" OWNED BY "BDProject"."Statistiche"."IdStatistica";


--
-- Name: Tag; Type: TABLE; Schema: BDProject; Owner: postgres; Tablespace: BDProject
--

CREATE TABLE "BDProject"."Tag" (
    "Tag" text NOT NULL
);


ALTER TABLE "BDProject"."Tag" OWNER TO postgres;

--
-- Name: Utenti; Type: TABLE; Schema: BDProject; Owner: postgres; Tablespace: BDProject
--

CREATE TABLE "BDProject"."Utenti" (
    "IdUtente" integer NOT NULL,
    "Email" text NOT NULL,
    "Nome" text NOT NULL,
    "Cognome" text NOT NULL,
    "Nickname" text NOT NULL,
    "Bio" text,
    "DataNascita" date NOT NULL,
    "Password" text NOT NULL,
    "Ruolo" integer NOT NULL
);


ALTER TABLE "BDProject"."Utenti" OWNER TO postgres;

--
-- Name: Utenti_IdUtenti_seq; Type: SEQUENCE; Schema: BDProject; Owner: postgres
--

CREATE SEQUENCE "BDProject"."Utenti_IdUtenti_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "BDProject"."Utenti_IdUtenti_seq" OWNER TO postgres;

--
-- Name: Utenti_IdUtenti_seq; Type: SEQUENCE OWNED BY; Schema: BDProject; Owner: postgres
--

ALTER SEQUENCE "BDProject"."Utenti_IdUtenti_seq" OWNED BY "BDProject"."Utenti"."IdUtente";


--
-- Name: zAttrAlbum; Type: TABLE; Schema: BDProject; Owner: postgres; Tablespace: BDProject
--

CREATE TABLE "BDProject"."zAttrAlbum" (
    "IdTag" text NOT NULL,
    "IdAlbum" integer NOT NULL
);


ALTER TABLE "BDProject"."zAttrAlbum" OWNER TO postgres;

--
-- Name: zAttrCanzone; Type: TABLE; Schema: BDProject; Owner: postgres; Tablespace: BDProject
--

CREATE TABLE "BDProject"."zAttrCanzone" (
    "IdTag" text NOT NULL,
    "IdCanzone" integer NOT NULL
);


ALTER TABLE "BDProject"."zAttrCanzone" OWNER TO postgres;

--
-- Name: zAttrPlaylist; Type: TABLE; Schema: BDProject; Owner: postgres; Tablespace: BDProject
--

CREATE TABLE "BDProject"."zAttrPlaylist" (
    "IdTag" text NOT NULL,
    "IdPlaylist" integer NOT NULL
);


ALTER TABLE "BDProject"."zAttrPlaylist" OWNER TO postgres;

--
-- Name: zContenuto; Type: TABLE; Schema: BDProject; Owner: postgres; Tablespace: BDProject
--

CREATE TABLE "BDProject"."zContenuto" (
    "IdAlbum" integer NOT NULL,
    "IdCanzone" integer NOT NULL
);


ALTER TABLE "BDProject"."zContenuto" OWNER TO postgres;

--
-- Name: zRaccolte; Type: TABLE; Schema: BDProject; Owner: postgres; Tablespace: BDProject
--

CREATE TABLE "BDProject"."zRaccolte" (
    "IdPlaylist" integer NOT NULL,
    "IdCanzone" integer NOT NULL
);


ALTER TABLE "BDProject"."zRaccolte" OWNER TO postgres;

--
-- Name: zStatCanzoni; Type: TABLE; Schema: BDProject; Owner: postgres; Tablespace: BDProject
--

CREATE TABLE "BDProject"."zStatCanzoni" (
    "IdStatistica" integer NOT NULL,
    "IdCanzone" integer NOT NULL
);


ALTER TABLE "BDProject"."zStatCanzoni" OWNER TO postgres;

--
-- Name: Album IdAlbum; Type: DEFAULT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."Album" ALTER COLUMN "IdAlbum" SET DEFAULT nextval('"BDProject"."Album_IdAlbum_seq"'::regclass);


--
-- Name: Canzoni IdCanzone; Type: DEFAULT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."Canzoni" ALTER COLUMN "IdCanzone" SET DEFAULT nextval('"BDProject"."Canzoni_IdCanzone_seq"'::regclass);


--
-- Name: Playlist IdPlaylist; Type: DEFAULT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."Playlist" ALTER COLUMN "IdPlaylist" SET DEFAULT nextval('"BDProject"."Playlist_IdPlaylist_seq"'::regclass);


--
-- Name: Statistiche IdStatistica; Type: DEFAULT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."Statistiche" ALTER COLUMN "IdStatistica" SET DEFAULT nextval('"BDProject"."Statistiche_IdStatistica_seq"'::regclass);


--
-- Name: Utenti IdUtente; Type: DEFAULT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."Utenti" ALTER COLUMN "IdUtente" SET DEFAULT nextval('"BDProject"."Utenti_IdUtenti_seq"'::regclass);


SET default_tablespace = '';

--
-- Name: Album AlbumPK; Type: CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."Album"
    ADD CONSTRAINT "AlbumPK" PRIMARY KEY ("IdAlbum");


--
-- Name: Artisti ArtistiPK; Type: CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."Artisti"
    ADD CONSTRAINT "ArtistiPK" PRIMARY KEY ("IdUtente");


--
-- Name: zAttrAlbum AttrAlbumPK; Type: CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."zAttrAlbum"
    ADD CONSTRAINT "AttrAlbumPK" PRIMARY KEY ("IdTag", "IdAlbum");


--
-- Name: zAttrCanzone AttrCanzoneFK; Type: CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."zAttrCanzone"
    ADD CONSTRAINT "AttrCanzoneFK" PRIMARY KEY ("IdTag", "IdCanzone");


--
-- Name: zAttrPlaylist AttrPlaylistPK; Type: CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."zAttrPlaylist"
    ADD CONSTRAINT "AttrPlaylistPK" PRIMARY KEY ("IdTag", "IdPlaylist");


--
-- Name: Canzoni CanzonePK; Type: CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."Canzoni"
    ADD CONSTRAINT "CanzonePK" PRIMARY KEY ("IdCanzone");


--
-- Name: zContenuto ContenutoPK; Type: CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."zContenuto"
    ADD CONSTRAINT "ContenutoPK" PRIMARY KEY ("IdAlbum", "IdCanzone");


--
-- Name: Playlist PlaylistPK; Type: CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."Playlist"
    ADD CONSTRAINT "PlaylistPK" PRIMARY KEY ("IdPlaylist");


--
-- Name: zRaccolte RaccoltePK; Type: CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."zRaccolte"
    ADD CONSTRAINT "RaccoltePK" PRIMARY KEY ("IdPlaylist", "IdCanzone");


--
-- Name: zStatCanzoni StaCanzoniPK; Type: CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."zStatCanzoni"
    ADD CONSTRAINT "StaCanzoniPK" PRIMARY KEY ("IdStatistica", "IdCanzone");


--
-- Name: Statistiche StatistichePK; Type: CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."Statistiche"
    ADD CONSTRAINT "StatistichePK" PRIMARY KEY ("IdStatistica");


--
-- Name: Tag TagPK; Type: CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."Tag"
    ADD CONSTRAINT "TagPK" PRIMARY KEY ("Tag");


--
-- Name: Utenti UtentiPK; Type: CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."Utenti"
    ADD CONSTRAINT "UtentiPK" PRIMARY KEY ("IdUtente");


--
-- Name: Utenti Utenti_Nickname_key; Type: CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."Utenti"
    ADD CONSTRAINT "Utenti_Nickname_key" UNIQUE ("Nickname");


--
-- Name: zContenuto AlbumFK; Type: FK CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."zContenuto"
    ADD CONSTRAINT "AlbumFK" FOREIGN KEY ("IdAlbum") REFERENCES "BDProject"."Album"("IdAlbum");


--
-- Name: zAttrAlbum AlbumFK; Type: FK CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."zAttrAlbum"
    ADD CONSTRAINT "AlbumFK" FOREIGN KEY ("IdAlbum") REFERENCES "BDProject"."Album"("IdAlbum") ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- Name: Canzoni ArtistaFK; Type: FK CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."Canzoni"
    ADD CONSTRAINT "ArtistaFK" FOREIGN KEY ("IdArtista") REFERENCES "BDProject"."Artisti"("IdUtente") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Album ArtistaFK; Type: FK CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."Album"
    ADD CONSTRAINT "ArtistaFK" FOREIGN KEY ("IdArtista") REFERENCES "BDProject"."Artisti"("IdUtente") ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- Name: zContenuto CanzoneFK; Type: FK CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."zContenuto"
    ADD CONSTRAINT "CanzoneFK" FOREIGN KEY ("IdCanzone") REFERENCES "BDProject"."Canzoni"("IdCanzone");


--
-- Name: zAttrCanzone CanzoneFK; Type: FK CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."zAttrCanzone"
    ADD CONSTRAINT "CanzoneFK" FOREIGN KEY ("IdCanzone") REFERENCES "BDProject"."Canzoni"("IdCanzone");


--
-- Name: zStatCanzoni CanzoneFK; Type: FK CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."zStatCanzoni"
    ADD CONSTRAINT "CanzoneFK" FOREIGN KEY ("IdCanzone") REFERENCES "BDProject"."Canzoni"("IdCanzone");


--
-- Name: zRaccolte IdCanzoneFK; Type: FK CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."zRaccolte"
    ADD CONSTRAINT "IdCanzoneFK" FOREIGN KEY ("IdCanzone") REFERENCES "BDProject"."Canzoni"("IdCanzone");


--
-- Name: zRaccolte IdPlaylistFK; Type: FK CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."zRaccolte"
    ADD CONSTRAINT "IdPlaylistFK" FOREIGN KEY ("IdPlaylist") REFERENCES "BDProject"."Playlist"("IdPlaylist");


--
-- Name: zAttrPlaylist PlaylistFK; Type: FK CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."zAttrPlaylist"
    ADD CONSTRAINT "PlaylistFK" FOREIGN KEY ("IdPlaylist") REFERENCES "BDProject"."Playlist"("IdPlaylist");


--
-- Name: zStatCanzoni StatisticaFK; Type: FK CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."zStatCanzoni"
    ADD CONSTRAINT "StatisticaFK" FOREIGN KEY ("IdStatistica") REFERENCES "BDProject"."Statistiche"("IdStatistica") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: zAttrCanzone TagFK; Type: FK CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."zAttrCanzone"
    ADD CONSTRAINT "TagFK" FOREIGN KEY ("IdTag") REFERENCES "BDProject"."Tag"("Tag");


--
-- Name: zAttrPlaylist TagFK; Type: FK CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."zAttrPlaylist"
    ADD CONSTRAINT "TagFK" FOREIGN KEY ("IdTag") REFERENCES "BDProject"."Tag"("Tag");


--
-- Name: zAttrAlbum TagFK; Type: FK CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."zAttrAlbum"
    ADD CONSTRAINT "TagFK" FOREIGN KEY ("IdTag") REFERENCES "BDProject"."Tag"("Tag") NOT VALID;


--
-- Name: Artisti UtenteFK; Type: FK CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."Artisti"
    ADD CONSTRAINT "UtenteFK" FOREIGN KEY ("IdUtente") REFERENCES "BDProject"."Utenti"("IdUtente") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Playlist UtenteFK; Type: FK CONSTRAINT; Schema: BDProject; Owner: postgres
--

ALTER TABLE ONLY "BDProject"."Playlist"
    ADD CONSTRAINT "UtenteFK" FOREIGN KEY ("IdUtente") REFERENCES "BDProject"."Utenti"("IdUtente") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

