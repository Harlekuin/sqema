# -*- coding: utf-8 -*-
"""Defines the Sqema class."""
import pathlib
from typing import List

import simqle
import pandas as pd


class DatabaseRoot:
    def __init__(self, database_directory: str, con_name: str):
        """

        :type con_name: str
        :type sqema_directory: str
        """
        self.con_name = con_name
        self.path = pathlib.Path(database_directory)

    def find_object(self, cm, search_path=None, schema=None):
        for path in (search_path or self.path).iterdir():

            if path.is_dir():
                if str(path).endswith(".table"):  # object found

                    self.ensure_table(cm, path, schema)
                else:

                    if str(path).endswith(".schema"):
                        self.find_object(cm, path, schema=path.stem)

    def ensure_table(self, cm, path, schema):
        # check for definition
        definition_path = pathlib.Path(path, "definition.sql")
        if definition_path.exists():
            with open(definition_path, "r") as f:
                sql = f.read()

            cm.execute_sql(sql=sql, con_name=self.con_name)

        # check for example data
        data_path = pathlib.Path(path, "data.csv")
        if data_path.exists():
            table_name = path.stem

            with open(data_path, "r") as f:
                data_df = pd.read_csv(f)
                con = cm.get_engine(con_name=self.con_name)

                kwargs = {
                    "name": table_name,
                    "con": con,
                    "if_exists": "append",
                    "index": False
                }

                if schema:
                    kwargs["schema"] = schema

                data_df.to_sql(**kwargs)


class Sqema:
    """The Sqema class."""
    database_roots: List[DatabaseRoot]

    def __init__(self, cm: simqle.ConnectionManager,
                 sqema_directory="./sqema.sqema"):
        """
        Initialise a Sqema class.

        args:
         - cm: a simqle.ConnectionManager object
         - sqema_directory: the directory that describes the SQL schema
        """
        self.cm = cm
        self.sqema_directory = sqema_directory
        self.database_roots = []

    def ensure_sql_environment(self):
        """Ensure a SQL environment."""
        root_path = pathlib.Path(self.sqema_directory)

        # look for possible database paths
        for connection in self.cm.config["connections"]:
            con_name = connection["name"]
            database_path = pathlib.Path(root_path, con_name + ".database")
            if database_path.exists():
                self.database_roots.append(DatabaseRoot(database_path,
                                                        con_name))

        for database_root in self.database_roots:
            database_root.find_object(self.cm)
