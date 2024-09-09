import psycopg2
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")


def connect(number):
    conn = psycopg2.connect(database=PG_DB, user=PG_USER, password=PG_PASSWORD, host="db")
    cur = conn.cursor()
    cur.execute(f"""SELECT *
    FROM films2
    WHERE place = %s""", (number,))
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res


def connect_all():
    conn = psycopg2.connect(database=PG_DB, user=PG_USER, password=PG_PASSWORD, host="db")
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM films2""")
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res


def call_names(info):
    parameter = info['name']
    conn = psycopg2.connect(database=PG_DB, user=PG_USER, password=PG_PASSWORD, host="db")
    cur = conn.cursor()
    cur.execute(f"""SELECT COUNT(name)
FROM films2
WHERE name = %s""", (parameter,))
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res[0][0]


def call_authority(info):
    parameter = info['name']
    conn = psycopg2.connect(database=PG_DB, user=PG_USER, password=PG_PASSWORD, host="db")
    cur = conn.cursor()
    cur.execute(f"""SELECT authority
            FROM films2
            WHERE name = %s""", (parameter,))
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res[0][0]


def call_count_films():
    conn = psycopg2.connect(database=PG_DB, user=PG_USER, password=PG_PASSWORD, host="db")
    cur = conn.cursor()
    cur.execute(f"""SELECT MAX(place)
FROM films2;""")
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res[0][0]


def write_full_name(user_id):
    conn = psycopg2.connect(database=PG_DB, user=PG_USER, password=PG_PASSWORD, host="db")
    cur = conn.cursor()
    cur.execute(f"""INSERT INTO users_table (user_id, datetime)
SELECT '{user_id}', '{datetime.datetime.now()}'
WHERE NOT EXISTS (
    SELECT 1 FROM users_table WHERE user_id = '{user_id}'
    )""")
    conn.commit()
    cur.execute(f"""
UPDATE users_table SET datetime = '{datetime.datetime.now()}'
WHERE user_id = '{user_id}'""")
    conn.commit()
    cur.close()
    conn.close()
