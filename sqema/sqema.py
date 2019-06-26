# -*- coding: utf-8 -*-
"""Defines the Sqema class."""


class Sqema:
    """The Sqema class."""

    def __init__(self, cm, sqema_directory="./sqema.sqema"):
        """
        Initialise a Sqema class.

        args:
         - cm: a simqle.ConnectionManager object
         - sqema_directory: the directory that describes the SQL schema
        """
        self.cm = cm
        self.sqema_directory = sqema_directory

    def ensure_sql_environment(self):
        """Ensure a SQL environment."""
        pass
