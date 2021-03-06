CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    description TEXT,
    filename TEXT UNIQUE,
    img_src TEXT UNIQUE,
    accepted BOOLEAN CHECK (accepted IN (0, 1)),
    FOREIGN KEY (author_id) REFERENCES user (id) ON DELETE CASCADE,
    CHECK (filename IS NOT NULL OR img_src IS NOT NULL OR description IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    author_id INTEGER NOT NULL,
    image_id INTEGER NOT NULL,
    body TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES user (id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES images (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ext_websites (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    website_user_id TEXT NOT NULL UNIQUE,
    website_url TEXT NOT NULL UNIQUE,
    image_class TEXT NOT NULL,
    FOREIGN KEY (website_user_id) REFERENCES user (id) ON DELETE CASCADE
);