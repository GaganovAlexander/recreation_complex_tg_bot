from db import cur, conn


def check_admin(id):
    cur.execute('SELECT * FROM admins WHERE tg_id = %s', (id,))
    return not not cur.fetchone()

def add_admin(id):
    cur.execute('INSERT INTO admins VALUES(%s)', (id,))
    conn.commit()
    