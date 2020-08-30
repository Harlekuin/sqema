from sqema import Sqema
from sqema.exceptions import NotAValidDefinitionError
import pandas


def test_sqema_class_init(mocker):
    # test if Sqema can init
    mocker.patch.object(Sqema, "setup_environment", auto_spec=True)

    sq = Sqema(sqema="", cm="")

    sq.setup_environment.assert_called()


def test_setup_environment(mocker):
    # should call setup_database for each database in the definition
    mocker.patch.object(Sqema, "setup_database", auto_spec=True)

    test_definition = {"databases": [{"name": "test_db_1"}, {"name": "test_db_2"}]}

    sq = Sqema(sqema=test_definition, cm="")

    sq.setup_database.assert_any_call({"name": "test_db_1"})
    sq.setup_database.assert_any_call({"name": "test_db_2"})

    assert sq.setup_database.call_count == 2


def test_setup_database(mocker, test_sqema):
    # should call setup_schema for each schema in the database
    sq = test_sqema(sqema="", cm="", mode="development")
    mocker.patch.object(Sqema, "setup_schema", auto_spec=True)

    test_database = {
        "name": "test_database",
        "schemas": [{"name": "test_schema_1"}, {"name": "test_schema_2"}],
    }

    sq.setup_database(database=test_database)

    sq.setup_schema.assert_any_call({"name": "test_schema_1"}, conn="test_database")
    sq.setup_schema.assert_any_call({"name": "test_schema_2"}, conn="test_database")

    assert sq.setup_schema.call_count == 2


def test_setup_schema(mocker, test_sqema):
    sq = test_sqema(sqema="", cm="", mode="development")

    mocker.patch.object(Sqema, "create_object", auto_spec=True)
    mocker.patch.object(Sqema, "insert_data", auto_spec=True)

    # config only object
    config_object = {"definition": {"type": "sql", "definition": "some config"}}

    test_config_schema = {"name": "test_schema", "config": [config_object]}

    sq.setup_schema(schema=test_config_schema, conn="some_conn")

    sq.create_object.assert_any_call(config_object, "some_conn")

    # table only object
    table_object = {
        "name": "test_table",
        "definition": {"type": "sql", "definition": "some table"},
        "post_definitions": [{"type": "sql", "sql": "some post definition"}],
        "data": [{"modes": ["development"], "file": "some_path"}],
    }

    test_table_schema = {"name": "test_schema", "tables": [table_object]}

    sq.setup_schema(schema=test_table_schema, conn="some_conn")

    sq.create_object.assert_any_call(table_object, "some_conn")
    sq.insert_data.assert_any_call(table_object, "some_conn", schema="test_schema")

    # view only object
    view_object = {"definition": {"type": "sql", "definition": "some view"}}

    test_view_schema = {"name": "test_schema", "views": [view_object]}

    sq.setup_schema(schema=test_view_schema, conn="some_conn")

    sq.create_object.assert_any_call(view_object, "some_conn")

    # other only object
    other_object = {"definition": {"type": "sql", "definition": "some other"}}

    test_other_schema = {"name": "test_schema", "others": [other_object]}

    sq.setup_schema(schema=test_other_schema, conn="some_conn")

    sq.create_object.assert_any_call(other_object, "some_conn")


def test_setup_schema_ordering(mocker, test_sqema):
    sq = test_sqema(sqema="", cm="", mode="development")

    mocker.patch.object(Sqema, "create_object", auto_spec=True)
    mocker.patch.object(Sqema, "insert_data", auto_spec=True)

    # check the ordering
    test_schema = {
        "name": "test_schema",
        "config": ["some config"],
        "tables": ["some table"],
        "views": ["some view"],
        "others": ["some other"],
    }

    sq.setup_schema(schema=test_schema, conn="some_conn")

    sq.create_object.assert_has_calls(
        [
            mocker.call("some config", "some_conn"),
            mocker.call("some table", "some_conn"),
            mocker.call("some view", "some_conn"),
            mocker.call("some other", "some_conn"),
        ]
    )


def test_get_sql(mocker):

    # -- inline sql definition --
    text_definition = {"type": "sql", "sql": "sql definition"}

    assert Sqema.get_sql(text_definition) == "sql definition"

    # -- file based definition --
    file_definition = {"type": "file", "path": "/some/path"}

    # create the mock open function
    test_read_data = "some test read data"
    m = mocker.mock_open(read_data=test_read_data)
    mocker.patch("builtins.open", m)

    assert Sqema.get_sql(file_definition) == test_read_data

    # invalid definition type
    invalid_definition = {"type": "notvalid"}
    try:
        Sqema.get_sql(invalid_definition)
    except NotAValidDefinitionError:
        pass


def test_create_object(mocker, test_sqema, test_connection_manager):
    cm = test_connection_manager()
    sq = test_sqema(sqema="", cm=cm, mode="development")
    test_object = {
        "name": "test name",
        "definition": "some definition",
        "post_definitions": [{"type": "sql", "sql": "some post definition",}],
    }

    mocker.patch.object(Sqema, "get_sql", auto_spec=True)

    sq.create_object(obj=test_object, conn="some conn")

    sq.get_sql.assert_any_call("some definition")
    sq.get_sql.assert_any_call(
        {"type": "sql", "sql": "some post definition",}
    )


def test_insert_data(mocker, test_sqema, test_connection_manager):
    cm = test_connection_manager()
    sq = test_sqema(sqema="", cm=cm, mode="development")

    # make sure nothing gets inserted if the mode doesn't match
    test_object = {"name": "test name", "data": [{"modes": ["test"]}]}

    mocker.patch.object(sq.cm, "get_engine", auto_spec=True)

    sq.insert_data(test_object, conn="some conn", schema="some schema")

    sq.cm.get_engine.assert_not_called()

    # test if the data is inserted if the modes match
    test_object = {
        "name": "test name",
        "data": [{"modes": ["development"], "file": "some file"}],
    }

    mocker.patch("pandas.read_csv")
    mocker.patch.object(pandas.DataFrame, "to_sql", auto_spec=True)

    sq.insert_data(table=test_object, conn="some conn", schema="some schema")

    pandas.read_csv.assert_called_once_with("some file")
    sq.cm.get_engine.assert_called_once_with("some conn")
