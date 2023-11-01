# FRONTEND AUTH
select_id_password_by_name = "SELECT id, password FROM imago_user WHERE username = %s;"
insert_user = "INSERT INTO imago_user (username, password, email) VALUES (%s, %s, %s);"
select_all_user_data_by_id = "SELECT * FROM imago_user WHERE id = %s;"

# API AUTH
select_user_by_id_name_email = (
    "SELECT username FROM imago_user WHERE id = %s AND username = %s AND email = %s;"
)
select_all_user_data_by_name = "SELECT * FROM imago_user WHERE username = %s;"

# GET IMAGES
# HOMEPAGE
image_data_query = (
    "SELECT i.id, i.title, i.description, i.img_src, i.filename, i.created, i.source,"
    " u.username, COUNT(c.id) AS comments"
    " FROM imago_images i"
    " LEFT JOIN imago_user u ON i.author_id = u.id"
    " LEFT JOIN imago_comments c ON i.id = c.image_id"
)
group_by_image = (
    "GROUP BY i.id, i.title, i.description, i.img_src, i.filename, i.created,"
    " i.source, u.username"
)
order_by_limit_offset = "ORDER BY i.created DESC LIMIT 11 OFFSET %s;"
grp_by_ord_by_limit_offset = group_by_image + " " + order_by_limit_offset
select_images_with_offset = image_data_query + " " + grp_by_ord_by_limit_offset
select_author_images_with_offset = (
    image_data_query + " WHERE u.username = %s " + grp_by_ord_by_limit_offset
)
select_single_image = (
    image_data_query + " WHERE i.id = %s " + group_by_image + " LIMIT 1;"
)
select_single_image_data = (
    "SELECT i.title, i.description, i.img_src, i.filename, i.created AS img_created,"
    " img_u.username AS img_author, c.body, c.created AS c_created,"
    " u.username AS c_author, counter.c_count"
    " FROM imago_images i"
    " LEFT JOIN imago_user img_u ON i.author_id = img_u.id"
    " LEFT JOIN imago_comments c ON i.id = c.image_id"
    " LEFT JOIN imago_user u ON c.author_id = u.id"
    " CROSS JOIN "
    "(SELECT COUNT(*) AS c_count FROM imago_comments c2 WHERE c2.image_id = %s) counter"
    " WHERE i.id = %s ORDER BY c_created DESC;"
)
select_images_by_author_id = (
    "SELECT * FROM imago_images i WHERE i.author_id = %s"
    " ORDER BY i.created DESC LIMIT %s OFFSET %s;"
)

# API
select_last_img_scr_from_author = (
    "SELECT img_src FROM imago_images WHERE author_id = %s"
    " ORDER BY created DESC LIMIT %s;"
)

# INSERT IMAGES
insert_image = (
    "INSERT INTO imago_images"
    " (author_id, title, description, filename, img_src, source, accepted)"
    " VALUES (%s, %s, %s, %s, %s, %s, %s);"
)

# COMMENTS
# GET COMMENTS
select_comments_on_img = (
    "SELECT ic.body, ic.created, iu.username"
    " FROM imago_comments ic"
    " LEFT JOIN imago_user iu ON ic.author_id = iu.id"
    " WHERE ic.image_id = %s ORDER BY ic.created DESC;"
)

# INSERT COMMENTS
insert_comment = (
    "INSERT INTO imago_comments (author_id, image_id, body) VALUES (%s, %s, %s)"
)


# UTILS
def do_nothing_on_conflict(query: str) -> str:
    return query[:-1] + " ON CONFLICT DO NOTHING;"
