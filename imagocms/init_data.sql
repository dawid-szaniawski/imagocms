INSERT OR IGNORE INTO user (username, password) VALUES
    ('kwejk', 'pbkdf2:sha256:260000$PO8kmstQDHw19pyO$7fa4b62d9632255f2d8b586290e429fa0fb18604392e07f0f789bbbca1d9a5c5'),
    ('jbzd', 'pbkdf2:sha256:260000$PO8kmstQDHw19pyO$7fa4b62d9632255f2d8b586290e429fa0fb18604392e07f0f789bbbca1d9a5c5'),
    ('Dawid', 'pbkdf2:sha256:260000$PO8kmstQDHw19pyO$7fa4b62d9632255f2d8b586290e429fa0fb18604392e07f0f789bbbca1d9a5c5');

INSERT OR IGNORE INTO ext_websites (website_user_id, website_url, image_class, pages_to_scan) VALUES
    (1, 'https://kwejk.pl/', 'full-image', 1),
    (2, 'https://jbzd.com.pl/', 'article-image', 2);
