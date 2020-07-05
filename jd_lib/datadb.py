#!/usr/bin/env python3

import sqlite3
from pprint import pprint

DEBUGIT = False  # True # False

# --------- debug ------------------------------------------------------------


def mydebug(*data):
    if DEBUGIT:
        pprint(data)
    return True

# --------- database interactions --------------------------------------------


def dict_factory(cursor, row) -> dict:
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DataDB(object):
    _db = None
    _table = None

    def __init__(self, uri=None, table=None):
        self._db = uri or 'app.db'
        self._table = table or 'resource'
        try:
            conn = sqlite3.connect(self._db, uri=True, timeout=1000)
            mydebug("SQLite version", sqlite3.version)
        except sqlite3.OperationalError as err:
            print('Database does not exist, creating it.')
            mydebug(err)
        finally:
            if conn:
                conn.close()
        self._create()

    def _create(self) -> bool:
        conn = sqlite3.connect(self._db, uri=True)
        cur = conn.cursor()
        query = '''CREATE TABLE IF NOT EXISTS {} (
                    id      INTEGER PRIMARY KEY AUTOINCREMENT,
                    name    TEXT NOT NULL,
                    value   TEXT NOT NULL
                );'''.format(self._table)
        cur.execute(query)
        query = 'SELECT id FROM {};'.format(self._table)
        id = cur.execute(query).fetchone()
        if not id:
            query = 'INSERT INTO {} (id, name, value) '.format(self._table) + \
                      'VALUES (?,?,?)'
            cur.execute(query, [0, 'dummy name', 'dummy value'])
        conn.commit()
        conn.close()
        return True

    def data_get_byid(self, id=None) -> dict:
        conn = sqlite3.connect(self._db, uri=True)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        if id is None:
            query = 'SELECT * FROM {};'.format(self._table)
            data = cur.execute(query).fetchall()
        else:
            query = 'SELECT * FROM {} WHERE id=?;'.format(self._table)
            data = cur.execute(query, [id, ]).fetchone()
        conn.close()
        mydebug("data", data)
        return data

    def data_get_byname(self, name) -> dict:
        conn = sqlite3.connect(self._db, uri=True)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        query = 'SELECT * FROM {} WHERE name=?;'.format(self._table)
        data = cur.execute(query, [name, ]).fetchone()
        conn.close()
        mydebug("data", data)
        if data and 'id' in data:
            return data['id']
        return None

    def data_add(self, data) -> dict:
        conn = sqlite3.connect(self._db, uri=True)
        cur = conn.cursor()
        query = 'INSERT INTO {} (name, value) VALUES (?,?)'.format(self._table)
        param = [data['name'], data['value']]
        cur.execute(query, param)
        conn.commit()
        conn.close()
        return data

    def data_update(self, data) -> dict:
        conn = sqlite3.connect(self._db, uri=True)
        cur = conn.cursor()
        query = 'UPDATE {} SET name=?, value=? WHERE id=?'.format(self._table)
        param = [data['name'], data['value'], data['id']]
        cur.execute(query, param)
        conn.commit()
        conn.close()
        return data

    def data_delete(self, id) -> bool:
        conn = sqlite3.connect(self._db, uri=True)
        cur = conn.cursor()
        query = 'DELETE FROM {} WHERE id=?'.format(self._table)
        cur.execute(query, [id, ])
        conn.commit()
        conn.close()
        return True

# --------- main -------------------------------------------------------------


if __name__ == '__main__':
    y = DataDB('file:app.db', table='resource')
    mydebug(y.data_get_byid())
