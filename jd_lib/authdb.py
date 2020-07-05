#!/usr/bin/env python3

"""
Simple interface to a minimalistic authentication database store.

Data is stored in a table in SQLite3.
"""

import sqlite3
import datetime
from pprint import pprint
from werkzeug.security import generate_password_hash

DEBUGIT = False  # True # False
TOKENKEY = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTU5MzM0MzQxMSwiZXhwIjoxNTkzMzQ3MDEx9Q'

# --------- debug ------------------------------------------------------------


def mydebug(*data):
    """Print information if global debug flag is set."""
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


class AuthDB():
    """Extremely simple authentication DB object class."""

    def __init__(self, uri=None):
        """Update internal class default values if needed."""
        self._db = uri or 'app.db'
        self._table = "auth"
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
        """Create table (if needed) and add at least one 'admin' user."""
        conn = sqlite3.connect(self._db, uri=True)
        cur = conn.cursor()
        query = '''CREATE TABLE IF NOT EXISTS auth (
                    username TEXT PRIMARY KEY NOT NULL,
                    password TEXT,
                    token TEXT,
                    token_ts timestamp
                );'''
        cur.execute(query)
        query = 'SELECT username FROM auth;'
        user = cur.execute(query).fetchone()
        if not user:
            default = '''INSERT INTO auth (username,password,token,token_ts)
                            VALUES (?,?,?,?);'''
            param = ["admin",
                     generate_password_hash("password"),
                     str(TOKENKEY),
                     datetime.datetime.now()
                     ]
            cur.execute(default, param)
        conn.commit()
        conn.close()
        return True

    def user_list(self) -> list:
        """Get full list of user names from DB."""
        conn = sqlite3.connect(self._db, uri=True)
        cur = conn.cursor()
        query = 'SELECT DISTINCT username FROM auth;'
        users = cur.execute(query).fetchall()[0]
        conn.close()
        # mydebug("users",users)
        if users:
            return users
        return None

    def user_get(self, username) -> dict:
        """Fetch credentals for given user from DB."""
        conn = sqlite3.connect(self._db, uri=True)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        query = 'SELECT * FROM auth WHERE username=?;'
        authdata = cur.execute(query, [username, ]).fetchone()
        conn.close()
        mydebug("authdata", authdata)
        return authdata

    def token_get(self, token) -> dict:
        """Fetch user info for given token from DB."""
        conn = sqlite3.connect(self._db, uri=True)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        # we don't check the token timestamp
        query = 'SELECT * FROM auth WHERE token=?;'
        authdata = cur.execute(query, [token, ]).fetchone()
        conn.close()
        mydebug("authdata", authdata)
        return authdata


# --------- main -------------------------------------------------------------


if __name__ == '__main__':
    x = AuthDB('file:app.db')
    mydebug(x.user_list())
    mydebug(x.user_get('admin'))
