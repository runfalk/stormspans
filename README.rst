StormSpans
==========
StormSpans brings support for PostgreSQL's
`range types <http://www.postgresql.org/docs/current/static/rangetypes.html>`_
to Canonical's `Storm ORM <http://storm.canonical.com/>`_ using
`PsycoSpans <https://github.com/runfalk/psycospans>`_ paired with
`Spans <https://github.com/runfalk/spans>`_.

This package's functionality probably be merged with
`storm-legacy <https://github.com/runfalk/storm-legacy>`_ in the future.


Installation
------------
Psycospans exists on PyPI.

.. code-block:: bash

    pip install psycospans


Documentation
-------------
For full doumentation please run ``pydoc stormspans`` from a shell.


Example
-------
.. code-block:: python

    from spans import intrange
    from storm.locals import *
    from stormspans import IntRange


    class Model(Storm):
        id = Int(primary=True)
        span = IntRange(default=intrange(1, 10))

        def __init__(self, span):
            self.span = span


    # NOTE: URI must start with postgres+spans://
    store = Store(create_database("postgres+spans://<url>"))
    store.execute("""
        CREATE TABLE int_range_test(
            id SERIAL,
            span int4range
        )
    """)

    store.add(Model(intrange(1, 100))
    store.commit()


Changelog
=========


Version 1.0.0
-------------
Released on 9th October 2018

- Added support for `storm-legacy <https://github.com/runfalk/storm-legacy>`_
- Added support for Python 3.4 and later. Note that this only work with
  ``storm-legacy`` since Storm is not Python 3 compatible


Version 0.1.0
-------------
Released 12th June 2014

- Initial commit
