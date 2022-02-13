CREATE SCHEMA IF NOT EXISTS tjadb;

CREATE  TABLE tjadb.artists ( 
	id                   serial  PRIMARY KEY ,
	name_orig            text  NOT NULL ,
	name_en              text  NOT NULL ,
	link                 text   ,
	info                 text   ,
	CONSTRAINT unq_artists_name UNIQUE ( name_orig, name_en, info ) 
 );

CREATE  TABLE tjadb.difficulties ( 
	id                   serial  PRIMARY KEY ,
	name_jp              text  NOT NULL ,
	name_en              text  NOT NULL 
 );

CREATE  TABLE tjadb.genres ( 
	id                   serial  PRIMARY KEY ,
	name_en              text  NOT NULL ,
	name_jp              text  NOT NULL ,
	tja_genre            text  NOT NULL ,
	CONSTRAINT "Unq_Genres_title_en" UNIQUE ( name_en ) ,
	CONSTRAINT "Unq_Genres_title_jp" UNIQUE ( name_jp ) ,
	CONSTRAINT "Unq_Genres_tja_genre" UNIQUE ( tja_genre ) 
 );

CREATE  TABLE tjadb.languages ( 
	id                   serial  PRIMARY KEY ,
	name_orig            text   ,
	name_en              text 
 );

CREATE  TABLE tjadb.song_tags ( 
	id                   serial  PRIMARY KEY ,
	name_orig            text  NOT NULL ,
	name_en              text  NOT NULL 
 );

CREATE  TABLE tjadb.songlists ( 
	id                   serial  PRIMARY KEY ,
	name_orig            text  NOT NULL ,
	name_en              text  NOT NULL 
 );

CREATE  TABLE tjadb.sources ( 
	id                   serial  PRIMARY KEY ,
	name_orig            text  NOT NULL ,
	name_en              text  NOT NULL ,
	genre_id             integer   ,
	about                text 
 );

CREATE  TABLE tjadb.users ( 
	id                   serial  PRIMARY KEY ,
	charter_name         text   ,
	discord_id           bigint   ,
	email                text   ,
	"password"           text   ,
	salt                 text   ,
	hashcount            integer DEFAULT 4000  ,
	staff                boolean   ,
	image_url            text   ,
	about                text   ,
	preferred_difficulty_id integer   ,
	preferred_language_id integer DEFAULT 1 NOT NULL ,
	CONSTRAINT unq_users_email UNIQUE ( email ) ,
	CONSTRAINT unq_users_discord_id UNIQUE ( discord_id ) ,
	CONSTRAINT unq_users_charter_name UNIQUE ( charter_name ) 
 );

CREATE  TABLE tjadb.song_states ( 
        id                   serial  PRIMARY KEY ,
        name                 text  NOT NULL
 );

CREATE  TABLE tjadb.songs ( 
	id                   serial  PRIMARY KEY ,
	title_orig           text  NOT NULL ,
	title_en             text  NOT NULL ,
	subtitle_orig        text  NOT NULL ,
	subtitle_en          text  NOT NULL ,
	source_id            integer   ,
	bpm                  decimal  NOT NULL ,
	genre_id             integer  NOT NULL ,
	charter_id           integer  NOT NULL ,
	d_kantan             smallint   ,
	d_kantan_charter_id  integer   ,
	d_futsuu             smallint   ,
	d_futsuu_charter_id  integer   ,
	d_muzukashii         smallint   ,
	d_muzukashii_charter_id integer   ,
	d_oni                smallint   ,
	d_oni_charter_id     integer   ,
	d_ura                smallint   ,
	d_ura_charter_id     integer   ,
	d_tower              smallint   ,
	d_tower_lives        smallint   ,
	downloads            integer DEFAULT 0  ,
	last_updated         date  NOT NULL ,
	created              date  NOT NULL ,
	uploaded             date  NOT NULL ,
	info                 text   ,
	video_link           text   ,
        state_id             integer  NOT NULL,
	obj_tja              oid  NOT NULL ,
	obj_ogg              oid  NOT NULL ,
	obj_bg_video_picture oid ,
        tja_orig_md5         uuid  NOT NULL ,
        tja_en_md5           uuid  NOT NULL
 );

