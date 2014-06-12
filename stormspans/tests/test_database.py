from datetime import date, datetime, timedelta
from os import environ
from psycopg2 import ProgrammingError
from spans import *
from storm.expr import State
from storm.locals import *
from storm.variables import ListVariable
from unittest import TestCase, skipUnless

from .. import *
from ..database import install_range
from ..expr import *
from ..properties import RangeProperty
from ..variables import \
    RangeVariable, \
    IntRangeVariable, \
    FloatRangeVariable, \
    DateRangeVariable, \
    DateTimeRangeVariable

@skipUnless(
    environ.get("STORM_POSTGRES_URI"),
    "No Storm Postgres URI provided, skipping database tests")
class TestDatabase(TestCase):
    def setUp(self):
        self.store = Store(create_database(environ["STORM_POSTGRES_URI"]))
        self.create_tables()
        self.fill_data()
        self.store.commit()

    def tearDown(self):
        self.store.rollback()
        self.drop_tables()
        self.store.commit()

    def create_tables(self):
        pass

    def fill_data(self):
        pass

    def drop_tables(self):
        pass

class TestOperators(TestDatabase):
    def run_operator(self, operator, arg1, arg2):
        return self.store.execute(Select(operator(arg1, arg2))).get_one()[0]

    def test_contains(self):
        self.assertTrue(self.run_operator(
            Contains, intrange(1, 5), intrange(1, 5)))
        self.assertFalse(self.run_operator(
            Contains, intrange(1, 5), intrange(1, 5, upper_inc=True)))

    def test_within(self):
        self.assertTrue(self.run_operator(
            Within, intrange(1, 5), intrange(1, 5, upper_inc=True)))
        self.assertFalse(self.run_operator(
            Within, intrange(1, 5, upper_inc=True), intrange(1, 5)))

    def test_overlap(self):
        self.assertTrue(self.run_operator(
            Overlap, intrange(1, 5), intrange(3, 8)))
        self.assertFalse(self.run_operator(
            Overlap, intrange(1, 5), intrange(5, 10)))

    def test_adjacent(self):
        self.assertFalse(self.run_operator(
            Adjacent, intrange(1, 5), intrange(3, 8)))
        self.assertTrue(self.run_operator(
            Adjacent, intrange(1, 5), intrange(5, 10)))

    def test_startsafter(self):
        self.assertFalse(self.run_operator(
            StartsAfter, intrange(1, 5), intrange(3, 8)))
        self.assertTrue(self.run_operator(
            StartsAfter, intrange(1, 5), intrange(1, 5)))
        self.assertTrue(self.run_operator(
            StartsAfter, intrange(5, 10), intrange(1, 5)))

    def test_endsbefore(self):
        self.assertTrue(self.run_operator(
            EndsBefore, intrange(1, 5), intrange(3, 8)))
        self.assertTrue(self.run_operator(
            EndsBefore, intrange(1, 5), intrange(1, 5)))
        self.assertFalse(self.run_operator(
            EndsBefore, intrange(5, 10), intrange(1, 5)))

class TestFunctions(TestDatabase):
    def run_expr(self, expr):
        return self.store.execute(Select(expr)).get_one()[0]

    def test_lower_inc(self):
        self.assertTrue(self.run_expr(LowerInc(intrange(1, 5))))
        self.assertTrue(self.run_expr(LowerInc(intrange(1, 5, lower_inc=False))))
        self.assertFalse(self.run_expr(LowerInc(floatrange(1.0, 5.0, lower_inc=False))))

    def test_upper_inc(self):
        self.assertFalse(self.run_expr(UpperInc(intrange(1, 5))))
        self.assertFalse(self.run_expr(UpperInc(intrange(1, 5, upper_inc=True))))
        self.assertTrue(self.run_expr(UpperInc(floatrange(1.0, 5.0, upper_inc=True))))

    def test_lower_inf(self):
        self.assertTrue(self.run_expr(LowerInf(intrange(upper=5))))
        self.assertFalse(self.run_expr(LowerInf(intrange(1))))

    def test_upper_inf(self):
        self.assertFalse(self.run_expr(UpperInf(intrange(upper=5))))
        self.assertTrue(self.run_expr(UpperInf(intrange(1))))

