from db import cur


def get_all_ids_names():
    cur.execute('SELECT id, name FROM houses')
    return cur.fetchall()

def get_by_id(id: int):
    cur.execute('SELECT * FROM houses WHERE id = %s', (id,))
    return cur.fetchone()