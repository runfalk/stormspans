from storm.databases.postgres import Postgres, PostgresConnection, compile as postgres_compile
from psycospans import connect, register_range_type
from spans import *
from spans.types import range_ as spansbase

__all__ = [
    "install_range"
]

compile = postgres_compile.create_child()

@compile.when(spansbase)
def compile_range(compile, range, state):
    state.parameters.append(range)
    return "?"

class PostgresStormSpansConnection(PostgresConnection):
    compile = compile

class PostgresStormSpans(Postgres):
    connection_factory = PostgresStormSpansConnection

    def raw_connect(self):
        raw_connection = connect(self._dsn)

        if self._version is None:
            self._version = raw_connection.server_version

        raw_connection.set_client_encoding("UTF8")
        raw_connection.set_isolation_level(self._isolation)
        return raw_connection

def install_range(pgrange, pyrange_variable, store):
    register_range_type(
        pgrange,
        pyrange_variable.range_type,
        store._connection._raw_connection)
