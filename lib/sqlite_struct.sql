PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Genres
(ID        INTEGER  PRIMARY KEY  AUTOINCREMENT,
 Title_JP  TEXT     NOT NULL,
 Title_EN  TEXT     NOT NULL,
 Genre     TEXT     NOT NULL);

CREATE TABLE IF NOT EXISTS Charters
(ID     INTEGER  PRIMARY KEY  AUTOINCREMENT,
 Name   TEXT     NOT NULL,
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
 Path           TEXT     NOT NULL,
 MD5            TEXT     NOT NULL,
 Added          TEXT     NOT NULL,
 Updated        TEXT     NOT NULL,
 FOREIGN KEY(Genre_ID)   REFERENCES "Genres" (ID),
 FOREIGN KEY(Charter_ID) REFERENCES "Charters" (ID));
