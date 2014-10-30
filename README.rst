gsqlite3
========

A gevent-ification of pysqlite3, including a SQLAlchemy dialect.

The module takes a simple approach of any potentiall long running methods off 
to the gevent hub threadpool for execution.


SQLAlchemy
----------
You can use gsqlite3 with SQLAlchemy by specifying 'sqlite+gsqlite3' as your URL scheme.
