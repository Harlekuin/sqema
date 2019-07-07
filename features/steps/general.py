"""General BDD Steps."""

from behave import given, when, then
import simqle as sq
import os
from sqema import Sqema


# --- Given ---

@given("we are using the {directory} directory")
def use_directory(context, directory):
    context.directory = directory

    connections_file = "./features/{directory}/.connections.yaml".format(
        directory=directory
    )
    sqema_directory = "./features/{directory}/sqema".format(
        directory=directory
    )

    context.cm = sq.ConnectionManager(connections_file)
    context.sqema_directory = sqema_directory


# --- Given ---


# --- When ---

@when("we ensure the {mode} environment")
def ensure_test_environment(context, mode):
    os.environ["SIMQLE_MODE"] = mode

    my_sqema = Sqema(cm=context.cm,
                     sqema_directory=context.sqema_directory)

    my_sqema.ensure_sql_environment()

    del os.environ["SIMQLE_MODE"]


# --- When ---


# --- Then ---

@then("the {mode} databases match the sqema")
def test_database_matches_production(context, mode):
    """
    Check if the test database matches the attempted sqema.

    The table looks like:

    CREATE TABLE [main].[MyTable] (
      id INT PRIMARY KEY ASC AUTOINCREMENT,
      FirstName TEXT,
      Age INT,
      Score REAL
    )
    """
    os.environ["SIMQLE_MODE"] = mode

    sql = """
        select id, FirstName, Age, Score
        from [main].[MyTable]
    """

    rst = context.cm.recordset(con_name="my-sqlite-database", sql=sql)
    correct_rst = (
        [
            (1, "James", 34, 28.5),
            (2, "Thea", 29, 6.05),
        ],

        ["id", "FirstName", "Age", "Score"],
    )

    assert rst == correct_rst


    sql = """
        select id, FirstName, Age, Score
        from [MyTable]
    """

    rst = context.cm.recordset(con_name="my-sqlite-database2", sql=sql)
    correct_rst = (
        [
            (1, "James", 34, 28.5),
            (2, "Thea", 29, 6.05),
        ],

        ["id", "FirstName", "Age", "Score"],
    )

    assert rst == correct_rst


    del os.environ["SIMQLE_MODE"]

# --- Then ---
