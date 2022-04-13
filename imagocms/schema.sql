DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS images;
DROP TABLE IF EXISTS comments;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE,
    moderator BOOLEAN CHECK (moderator IN (0, 1)),
    superuser BOOLEAN CHECK (superuser IN (0, 1))
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    description TEXT,
    filename TEXT UNIQUE,
    img_src TEXT UNIQUE,
    accepted BOOLEAN CHECK (accepted IN (0, 1)),
    FOREIGN KEY (author_id) REFERENCES user (id) ON DELETE CASCADE,
    CHECK (filename is not null or img_src is not null)
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    image_id INTEGER NOT NULL,
    body TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES user (id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES images (id) ON DELETE CASCADE
);