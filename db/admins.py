from db import cur, conn


def check_admin(id):
    cur.execute('SELECT * FROM admins WHERE tg_id = %s', (id,))
    return not not cur.fetchone()

def add_admin(id, username, time):
    cur.execute('INSERT INTO admins VALUES(%s, %s, %s)', (id, username, time))
    conn.commit()
    