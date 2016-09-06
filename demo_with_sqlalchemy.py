from __future__ import print_function
import sys
import gevent
from sqlalchemy import create_engine, MetaData, Table, Column, Integer


try:
    xrange
except:
    assert sys.version_info >= (3,)
    xrange = range


def create_table_and_query(engine):

    metadata = MetaData()
    table = Table('example', metadata, Column('value', Integer))

    metadata.create_all(engine)
    engine.execute(table.insert(), [{'value':i} for i in xrange(1000000)])

    print("*" * 60)
    print(engine.url)
    print("*" * 60)
    # have a look and watch the serial/parallel execution
    engine.echo = True
    g1 = gevent.spawn(query, engine, table, 10, 20)
    g2 = gevent.spawn(query, engine, table, 500, 1000)
    gevent.joinall([g1, g2])


def query(engine, table, offset, limit):
    with engine.begin() as bind:
        select = table.select().offset(offset).limit(limit)
        assert len(bind.execute(select).fetchall()) == limit


def main():
    e1 = create_engine('sqlite://')
    e2 = create_engine('sqlite+gsqlite3://')
    for engine in [e1, e2]:
        create_table_and_query(engine)


if __name__ == '__main__':
    main()
