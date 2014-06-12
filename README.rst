StormSpans
==========
StormSpans brings support for PostgreSQL's range types [#]_ to Canonical's
Storm [#]_ using PsycoSpans [#]_ paired with Spans [#]_.

Installation
------------
Psycospans exists on PyPI.

::

    pip install psycospans

Documentation
-------------
For full doumentation please run ``pydoc stormspans`` from a shell.

Example
-------

::

	from spans import intrange
	from storm.locals import *
	from stormspans import IntRange

	class Model(Storm):
		id = Int(primary=True)
		span = IntRange(default=intrange(1, 10))

.. [#] http://www.postgresql.org/docs/9.2/static/rangetypes.html
.. [#] http://storm.canonical.com/
.. [#] https://github.com/runfalk/psycospans
.. [#] https://github.com/runfalk/spans