CREATE  TABLE tjadb.songs_in_songlists ( 
	song_id              integer  NOT NULL ,
	songlist_id          integer  NOT NULL ,
	CONSTRAINT pk_songs_in_songlists PRIMARY KEY ( song_id, songlist_id )
 );

CREATE  TABLE tjadb.tags_per_song ( 
	tag_id               integer  NOT NULL ,
	song_id              integer  NOT NULL ,
	CONSTRAINT pk_tags_per_song PRIMARY KEY ( tag_id, song_id )
 );

CREATE  TABLE tjadb.artists_per_song ( 
	song_id              integer  NOT NULL ,
	artist_id            integer  NOT NULL ,
	CONSTRAINT pk_artists_per_song PRIMARY KEY ( song_id, artist_id )
 );

CREATE  TABLE tjadb.song_comments ( 
	song_id              integer  NOT NULL ,
	user_id              integer  NOT NULL ,
	difficulty_id        integer  NOT NULL ,
	player_score         integer   ,
	player_cleared       boolean DEFAULT false  ,
	player_fc            boolean DEFAULT false  ,
	rating               integer   ,
	CONSTRAINT pk_song_comments PRIMARY KEY ( song_id, user_id, difficulty_id )
 );

CREATE  TABLE tjadb.song_of_the_day_history ( 
	"date"               date DEFAULT CURRENT_DATE NOT NULL ,
	song_id              integer  NOT NULL ,
	CONSTRAINT "Pk_Song_of_the_Day_History_date" PRIMARY KEY ( "date" )
 );

CREATE  TABLE tjadb.tjadb_settings (
        name      text  NOT NULL ,
        type      text  NOT NULL ,
        value     json   ,
        CONSTRAINT pk_tjadb_settings_id PRIMARY KEY ( name )
 );


ALTER TABLE tjadb.artists_per_song ADD CONSTRAINT fk_artists_per_song_artists FOREIGN KEY ( artist_id ) REFERENCES tjadb.artists( id ) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE tjadb.artists_per_song ADD CONSTRAINT fk_artists_per_song_songs FOREIGN KEY ( song_id ) REFERENCES tjadb.songs( id );

ALTER TABLE tjadb.song_comments ADD CONSTRAINT fk_song_comments_songs FOREIGN KEY ( song_id ) REFERENCES tjadb.songs( id );

ALTER TABLE tjadb.song_comments ADD CONSTRAINT fk_song_comments_users FOREIGN KEY ( user_id ) REFERENCES tjadb.users( id ) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE tjadb.song_comments ADD CONSTRAINT fk_song_comments_difficulties FOREIGN KEY ( difficulty_id ) REFERENCES tjadb.difficulties( id );

ALTER TABLE tjadb.song_of_the_day_history ADD CONSTRAINT fk_song_of_the_day_history FOREIGN KEY ( song_id ) REFERENCES tjadb.songs( id );

ALTER TABLE tjadb.songs ADD CONSTRAINT fk_songs_sources FOREIGN KEY ( source_id ) REFERENCES tjadb.sources( id ) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE tjadb.songs ADD CONSTRAINT fk_songs_genres FOREIGN KEY ( genre_id ) REFERENCES tjadb.genres( id );

ALTER TABLE tjadb.songs ADD CONSTRAINT fk_songs_users_charter FOREIGN KEY ( charter_id ) REFERENCES tjadb.users( id );

ALTER TABLE tjadb.songs ADD CONSTRAINT fk_songs_users_kantan FOREIGN KEY ( d_kantan_charter_id ) REFERENCES tjadb.users( id );

