import sqlite3
database_name = "database.db"


def add_new_user(user_id):
    user_id = "id" + str(user_id)
    conn = sqlite3.connect(database_name)

    sql_create_table = """ CREATE TABLE IF NOT EXISTS {0} (
                                            meme_path text,
                                            key_words text
                                        ); """.format(user_id)
    c = conn.cursor()
    c.execute(sql_create_table)


def add_new_meme(user_id, meme_path, key_words):
    user_id = "id" + str(user_id)
    conn = sqlite3.connect(database_name)

    sql = ''' INSERT INTO {0}(meme_path,key_words)
                  VALUES(?,?) '''.format(user_id)
    cur = conn.cursor()
    cur.execute(sql, (meme_path, key_words))
    conn.commit()


def get_user_memes(user_id):
    user_id = "id" + str(user_id)
    conn = sqlite3.connect(database_name)

    cur = conn.cursor()
    cur.execute("SELECT * FROM {0}".format(user_id))

    rows = cur.fetchall()
    paths = []
    key_words = []
    for row in rows:
        paths.append(row[0])
        key_words.append(row[1])

    return paths, key_words

