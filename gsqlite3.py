""" A gevent friendly wrapper for the standard 'sqlite3' module.

The strategy used is a simple one.  All potentially time consuming
operations are run using the threadpool attached to the ``gevent`` hub.
"""

from functools import wraps

# We want to look as much like the sqlite3 DBAPI module as possible.
# The easiest way of exposing the same module interface is to do this.
from sqlite3 import *
import sqlite3

from gevent.hub import get_hub


@wraps(sqlite3.connect)
def connect(*args, **kwargs):
    kwargs['factory'] = Connection
    return sqlite3.connect(*args, **kwargs)


def _using_threadpool(method):
    @wraps(method, ['__name__', '__doc__'])
    def apply(*args, **kwargs):
        return get_hub().threadpool.apply(method, args, kwargs)
    return apply


class Cursor(sqlite3.Cursor):
    """ A greenlet friendly sub-class of sqlite3.Cursor. """


for method in [sqlite3.Cursor.execute,
               sqlite3.Cursor.executemany,
               sqlite3.Cursor.executescript,
               sqlite3.Cursor.fetchone,
               sqlite3.Cursor.fetchmany,
               sqlite3.Cursor.fetchall,
               sqlite3.Cursor.next]:
    setattr(Cursor, method.__name__, _using_threadpool(method))



class Connection(sqlite3.Connection):
    """ A greenlet friendly sub-class of sqlite3.Connection. """

    def __init__(self, *args, **kwargs):
        # by default [py]sqlite3 checks that object methods are run in the same
        # thread as the one that created the Connection or Cursor. If it finds
        # they are not then an exception is raised.
        # <https://docs.python.org/2/library/sqlite3.html#multithreading>
        # Luckily for us we can switch this check off.
        kwargs['check_same_thread'] = False
        super(Connection, self).__init__(*args, **kwargs)

    def cursor(self):
        return Cursor(self)


for method in [sqlite3.Connection.commit,
               sqlite3.Connection.rollback]:
    setattr(Connection, method.__name__, _using_threadpool(method))


#
# A dialect for SQLAlchemy. For example 'sqlite+gsqlite3://'.

try:
    from sqlalchemy.dialects.sqlite.pysqlite import SQLiteDialect_pysqlite
except ImportError:
    pass
else:
    class SQLiteDialect_gsqlite3(SQLiteDialect_pysqlite):

        @classmethod
        def dbapi(cls):
            import gsqlite3
            return gsqlite3
