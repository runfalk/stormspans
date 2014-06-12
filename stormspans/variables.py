from storm.variables import Variable

from spans import *

__all__ = [
    "RangeVariable",
    "IntRangeVariable",
    "FloatRangeVariable",
    "DateRangeVariable",
    "DateTimeRangeVariable"
]

class RangeVariable(Variable):
    """
    Extension of standard variable class to handle conversion to and from Psycopg2
    range types
    """

    def parse_set(self, value, from_db):
        if not isinstance(value, self.range_type):
            raise ValueError(
                "Expected '{range_type.__name__}' '{value!r}' given".format(
                    range_type=self.range_type,
                    value=value))

        return value

    def parse_get(self, value, to_db):
        return value

# Define the builtin range properties and variables
class IntRangeVariable(RangeVariable):
    range_type = intrange

class FloatRangeVariable(RangeVariable):
    range_type = floatrange

class DateRangeVariable(RangeVariable):
    range_type = daterange

class DateTimeRangeVariable(RangeVariable):
    range_type = datetimerange