ALTER TABLE tjadb.songs ADD CONSTRAINT fk_songs_users_futsuu FOREIGN KEY ( d_futsuu_charter_id ) REFERENCES tjadb.users( id ) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE tjadb.songs ADD CONSTRAINT fk_songs_users_muzukashii FOREIGN KEY ( d_muzukashii_charter_id ) REFERENCES tjadb.users( id ) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE tjadb.songs ADD CONSTRAINT fk_songs_users_oni FOREIGN KEY ( d_oni_charter_id ) REFERENCES tjadb.users( id ) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE tjadb.songs ADD CONSTRAINT fk_songs_users_ura FOREIGN KEY ( d_ura_charter_id ) REFERENCES tjadb.users( id ) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE tjadb.songs ADD CONSTRAINT fk_songs_song_states FOREIGN KEY ( state_id ) REFERENCES tjadb.song_states( id ) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE tjadb.songs_in_songlists ADD CONSTRAINT fk_songs_in_songlists FOREIGN KEY ( songlist_id ) REFERENCES tjadb.songlists( id ) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE tjadb.songs_in_songlists ADD CONSTRAINT fk_songs_in_songlists_songs FOREIGN KEY ( song_id ) REFERENCES tjadb.songs( id ) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE tjadb.sources ADD CONSTRAINT fk_sources_genres FOREIGN KEY ( genre_id ) REFERENCES tjadb.genres( id ) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE tjadb.tags_per_song ADD CONSTRAINT fk_tags_per_song_songs FOREIGN KEY ( song_id ) REFERENCES tjadb.songs( id );

ALTER TABLE tjadb.tags_per_song ADD CONSTRAINT fk_tags_per_song_song_tags FOREIGN KEY ( tag_id ) REFERENCES tjadb.song_tags( id );

ALTER TABLE tjadb.users ADD CONSTRAINT fk_users_difficulties FOREIGN KEY ( preferred_difficulty_id ) REFERENCES tjadb.difficulties( id ) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE tjadb.users ADD CONSTRAINT fk_users_languages FOREIGN KEY ( preferred_language_id ) REFERENCES tjadb.languages( id ) ON DELETE RESTRICT ON UPDATE RESTRICT;


SELECT pg_catalog.setval('tjadb.songs_id_seq', 9999, true);

INSERT INTO tjadb.difficulties(name_jp, name_en) VALUES ('かんたん', 'Easy');
INSERT INTO tjadb.difficulties(name_jp, name_en) VALUES ('ふつう', 'Normal');
INSERT INTO tjadb.difficulties(name_jp, name_en) VALUES ('むずかしい', 'Hard');
INSERT INTO tjadb.difficulties(name_jp, name_en) VALUES ('おに', 'Oni');
INSERT INTO tjadb.difficulties(name_jp, name_en) VALUES ('うら', 'Ura');

INSERT INTO tjadb.genres(name_en, name_jp, tja_genre)
  VALUES ('Pop', 'Pop', 'J-Pop');
INSERT INTO tjadb.genres(name_en, name_jp, tja_genre)
  VALUES ('Anime', 'アニメ', 'アニメ');
INSERT INTO tjadb.genres(name_en, name_jp, tja_genre)
  VALUES ('Vocaloid', 'ボーカロイド曲', 'ボーカロイド');
INSERT INTO tjadb.genres(name_en, name_jp, tja_genre)
  VALUES ('Children & Folk', 'どうよう', 'どうよう');
INSERT INTO tjadb.genres(name_en, name_jp, tja_genre)
  VALUES ('Variety', 'バラエティ', 'バラエティ');
INSERT INTO tjadb.genres(name_en, name_jp, tja_genre)
  VALUES ('Classical', 'クラシック', 'クラシック');
INSERT INTO tjadb.genres(name_en, name_jp, tja_genre)
  VALUES ('Game Music','ゲームミュージック', 'ゲームミュージック');
INSERT INTO tjadb.genres(name_en, name_jp, tja_genre)
  VALUES ('Namco Original', 'ナムコオリジナル', 'ナムコオリジナル');

INSERT INTO tjadb.languages(name_orig, name_en) VALUES ('English', 'English');
INSERT INTO tjadb.languages(name_orig, name_en) VALUES ('日本語', 'Japanese');
INSERT INTO tjadb.languages(name_orig, name_en) VALUES ('Español', 'Spanish');

INSERT INTO tjadb.song_states(name) VALUES ('Ongoing');
INSERT INTO tjadb.song_states(name) VALUES ('On Hold');
INSERT INTO tjadb.song_states(name) VALUES ('Canceled');
INSERT INTO tjadb.song_states(name) VALUES ('Peer Review');
INSERT INTO tjadb.song_states(name) VALUES ('Metadata Review');
INSERT INTO tjadb.song_states(name) VALUES ('Approved');
INSERT INTO tjadb.song_states(name) VALUES ('Rejected');
