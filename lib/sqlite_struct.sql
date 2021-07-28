PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Genres
(ID        INTEGER  PRIMARY KEY  AUTOINCREMENT,
 Title_JP  TEXT     NOT NULL,
 Title_EN  TEXT     NOT NULL,
 Genre     TEXT     NOT NULL  UNIQUE);

CREATE TABLE IF NOT EXISTS Charters
(ID     INTEGER  PRIMARY KEY  AUTOINCREMENT,
 Name   TEXT     NOT NULL  UNIQUE,
 Image  BLOB,
 About  TEXT,
 Staff  BOOL     DEFAULT 0);

CREATE TABLE IF NOT EXISTS Songs
(ID             INTEGER  PRIMARY KEY  AUTOINCREMENT,
 Title_Orig     TEXT     NOT NULL,
 Title_Eng      TEXT     NOT NULL,
 Subtitle_Orig  TEXT     NOT NULL,
 Subtitle_Eng   TEXT     NOT NULL,
 Artist_Orig    TEXT     NOT NULL,
 Artist_Eng     TEXT     NOT NULL,
 Source_Orig    TEXT,
 Source_Eng     TEXT,
 BPM            REAL     NOT NULL,
 Genre_ID       INTEGER  NOT NULL,
 Charter_ID     INTEGER  NOT NULL,
 D_Kantan       INTEGER,
 D_Futsuu       INTEGER,
 D_Muzukashii   INTEGER,
 D_Oni          INTEGER,
 D_Ura          INTEGER,
 Vetted         BOOL     DEFAULT 0,
 Comments       TEXT,
 Video_Link     TEXT,
 Path           TEXT     NOT NULL  UNIQUE,
 MD5_Orig       TEXT     NOT NULL  UNIQUE,
 MD5_Eng        TEXT     NOT NULL  UNIQUE,
 Added          TEXT     NOT NULL,
 Updated        TEXT     NOT NULL,
 FOREIGN KEY(Genre_ID)   REFERENCES "Genres" (ID),
 FOREIGN KEY(Charter_ID) REFERENCES "Charters" (ID));

UPDATE SQLITE_SEQUENCE SET seq = 9999 WHERE name = 'Songs';
INSERT INTO SQLITE_SEQUENCE (name, seq) SELECT 'Songs', 9999 WHERE NOT EXISTS
    (SELECT changes() AS change FROM sqlite_sequence WHERE change <> 0);
COMMIT;

INSERT OR IGNORE INTO Genres(Title_JP, Title_EN, Genre)
  VALUES('J-Pop', 'J-Pop', 'J-Pop') ON CONFLICT DO NOTHING;
INSERT OR IGNORE INTO Genres(Title_JP, Title_EN, Genre)
  VALUES('アニメ', 'Anime', 'アニメ') ON CONFLICT DO NOTHING;
INSERT OR IGNORE INTO Genres(Title_JP, Title_EN, Genre)
  VALUES('ボーカロイド曲', 'Vocaloid', 'ボーカロイド') ON CONFLICT DO NOTHING;
INSERT OR IGNORE INTO Genres(Title_JP, Title_EN, Genre)
  VALUES('どうよう', 'Children & Folk', 'どうよう') ON CONFLICT DO NOTHING;
INSERT OR IGNORE INTO Genres(Title_JP, Title_EN, Genre)
  VALUES('バラエティ', 'Variety', 'バラエティ') ON CONFLICT DO NOTHING;
INSERT OR IGNORE INTO Genres(Title_JP, Title_EN, Genre)
  VALUES('クラシック', 'Classical', 'クラシック') ON CONFLICT DO NOTHING;
INSERT OR IGNORE INTO Genres(Title_JP, Title_EN, Genre)
  VALUES('ゲームミュージック', 'Game Music', 'ゲームミュージック') ON CONFLICT DO NOTHING;
INSERT OR IGNORE INTO Genres(Title_JP, Title_EN, Genre)
  VALUES('ナムコオリジナル', 'Namco Original', 'ナムコオリジナル') ON CONFLICT DO NOTHING;
