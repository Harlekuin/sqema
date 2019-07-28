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
    raise

# --- When ---


# --- Then ---

@then("the {mode} tables match the sqema")
def test_tables(context, mode):
    """Check if the tables match the sqema"""
    os.environ["SIMQLE_MODE"] = mode

    # --- sqlite connection 1 ---
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
    # --- sqlite connection 1 ---

    # --- sqlite connection 2 ---
    sql = """
        select id, FirstName, Age, Score
        from [MyTable]
    """

    rst = context.cm.recordset(con_name="my-sqlite-database2", sql=sql)
    correct_rst = (
        [
            (1, "James", 34, 28.5),
            (2, "Thea", 29, 6.06),
        ],

        ["id", "FirstName", "Age", "Score"],
    )

    assert rst == correct_rst
    # --- sqlite connection 2 ---

    # --- MySQL connection ---
    sql = "select id, testfield from AMySQLTable"
    rst = context.cm.recordset(con_name="my-mysql-database", sql=sql)
    correct_rst = (
        [
            (1, "somedata"),
            (2, "some more data"),
        ],

        ["id", "testfield"],
    )
    assert rst == correct_rst
    # --- MySQL connection ---

    # --- PostGreSQL connection ---
    sql = "select id, testfield from apostgresqltable"
    rst = context.cm.recordset(con_name="my-postgresql-database", sql=sql)
    correct_rst = (
        [
            (1, "somedata 2"),
            (2, "some more data 2"),
        ],

        ["id", "testfield"],
    )
    assert rst == correct_rst
    # --- PostGreSQL connection ---

    del os.environ["SIMQLE_MODE"]


@then("the {mode} views match the sqema")
def test_views(context, mode):
    """Check if the tables match the sqema"""
    os.environ["SIMQLE_MODE"] = mode

    sql = """
        select FirstName, HalfAge
        from [MyView]
    """

    rst = context.cm.recordset(con_name="my-sqlite-database", sql=sql)
    correct_rst = (
        [
            ("James", 17),
            ("Thea", 14.5),
        ],

        ["FirstName", "HalfAge"],
    )

    assert rst == correct_rst
    del os.environ["SIMQLE_MODE"]


@then("the {mode} procedures match the sqema")
def test_procedures(context, mode):
    """Check if the tables match the sqema"""
    os.environ["SIMQLE_MODE"] = mode

    sql = "call MySP();"
    rst = context.cm.recordset(con_name="my-mysql-database", sql=sql)
    correct_rst = (
        [
            (1, "somedata"),
            (2, "some more data"),
        ],

        ["id", "testfield"],
    )
    assert rst == correct_rst

    del os.environ["SIMQLE_MODE"]


@then("the {mode} functions match the sqema")
def test_functions(context, mode):
    """Check if the tables match the sqema"""
    os.environ["SIMQLE_MODE"] = mode

    sql = """
        select 
            id, 
            testfield, 
            SomeFunction() as somenum
            from AMySQLTable;
        """
    rst = context.cm.recordset(con_name="my-mysql-database", sql=sql)
    correct_rst = (
        [
            (1, "somedata", 3),
            (2, "some more data", 3),
        ],

        ["id", "testfield", "somenum"],
    )
    assert rst == correct_rst

    del os.environ["SIMQLE_MODE"]


@then("the {mode} indexes match the sqema")
def test_indexes(context, mode):
    """Check if the tables match the sqema"""
    os.environ["SIMQLE_MODE"] = mode

    sql = "PRAGMA index_list(MyTable);"

    rst = context.cm.recordset(con_name="my-mysql-database", sql=sql)

    correct_rst = ([(0, "idx_MyTable_FirstName", 1), ],
                   ["seq", "name", "unique"],)
    print(rst)
    print(correct_rst)

    assert rst == correct_rst

    del os.environ["SIMQLE_MODE"]
