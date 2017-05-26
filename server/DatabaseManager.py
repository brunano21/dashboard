import sqlite3
# -*- coding: utf-8 -*-
"""
    DatabaseManager.py
    ~~~~~~
    Simple class that holds and manages the connection and
    interaction with the database. It exposes a bunch of methods
    specific for each statistics.
"""


class DatabaseManager(object):

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.conn.row_factory = self.dict_factory
        # self.conn.execute('''DROP TABLE downloads''')
        # self.conn.execute('''CREATE TABLE downloads
        #           (lat real, lng real, app_id text,
        #           loc_short text, loc_long text, downloaded_at real)''')
        # self.conn.commit()
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def dict_factory(self, cursor, row):
        """ Returns a dictionary, given a query's result list. """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def get_data_by_country(self):
        q = """SELECT loc_long, loc_short, COUNT (*) AS 'tot'
            FROM downloads
            GROUP BY loc_short"""
        results = self.cur.execute(q).fetchall()
        return results

    def get_data_by_time(self):
        q = """SELECT
            CASE
            WHEN (downloaded_at % 86400000) < (86400000/4) THEN '00am-08am'
            WHEN (downloaded_at % 86400000) < (86400000*2/4) THEN '08am-12pm'
            WHEN (downloaded_at % 86400000) < (86400000*3/4) THEN '12pm-18pm'
            ELSE '18pm-24pm'END
            `AmPmTime`,
            COUNT(*) as 'tot'
            FROM downloads
            Group by `AmPmTime`"""
        results = self.cur.execute(q).fetchall()
        return results

    def get_all_downloads(self):
        q = "SELECT * FROM downloads"
        results = self.cur.execute(q).fetchall()
        return results

    def get_history(self):
        q = """SELECT strftime("%Y-%m-%d", downloaded_at/1000, "unixepoch") as "date",
            downloaded_at,
            COUNT(*) AS `num`
            FROM downloads
            GROUP BY `date`"""
        results = self.cur.execute(q).fetchall()
        return results

    def save_download(
            self, lat, lng, app_id,
            short_name, long_name, downloaded_at):
        q = "INSERT INTO downloads VALUES (?, ?, ?, ?, ?, ?)"
        self.cur.execute(
            q,
            (lat, lng, app_id, short_name, long_name, downloaded_at))
        self.conn.commit()
