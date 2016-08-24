import sqlite3

conn = sqlite3.connect("series.sqlite")
c = conn.cursor()


def migrate(req):
    c.execute(req)
    conn.commit()

migrate("""CREATE TABLE series(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT,
    api_id INTEGER,
    season INTEGER,
    episode INTEGER
    )""")


