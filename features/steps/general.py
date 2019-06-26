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

@when("we ensure the test environment")
def ensure_test_environment(context):
    os.environ["SIMQLE_TEST"] = "True"

    my_sqema = Sqema(cm=context.cm,
                     sqema_directory=context.sqema_directory)

    my_sqema.ensure_sql_environment()

    del os.environ["SIMQLE_TEST"]

# --- When ---


# --- Then ---

@then("the test database matches the production database")
def test_database_matches_production(context):
    """
    Check if the test database matches the attempted sqema.

    The table looks like:

    CREATE TABLE [MySchema].[MyTable] (
      id INT PRIMARY KEY ASC AUTOINCREMENT,
      FirstName TEXT,
      Age INT,
      Score REAL
    )
    """
    os.environ["SIMQLE_TEST"] = "True"

    sql = """
        select id, FirstName, Age, Score
        from [MySchema].[MyTable]
    """

    rst = context.cm.recordset(con_name="my-sqlite-database", sql=sql)

    correct_rst = (
        ["id", "FirstName", "Age", "Score"],

        [
            (1, "James", 34, 28.5),
            (2, "Thea", 29, 6.05),
        ]
    )

    assert rst == correct_rst

    del os.environ["SIMQLE_TEST"]

# --- Then ---
