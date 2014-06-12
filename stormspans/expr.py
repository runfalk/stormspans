from storm.expr import NamedFunc, BinaryOper

__all__ = [
    "Within",
    "Contains",
    "Overlap",
    "Adjacent",
    "StartsAfter",
    "EndsBefore",

    "LowerInc",
    "UpperInc",
    "LowerInf",
    "UpperInf"
]

class Within(BinaryOper):
    __slots__ = ()
    oper = " <@ "

class Contains(BinaryOper):
    __slots__ = ()
    oper = " @> "

class Overlap(BinaryOper):
    __slots__ = ()
    oper = " && "

class Adjacent(BinaryOper):
    __slots__ = ()
    oper = " -|- "

class StartsAfter(BinaryOper):
    __slots__ = ()
    oper = " &> "

class EndsBefore(BinaryOper):
    __slots__ = ()
    oper = " &< "

class LowerInc(NamedFunc):
    __slots__ = ()
    name = "lower_inc"

class UpperInc(NamedFunc):
    __slots__ = ()
    name = "upper_inc"

class LowerInf(NamedFunc):
    __slots__ = ()
    name = "lower_inf"

class UpperInf(NamedFunc):
    __slots__ = ()
    name = "upper_inf"
