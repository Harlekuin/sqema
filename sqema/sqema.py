# -*- coding: utf-8 -*-
"""Defines the Sqema class."""
# import json

# import pathlib
import os
from sqema.exceptions import NotAValidDefinitionError


from simqle import ConnectionManager

import pandas as pd
from yaml import safe_load

from logging import getLogger

logger = getLogger("sqema")


class Sqema:
    def __init__(self, sqema, cm):
        """
        Initialise a Sqema Instance.

        Sqema will set up your production, development and test database configurations.

        args:
         - cm: a Connection Manager
         - sqema_file: the file that defines the database structure
        """
        logger.info(f"Creating Sqema instance.")

        self.cm = cm
        self.definition = sqema

        self.mode = os.getenv("SIMQLE_MODE", "development")
        logger.info(f"Sqema mode set to {self.mode}")

        self.setup_environment()

    def setup_environment(self):
        """Set up the SQL environment using the sqema_file."""
        for database in self.definition["databases"]:
            self.setup_database(database)

    def setup_database(self, database):
        """Setup a database from a sqema database dictionary."""
        logger.info(f"Setting up Database {database['name']}")

        for schema in database["schemas"]:
            self.setup_schema(schema, conn=database["name"])

    def setup_schema(self, schema, conn):
        """Setup a schema from a schema dictionary."""
        logger.info(f"Setting up Schema {schema['name']}")

        # Config
        for config in schema["config"]:
            self.create_object(config, conn)

        # Tables
        for table in schema["tables"]:
            self.create_object(table, conn)
            self.insert_data(table, conn, schema=schema["name"])

        # Views
        for view in schema["views"]:
            self.create_object(view, conn)

        # Other. Use for objects like procedures or triggers
        for other in schema["others"]:
            self.create_object(other, conn)

    @staticmethod
    def get_sql(definition):
        """
        Return the sql definition text from an object.

        Definitions can be given as a str or a file.
        """
        if definition["type"] == "sql":
            return definition["sql"]
        elif definition["type"] == "file":
            with open(definition["path"], "r") as def_file:
                return def_file.read()
        else:
            raise NotAValidDefinitionError

    def create_object(self, obj, conn):
        """Create an object from its definition."""
        obj_name = obj.get("name", "unknown")
        logger.info(f"Creating object called {obj_name}")

        # Create the object from its definition
        sql = self.get_sql(obj["definition"])
        self.cm.execute_sql(con_name=conn, sql=sql)

        # Execute each post definition
        for definition in obj.get("post_definitions", []):
            sql = self.get_sql(definition)
            logger.info(f"executing post definition for object {obj_name}")
            self.cm.execute_sql(con_name=conn, sql=sql)

    def insert_data(self, table, conn, schema):
        """Insert data to given table."""
        for data_set in table["data"]:
            if self.mode not in data_set["modes"]:
                continue

            logger.info(f"Inserting data to {table['name']}, {schema}")

            df = pd.read_csv(data_set["file"])
            con = self.cm.get_engine(conn)
            df.to_sql(
                name=table["name"],
                con=con,
                schema=schema,
                if_exists="append",
                index=False,
                chunksize=1000,
            )
