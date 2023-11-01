CREATE TABLE IF NOT EXISTS imago_user (
    id INT GENERATED ALWAYS AS IDENTITY UNIQUE,
    username VARCHAR(32) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS imago_images (
    id INT GENERATED ALWAYS AS IDENTITY UNIQUE,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    description TEXT,
    filename TEXT UNIQUE,
    img_src TEXT UNIQUE,
    source TEXT,
    accepted BOOLEAN,
    FOREIGN KEY (author_id) REFERENCES imago_user (id) ON DELETE CASCADE,
    CHECK (filename IS NOT NULL OR img_src IS NOT NULL OR description IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS imago_comments (
    id INT GENERATED ALWAYS AS IDENTITY UNIQUE,
    author_id INTEGER NOT NULL,
    image_id INTEGER NOT NULL,
    body TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES imago_user (id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES imago_images (id) ON DELETE CASCADE
);