import psycopg2.extras

from configs import DB_NAME, DB_USER, DB_PASSWORD

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host='localhost', port='5432')
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

def create_tables():
    cur.execute('''
    CREATE TABLE IF NOT EXISTS
    houses (
    id SMALLSERIAL PRIMARY KEY,
    name VARCHAR(63) NOT NULL,
    description VARCHAR(511) NOT NULL,
    price VARCHAR(127)
    );
    CREATE TABLE IF NOT EXISTS
    booking (
        house_id SMALLINT NOT NULL,
        day DATE NOT NULL,
        CONSTRAINT fk_houses
            FOREIGN KEY (house_id)
            REFERENCES houses(id)
    );
    CREATE TABLE IF NOT EXISTS 
    admins (
        tg_id INTEGER PRIMARY KEY,
        username VARCHAR(255),
        becoming_date DATE
    )
    ''')
    conn.commit()

import db.houses as houses
import db.booking as booking
import db.admins as admins