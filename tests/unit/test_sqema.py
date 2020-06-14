from sqema import Sqema


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
