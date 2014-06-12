from storm.expr import Column, Undef, Add, Sub, Mul, LShift, RShift, Lower, Upper
from storm.locals import *
from storm.properties import Property, PropertyColumn

from .variables import *
from .expr import *

__all__ = [
    "IntRange",
    "FloatRange",
    "DateRange",
    "DateTimeRange"
]


class RangeProperty(Property):
    def __init__(self, name=None, primary=False, type=None, **kwargs):
        if type is None:
            type = Property()

        kwargs["value"] = kwargs.pop("default", Undef)
        kwargs["value_factory"] = kwargs.pop("default_factory", Undef)

        Property.__init__(self, name, primary, self.variable_class, kwargs)

    def _get_column(self, cls):
        # Cache per-class column values in the class itself, to avoid
        # holding a strong reference to it here, and thus rendering
        # classes uncollectable in certain situations (e.g. subclasses
        # where the property is stored in the base).
        try:
            # Use class dictionary explicitly to get sensible
            # results on subclasses.
            column = cls.__dict__["_storm_columns"].get(self)
        except KeyError:
            cls._storm_columns = {}
            column = None
        if column is None:
            attr = self._detect_attr_name(cls)
            if self._name is None:
                name = attr
            else:
                name = self._name
            column = RangePropertyColumn(self, cls, attr, name, self._primary,
                                    self._variable_class,
                                    self._variable_kwargs)
            cls._storm_columns[self] = column
        return column

class RangeComparable(object):
    def lower(self):
        return Lower(self)

    def upper(self):
        return Upper(self)

    def lower_inc(self):
        return LowerInc(self)

    def upper_inc(self):
        return UpperInc(self)

    def lower_inf(self):
        return LowerInf(self)

    def upper_inf(self):
        return UpperInf(self)

    def contains(self, other):
        return Contains(self, other)

    def within(self, other):
        return Within(self, other)

    def overlap(self, other):
        return Overlap(self, other)

    def adjacent(self, other):
        return Adjacent(self, other)

    def union(self):
        return Add(self, other)

    def difference(self, other):
        return Sub(self, other)

    def intersection(self, other):
        return Mul(self, other)

    def left_of(self, other):
        return LShift(self, other)

    def right_of(self, other):
        return RShift(self, other)

    def __contains__(self, other):
        return Contains(self, other)

    def __lshift__(self, other):
        return self.left_of(other)

    def __rshift__(self, other):
        return self.right_of(other)

class RangePropertyColumn(RangeComparable, PropertyColumn):
    pass

class IntRange(RangeProperty):
    variable_class = IntRangeVariable

class FloatRange(RangeProperty):
    variable_class = FloatRangeVariable

class DateRange(RangeProperty):
    variable_class = DateRangeVariable

class DateTimeRange(RangeProperty):
    variable_class = DateTimeRangeVariable
