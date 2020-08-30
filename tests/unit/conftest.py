from sqema import Sqema
import pytest

# from simqle import ConnectionManager


@pytest.fixture
def test_sqema():
    class TestSqema(Sqema):
        def __init__(self, sqema, cm, mode):
            self.definition = sqema
            self.cm = cm
            self.mode = mode

    return TestSqema


@pytest.fixture
def test_connection_manager():
    class TestConnectionManager:
        def __init__(self):
            pass

        def execute_sql(self, con_name, sql):
            pass

        def get_engine(self, con_name):
            return con_name

    return TestConnectionManager
