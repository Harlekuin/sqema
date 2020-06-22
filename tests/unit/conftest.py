from sqema import Sqema
import pytest


@pytest.fixture
def test_sqema():
    class TestSqema(Sqema):
        def __init__(self, sqema, cm, mode):
            self.definition = sqema
            self.cm = cm
            self.mode = mode

    return TestSqema
