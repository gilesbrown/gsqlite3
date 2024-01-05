gsqlite3
========

An experimental gevent-ification of pysqlite3, including a SQLAlchemy dialect.

The module takes a simple approach of any potentiall long running methods off 
to the gevent hub threadpool for execution.

This lets greenlet code perform parallel queries.  

Try the `demo <https://raw.githubusercontent.com/gilesbrown/gsqlite3/master/demo.py>`_  script.

.. code:: shell

    $ python demo.py
    Populating 'demo.sqlite' ...
    gsqlite3: 10 loops, best of 3: 105 msec per loop
    sqlite3: 10 loops, best of 3: 243 msec per loop

SQLAlchemy
----------
You can use gsqlite3 with SQLAlchemy by specifying 'sqlite+gsqlite3' as your URL scheme.