class TestIntRangeDatabase(TestDatabase):
    class SimpleModel(Storm):
        __storm_table__ = "int_range_test"

        id = Int(primary=True, default=AutoReload)
        span = IntRange(default=intrange(10, 15))

        def __init__(self, span=None):
            if span is not None:
                self.span = span

    def create_tables(self):
        self.store.execute("""
            CREATE TABLE int_range_test(
                id SERIAL,
                span int4range
            )
        """)

    def fill_data(self):
        self.store.execute("""
            INSERT INTO int_range_test(span) VALUES (?),(?),(?)
        """, [intrange(1, 5), intrange(3, 8), intrange(5, 10)])

    def drop_tables(self):
        self.store.execute("""
            DROP TABLE IF EXISTS
                int_range_test
                CASCADE
        """)

    def test_get(self):
        ir = self.store.get(self.SimpleModel, 1)

        self.assertIsNot(ir, None)
        self.assertEquals(ir.span, intrange(1, 5))

    def test_default_insert(self):
        ir = self.SimpleModel()
        self.store.add(ir)
        self.store.commit()
        self.store.invalidate(ir)

        self.assertEquals(ir.span, intrange(10, 15))

    def test_insert(self):
        ir = self.SimpleModel(intrange(upper=10, lower_inc=False))
        self.store.add(ir)
        self.store.commit()
        self.store.invalidate(ir)

        self.assertEquals(ir.span, intrange(upper=10, lower_inc=False))

    def test_simple_functions(self):
        self.assertEqual(
            list(self.store.find(
                self.SimpleModel.span.lower()).order_by(self.SimpleModel.id)),
            [1, 3, 5])
        self.assertEqual(
            list(self.store.find(
                self.SimpleModel.span.upper()).order_by(self.SimpleModel.id)),
            [5, 8, 10])

        self.assertEqual(
            list(self.store.find(
                self.SimpleModel.span.lower_inc()).order_by(self.SimpleModel.id)),
            [True] * 3)
        self.assertEqual(
            list(self.store.find(
                self.SimpleModel.span.upper_inc()).order_by(self.SimpleModel.id)),
            [False] * 3)

        self.assertEqual(
            list(self.store.find(
                self.SimpleModel.span.lower_inf()).order_by(self.SimpleModel.id)),
            [False] * 3)
        self.assertEqual(
            list(self.store.find(
                self.SimpleModel.span.upper_inf()).order_by(self.SimpleModel.id)),
            [False] * 3)

    def test_contains(self):
        self.assertEqual(self.store.find(
            self.SimpleModel,
            self.SimpleModel.span.contains(1)).count(), 1)
        self.assertEqual(self.store.find(
            self.SimpleModel,
            self.SimpleModel.span.contains(3)).count(), 2)
        self.assertEqual(self.store.find(
            self.SimpleModel,
            self.SimpleModel.span.contains(5)).count(), 2)
        self.assertEqual(self.store.find(
            self.SimpleModel,
            self.SimpleModel.span.contains(10)).count(), 0)

        self.assertEqual(self.store.find(
            self.SimpleModel,
            self.SimpleModel.span.contains(intrange(1, 3))).count(), 1)
        self.assertEqual(self.store.find(
            self.SimpleModel,
            self.SimpleModel.span.contains(intrange(3, 5))).count(), 2)
        self.assertEqual(self.store.find(
            self.SimpleModel,
            self.SimpleModel.span.contains(intrange(5, 8))).count(), 2)
        self.assertEqual(self.store.find(
            self.SimpleModel,
            self.SimpleModel.span.contains(intrange(10, 15))).count(), 0)

class TimeDeltaRangeVariable(RangeVariable):
    range_type = timedeltarange

class TimeDeltaRange(RangeProperty):
    variable_class = TimeDeltaRangeVariable

class CustomTypeModel(Storm):
    __storm_table__ = "td_range_test"

    id = Int(primary=True)
    span = TimeDeltaRange()
    spans = List(type=TimeDeltaRange())

class TestCustomRangeDatabase(TestDatabase):
    class SimpleModel(Storm):
        __storm_table__ = "int_range_test"

        id = Int(primary=True, default=AutoReload)
        span = IntRange(default=intrange(10, 15))

        def __init__(self, span=None):
            if span is not None:
                self.span = span

    def setUp(self):
        super(TestCustomRangeDatabase, self).setUp()

        # Create tables
        try:
            self.store.execute("""
                CREATE TYPE intervalrange AS RANGE(SUBTYPE = interval)
            """)
        except ProgrammingError:
            # The type already exists in this database
            self.store.rollback()

        self.store.execute("""
            CREATE TABLE IF NOT EXISTS td_range_test(
                id SERIAL,
                span intervalrange,
                spans intervalrange[]
            )
        """)

        self.store.commit()

        install_range("intervalrange", TimeDeltaRangeVariable, self.store)

        self.store.execute(
            "INSERT INTO td_range_test(span, spans) VALUES (?, ?)",
            [
                timedeltarange(timedelta(days=1), timedelta(days=5)),
                [timedeltarange(timedelta(days=1), timedelta(days=2))]])
        self.store.commit()

    def drop_tables(self):
        self.store.execute("""
            DROP TABLE IF EXISTS
                td_range_test
                CASCADE
        """)
        self.store.execute("""DROP TYPE intervalrange CASCADE""")

    def test_get(self):
        r = self.store.get(CustomTypeModel, 1)

        self.assertEqual(
            r.span, timedeltarange(timedelta(days=1), timedelta(days=5)))
        self.assertEqual(
            r.spans, [timedeltarange(timedelta(days=1), timedelta(days=2))])

    def test_insert(self):
        r = CustomTypeModel()
        r.span = timedeltarange(timedelta(days=1), timedelta(days=10))
        r.spans = [
            timedeltarange(timedelta(days=1), timedelta(days=5)),
            timedeltarange(timedelta(days=5), timedelta(days=10))]
        self.store.add(r)
        self.store.commit()

        self.store.invalidate(r)
        self.assertEqual(
            r.span, timedeltarange(timedelta(days=1), timedelta(days=10)))
        self.assertEqual(
            r.spans,
            [
                timedeltarange(timedelta(days=1), timedelta(days=5)),
                timedeltarange(timedelta(days=5), timedelta(days=10))])

