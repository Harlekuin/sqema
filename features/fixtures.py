"""BDD fixtures."""

import os
from behave import fixture


@fixture
def sqlite_database(context):
    """Ensure that temporary sqlite databases are removed."""
    sqlite_cleanup()
    context.add_cleanup(sqlite_cleanup)
    return


def sqlite_cleanup():
    """Remove all known test databases."""
    databases = [
        "/tmp/database.db",
        "/tmp/production-database.db",
        "/tmp/development-database.db",
        "/tmp/test-database.db",
    ]

    for database in databases:
        try:
            os.remove(database)
        except OSError:
            pass
