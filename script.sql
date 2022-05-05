create table "DBProject"."Utenti"
(
    "Nickname"     text not null
        constraint utenti_pk
            primary key,
    "Nome"         text not null,
    "Cognome"      text not null,
    "Data_nascita" date not null,
    email          text not null,
    password       text not null
);

alter table "DBProject"."Utenti"
    owner to postgres;

create unique index utenti_email_uindex
    on "DBProject"."Utenti" (email);

create table "DBProject"."Artisti"
(
    id_utente text not null
        constraint artisti_pk
            primary key
        constraint artisti_utenti_nickname_fk
            references "DBProject"."Utenti"
            on update cascade on delete cascade,
    bio       text,
    debutto   date
);

alter table "DBProject"."Artisti"
    owner to postgres;

create table "DBProject"."Playlist"
(
    id          integer not null
        constraint playlist_pk
            primary key,
    id_utente   text
        constraint playlist_utenti_nickname_fk
            references "DBProject"."Utenti"
            on update cascade on delete cascade,
    nome        text    not null,
    descrizione text,
    tag         text,
    n_canzoni   integer
);

alter table "DBProject"."Playlist"
    owner to postgres;

create table "DBProject"."Canzoni"
(
    id             serial
        constraint canzoni_pk
            primary key,
    titolo         text,
    anno           smallint,
    durata         integer,
    genere         text,
    tag            text,
    n_riproduzioni integer not null,
    id_artista     text    not null
        constraint canzoni_artisti_id_utente_fk
            references "DBProject"."Artisti"
            on update cascade on delete cascade,
    lingua         text
);

alter table "DBProject"."Canzoni"
    owner to postgres;

create table "DBProject"."Album"
(
    id                serial
        constraint album_pk
            primary key,
    titolo            text    not null,
    anno              smallint,
    genere            text,
    n_canzoni         integer not null,
    casa_discografica text,
    id_artista        text
        constraint album_artisti_id_utente_fk
            references "DBProject"."Artisti"
            on update cascade on delete cascade
);

alter table "DBProject"."Album"
    owner to postgres;

create table "DBProject".raccolte
(
    id_playlist integer not null
        constraint raccolte_playlist_id_fk
            references "DBProject"."Playlist"
            on update cascade on delete cascade,
    id_canzone  integer not null
        constraint raccolte_canzoni_id_fk
            references "DBProject"."Canzoni"
            on update cascade on delete cascade,
    constraint key_name
        primary key (id_playlist, id_canzone)
);

alter table "DBProject".raccolte
    owner to postgres;

create table "DBProject".contenuto
(
    id_canzone integer
        constraint contenuto_canzoni_id_fk
            references "DBProject"."Canzoni"
            on update cascade on delete cascade,
    id_album   integer
        constraint contenuto_album_id_fk
            references "DBProject"."Album"
            on update cascade on delete cascade
);

alter table "DBProject".contenuto
    owner to postgres;


