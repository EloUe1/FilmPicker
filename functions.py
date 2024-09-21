import psycopg2
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")


class DBConnect:
    def __init__(self, PG_DB, PG_USER, PG_PASSWORD):
        self.conn = psycopg2.connect(database=PG_DB, user=PG_USER, password=PG_PASSWORD, host='db')

    def call_film(self, place):
        cur = self.conn.cursor()
        cur.execute(f"""SELECT *
        FROM films2
        WHERE place = %s""", (place,))
        res = cur.fetchall()
        cur.close()
        return res

    def call_all_films(self):
        cur = self.conn.cursor()
        cur.execute(f"""SELECT * FROM films2""")
        res = cur.fetchall()
        cur.close()
        return res

    def call_names(self, info):
        cur = self.conn.cursor()
        parameter = info['name']
        cur.execute(f"""SELECT COUNT(name)
    FROM films2
    WHERE name = %s""", (parameter,))
        res = cur.fetchall()
        cur.close()
        return res[0][0]

    def call_authority(self, info):
        cur = self.conn.cursor()
        parameter = info['name']
        cur.execute(f"""SELECT authority
                FROM films2
                WHERE name = %s""", (parameter,))
        res = cur.fetchall()
        cur.close()
        return res[0][0]

    def call_count_films(self):
        cur = self.conn.cursor()
        cur.execute(f"""SELECT MAX(place)
    FROM films2;""")
        res = cur.fetchall()
        cur.close()
        return res[0][0]

    def write_full_name(self, tg_id):
        cur = self.conn.cursor()
        cur.execute(f"""INSERT INTO users_table (tg_id, datetime)
    SELECT '{tg_id}', '{datetime.datetime.now()}'
    WHERE NOT EXISTS (
        SELECT 1 FROM users_table WHERE tg_id = '{tg_id}'
        )""")
        self.conn.commit()
        cur.execute(f"""
    UPDATE users_table SET datetime = '{datetime.datetime.now()}'
    WHERE tg_id = '{tg_id}'""")
        self.conn.commit()
        cur.close()

    def write_film_position(self, place, tg_id):
        cur = self.conn.cursor()
        cur.execute(f"""INSERT INTO position (tg_id, place)
    SELECT '{tg_id}', '{place}'
    WHERE NOT EXISTS (
    SELECT 1 FROM position WHERE tg_id = '{tg_id}');""")
        self.conn.commit()
        cur.execute(f"""UPDATE position SET place = '{place}'
WHERE tg_id = '{tg_id}';""")
        cur.close()

    def call_film_by_id(self, tg_id):
        cur = self.conn.cursor()
        cur.execute(f"""SELECT *
FROM films2
JOIN position ON films2.place=position.place
WHERE position.tg_id='{tg_id}';""")
        res = cur.fetchall()
        cur.close()
        return res

    def call_film_id(self, tg_id):
        cur = self.conn.cursor()
        cur.execute(f"""SELECT place FROM position WHERE tg_id = '{tg_id}';""")
        res = cur.fetchall()
        cur.close()
        return res[0][0]


DB = DBConnect(PG_DB=PG_DB, PG_USER=PG_USER, PG_PASSWORD=PG_PASSWORD)