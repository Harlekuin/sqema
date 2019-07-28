# -*- coding: utf-8 -*-
"""Defines the Sqema class."""
import pathlib

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

        def check_process(endings):
            # iterdir will check in schema folders
            for path in (search_path or self.path).iterdir():
                if path.is_dir():
                    for ending in endings:
                        if str(path).endswith(".{}".format(ending)):
                            self.ensure_process(cm, path)

        # Run 1: Pre settings
        check_process(endings=["presetting"])

        # Run 2: Tables
        for path in (search_path or self.path).iterdir():
            if path.is_dir():
                if str(path).endswith(".table"):
                    print(f"adding table {str(path)}")
                    self.ensure_table(cm, path, schema)

        # Run 3: Indexes
        check_process(endings=["index"])

        # Run 4: Views, Procedures and Functions
        check_process(endings=["view", "procedure", "function"])

        # Run 5: Other
        check_process(endings=["other"])

        # Run 6: Post Settings
        check_process(endings=["postsetting"])

    def ensure_process(self, cm, path):
        sql = self.get_definition(path)
        if not sql:
            print(f"no sql found for {path}")
            return
        cm.execute_sql(sql=sql, con_name=self.con_name)

    def ensure_table(self, cm, path, schema):
        self.ensure_process(cm, path)

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

        index_path = pathlib.Path(path, "index.sql")
        if index_path.exists():
            with open(index_path, "r") as f:
                sql = f.read()

            cm.execute_sql(sql=sql, con_name=self.con_name)

    @staticmethod
    def get_definition(path):
        definition_path = pathlib.Path(path, "definition.sql")
        if definition_path.exists():
            with open(definition_path, "r") as f:
                return f.read()


class Sqema:
    """The Sqema class."""

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
