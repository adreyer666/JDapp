#!/usr/bin/env python3

"""
Simple interface to a minimalistic Key/Value store.

Data is stored in a table in SQLite3.
"""

import sqlite3
import datetime

# --------- database interactions --------------------------------------------


def dict_factory(cursor, row) -> dict:
    """Map function. Make result rows accessible via column name."""
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data


class KeyValueDB():
    """Database class to contain all the necessary parameters and functions."""

    def __init__(self, table=None, uri=None, verbose=1):
        """Update internal class default values."""
        if verbose:
            self._verbose = verbose
        else:
            self._verbose = 0
        self._db = uri or 'app.db'
        self._table = table or 'kv'
        try:
            conn = sqlite3.connect(self._db, uri=True, timeout=1000)
            if self._verbose:
                print("SQLite version", sqlite3.version)
        except sqlite3.OperationalError as err:
            if self._verbose:
                print('Database does not exist, creating it.')
            if self._verbose > 1:
                print(err)
        cur = conn.cursor()
        try:
            query = 'SELECT key FROM {} LIMIT 1;'.format(self._table)
            entry = cur.execute(query).fetchone()
            if self._verbose > 1:
                print(entry)
        except sqlite3.OperationalError as err:
            if self._verbose:
                print('Table does not exist, creating it.')
                if self._verbose > 1:
                    print(err)
            self._create()
        if conn:
            conn.close()

    def _create(self) -> bool:
        conn = sqlite3.connect(self._db, uri=True)
        cur = conn.cursor()
        query = '''CREATE TABLE IF NOT EXISTS {} (
                    key   TEXT PRIMARY KEY NOT NULL,
                    value TEXT,
                    ts    timestamp
                );'''.format(self._table)
        cur.execute(query)
        conn.commit()
        conn.close()
        return True

    def get(self, key=None) -> dict:
        """Fetch a specific row from the database or a list of all keys."""
        conn = sqlite3.connect(self._db, uri=True)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        if key is None:
            # Query for list of keys.
            query = 'SELECT key FROM {};'.format(self._table)
            cur.execute(query)
            entry = [r['key'] for r in cur.fetchall()]
            conn.close()
            if self._verbose > 1:
                print("entry", entry)
            return entry
        # Query full entry matching key.
        query = 'SELECT value FROM {} WHERE key=?;'.format(self._table)
        entry = cur.execute(query, [key, ]).fetchone()
        conn.close()
        if self._verbose > 1:
            print("entry", entry)
        return entry

    def set(self, key=None, value=None) -> str:
        """Insert or update a specific row defined by key."""
        if (key is None) or (value is None):
            return None
        conn = sqlite3.connect(self._db, uri=True)
        cur = conn.cursor()
        query = 'SELECT key FROM {} WHERE key=?;'.format(self._table)
        entry = cur.execute(query, [key, ]).fetchone()
        if self._verbose > 2:
            print("ENTRY: ", entry)
        if not entry:
            query = 'INSERT INTO {} '.format(self._table) \
                    + '(value,ts,key) VALUES (?,?,?);'
        else:
            query = 'UPDATE {} '.format(self._table) \
                    + 'SET value=?, ts=? WHERE key=?;'
        param = [value, datetime.datetime.now(), key]
        cur.execute(query, param)
        conn.commit()
        conn.close()
        return key


# --------- main -------------------------------------------------------------

if __name__ == '__main__':
    x = KeyValueDB(uri='file:app.db', table='kv')
    print("getall:  ", x.get())
    print("add 1:   ", x.set('0-0-0-0', 'a-b-c-d'))
    print("add 2:   ", x.set('0-0-1-0', 'a-b-d-c'))
    print("add 3:   ", x.set('0-1-0-0', 'a-d-c-b'))
    print('---')
    print("get inv: ", x.get('0-1-0-1'))
    print("get val: ", x.get('0-1-0-0'))
    print("upd 3:   ", x.set('0-1-0-0', 'e-e-e-e'))
    print("getall:  ", x.get())
