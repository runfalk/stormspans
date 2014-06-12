"""
StormSpans brings support for PostgreSQL's range types to Canonical's Storm
using PsycoSpans paired with Spans.

    from spans import intrange
    from storm.locals import *
    from stormspans import IntRange

    class Model(Storm):
        id = Int(primary=True)
        span = IntRange(default=intrange(1, 10))

To connect to the database "postgres+spans://..." must be specified instead of
"postgres://..."
"""

__version__ = "0.1.0"

from storm.database import register_scheme

from .database import PostgresStormSpans, install_range
from .properties import *

__all__ = [
    "IntRange",
    "FloatRange",
    "DateRange",
    "DateTimeRange",
    "install_range"
]

register_scheme("postgres+spans", PostgresStormSpans)
