from datetime import datetime

from db import cur


def get_all_ids_names():
    cur.execute('SELECT id, name FROM houses')
    return cur.fetchall()

def get_by_id(id: int):
    cur.execute('SELECT * FROM houses WHERE id = %s', (id,))
    res = cur.fetchone()
    cur.execute('SELECT day FROM booking WHERE house_id = %s and day > %s', (id, datetime.now()))
    res['booking'] = tuple(map(lambda x: x.get('day'), cur.fetchall()))
    return res
