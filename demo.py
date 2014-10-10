""" Demo of parallel queries using ``gsqlite3``. """

import os
from functools import partial
from random import randint
from timeit import Timer
import gevent
import sqlite3
import gsqlite3


filename = os.path.join(os.path.dirname(__file__), 'demo.sqlite')
select_stmt = "SELECT * FROM example WHERE value >= ? AND value < ?"
num_rows_to_fetch = 100000

def populate(module, num_rows=1000000):
    con = module.connect(filename)
    con.execute("CREATE TABLE IF NOT EXISTS example (value)")
    (count,) = con.execute("SELECT count(1) FROM example").fetchone()
    if count < num_rows:
        num_rows -= count
        values = [(randint(1, 1000000),) for _ in xrange(num_rows)]
        print "Populating '{}' ...".format(filename)
        insert = "INSERT INTO example (value) VALUES (?)"
        con.executemany(insert, values)
        con.commit()


def query(module, lower, upper):
    con = module.connect(filename)
    cur = con.cursor()
    cur.execute(select_stmt, (lower, upper))
    cur.fetchmany(num_rows_to_fetch)


def query_using_greenlets(module):
    g1 = gevent.spawn(query, module, 10, 100)
    g2 = gevent.spawn(query, module, 100, 1000)
    g3 = gevent.spawn(query, module, 1000, 5000)
    gevent.joinall([g1, g2, g3])


def main():
    modules = [gsqlite3, sqlite3]
    # either module will work here
    populate(modules[0])
    for module in modules:
        time_query_using_module(module)
    os.unlink(filename)
    return None

def time_query_using_module(module):
    # This is largely copied verbatim from the 'timeit' module
    repeat = 3
    number = 10
    verbose = False
    precision = 3
    stmt = partial(query_using_greenlets, module)
    t = Timer(stmt)
    try:
        r = t.repeat(repeat, number)
    except:
        t.print_exc()
        return 1
    best = min(r)
    if verbose:
        print "raw times:", " ".join(["%.*g" % (precision, x) for x in r])
    print "%s: %d loops," % (module.__name__, number),
    usec = best * 1e6 / number
    if usec < 1000:
        print "best of %d: %.*g usec per loop" % (repeat, precision, usec)
    else:
        msec = usec / 1000
        if msec < 1000:
            print "best of %d: %.*g msec per loop" % (repeat, precision, msec)
        else:
            sec = msec / 1000
            print "best of %d: %.*g sec per loop" % (repeat, precision, sec)

if __name__ == '__main__':
    main()
