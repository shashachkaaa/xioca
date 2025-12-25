# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import sqlite3, threading, json

connect = sqlite3.connect("db.db")
cursor = connect.cursor()

class Database:
    def get(self, module: str, variable: str, default=None):
        """Get value from database"""
        raise NotImplementedError

    def set(self, module: str, variable: str, value):
        """Set key in database"""
        raise NotImplementedError

    def remove(self, module: str, variable: str):
        """Remove key from database"""
        raise NotImplementedError
    
    def drop_table(self, module: str):
        """Drop table in database"""
        raise NotImplementedError
        
    def get_collection(self, module: str) -> dict:
        """Get database for selected module"""
        raise NotImplementedError
    
    def exists(self, module: str, variable: str) -> bool:
        """Check if a key exists in the database"""
        raise NotImplementedError

    def keys(self) -> list:
        """Get all table names in database"""
        raise NotImplementedError

    def close(self):
        """Close the database"""
        raise NotImplementedError

class SqliteDatabase(Database):
    def __init__(self, file):
        self._conn = sqlite3.connect(file, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._cursor = self._conn.cursor()
        self._lock = threading.Lock()

    @staticmethod
    def _parse_row(row: sqlite3.Row):
        if row["type"] == "bool":
            return row["val"] == "1"
        elif row["type"] == "int":
            return int(row["val"])
        elif row["type"] == "str":
            return row["val"]
        else:
            return json.loads(row["val"])

    def _execute(self, module: str, *args, **kwargs) -> sqlite3.Cursor:
        self._lock.acquire()
        try:
            return self._cursor.execute(*args, **kwargs)
        except sqlite3.OperationalError as e:
            if str(e).startswith("no such table"):
                sql = f"""
                CREATE TABLE IF NOT EXISTS '{module}' (
                var TEXT UNIQUE NOT NULL,
                val TEXT NOT NULL,
                type TEXT NOT NULL
                )
                """
                self._cursor.execute(sql)
                self._conn.commit()
                return self._cursor.execute(*args, **kwargs)
            raise e from None
        finally:
            self._lock.release()

    def get(self, module: str, variable: str, default=None):
        sql = f"SELECT * FROM '{module}' WHERE var=:var"
        cur = self._execute(module, sql, {"tabl": module, "var": variable})

        row = cur.fetchone()
        if row is None:
            return default
        else:
            return self._parse_row(row)

    def set(self, module: str, variable: str, value) -> bool:
        sql = f"""
        INSERT INTO '{module}' VALUES ( :var, :val, :type )
        ON CONFLICT (var) DO
        UPDATE SET val=:val, type=:type WHERE var=:var
        """

        if isinstance(value, bool):
            val = "1" if value else "0"
            typ = "bool"
        elif isinstance(value, str):
            val = value
            typ = "str"
        elif isinstance(value, int):
            val = str(value)
            typ = "int"
        else:
            val = json.dumps(value)
            typ = "json"

        self._execute(module, sql, {"var": variable, "val": val, "type": typ})
        self._conn.commit()

        return True

    def remove(self, module: str, variable: str):
        sql = f"DELETE FROM '{module}' WHERE var=:var"
        self._execute(module, sql, {"var": variable})
        self._conn.commit()

    def get_collection(self, module: str) -> dict:
        sql = f"SELECT * FROM '{module}'"
        cur = self._execute(module, sql)

        collection = {}
        for row in cur:
            collection[row["var"]] = self._parse_row(row)

        return collection
    
    def drop_table(self, module: str):
        sql = f"DROP TABLE IF EXISTS '{module}'"
        self._execute(module, sql)
        self._conn.commit()
        return
    
    def exists(self, module: str, variable: str) -> bool:
        sql = f"SELECT COUNT(*) FROM '{module}' WHERE var=:var"
        cur = self._execute(module, sql, {"var": variable})
        
        return cur.fetchone()[0] > 0

    def keys(self) -> list:
        """Get all table names in database"""
        self._lock.acquire()
        try:
            self._cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = self._cursor.fetchall()
            return [table[0] for table in tables]
        finally:
            self._lock.release()

    def close(self):
        self._conn.commit()
        self._conn.close()

db = SqliteDatabase('db.db')
__all__ = ['db']