#!/usr/bin/env python3

"""
Simple interface to a minimalistic data store.

Data is stored in a table in SQLite3.
"""

import sqlite3
from pprint import pprint

DEBUGIT = False  # True # False

# --------- debug ------------------------------------------------------------


def mydebug(*data):
    """Print extra info when DEBG is enabled."""
    if DEBUGIT:
        pprint(data)
    return True

# --------- database interactions --------------------------------------------


def dict_factory(cursor, row) -> dict:
    """Map function. Make result rows accessible via column name."""
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data


class DataDB():
    """Database class to contain all the necessary parameters and functions."""

    def __init__(self, uri=None, table=None):
        """Update internal class default values."""
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
        row = cur.execute(query).fetchone()
        if not row:
            query = 'INSERT INTO {} (id, name, value) '.format(self._table) + \
                      'VALUES (?,?,?)'
            cur.execute(query, [0, 'dummy name', 'dummy value'])
        conn.commit()
        conn.close()
        return True

    def data_get_byid(self, key_id=None) -> dict:
        """Fetch a specific row or all rows from the database."""
        conn = sqlite3.connect(self._db, uri=True)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        if key_id is None:
            query = 'SELECT * FROM {};'.format(self._table)
            data = cur.execute(query).fetchall()
        else:
            query = 'SELECT * FROM {} WHERE id=?;'.format(self._table)
            data = cur.execute(query, [key_id, ]).fetchone()
        conn.close()
        mydebug("data", data)
        return data

    def data_get_byname(self, name=None) -> dict:
        """Fetch a specific row or all rows from the database."""
        if name is None:
            mydebug("No name supplied to data_get_byname")
            return None
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
        """Insert a data row ."""
        conn = sqlite3.connect(self._db, uri=True)
        cur = conn.cursor()
        query = 'INSERT INTO {} (name, value) VALUES (?,?)'.format(self._table)
        param = [data['name'], data['value']]
        cur.execute(query, param)
        conn.commit()
        conn.close()
        return data

    def data_update(self, data) -> dict:
        """Update a data row, use id provided in data set."""
        conn = sqlite3.connect(self._db, uri=True)
        cur = conn.cursor()
        query = 'UPDATE {} SET name=?, value=? WHERE id=?'.format(self._table)
        param = [data['name'], data['value'], data['id']]
        cur.execute(query, param)
        conn.commit()
        conn.close()
        return data

    def data_delete(self, key_id) -> bool:
        """Delete data row indicated by key_id."""
        if key_id is None:
            return False
        conn = sqlite3.connect(self._db, uri=True)
        cur = conn.cursor()
        query = 'DELETE FROM {} WHERE id=?'.format(self._table)
        cur.execute(query, [key_id, ])
        conn.commit()
        conn.close()
        return True

# --------- main -------------------------------------------------------------


if __name__ == '__main__':
    y = DataDB('file:app.db', table='resource')
    mydebug(y.data_get_byid())
