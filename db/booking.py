from datetime import datetime

from db import cur, conn


def add_book(house_id, day):
    try:
        cur.execute('INSERT INTO booking VALUES(%s, %s)', (house_id, day))
    except:
        conn.rollback()
        return False
    conn.commit()
    return True

def remove_book(house_id, day):
    cur.execute('DELETE FROM booking WHERE house_id = %s AND day = %s', (house_id, day))
    conn.commit()

def check_day(day):
    cur.execute('SELECT * FROM booking WHERE day = %s', (day,))
    return not cur.fetchone()


def get_by_id():
    cur.execute('SELECT day FROM booking WHERE house_id = %s and day > %s', (id, datetime.now()))
    return tuple(map(lambda x: x.get('day'), cur.fetchall()))