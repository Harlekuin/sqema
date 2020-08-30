from sqema import Sqema
from simqle import ConnectionManager
import os

try:
    os.remove("/tmp/prod-database.db")
except OSError:
    pass

cm = ConnectionManager("./features/general-test/.connections.yaml")
sqema_dir = "./features/general-test/sqema"

my_sqema = Sqema(cm, sqema_dir)

my_sqema.ensure_sql_environment()


sql = "select * from main.MyTable"

print(cm.recordset(con_name="my-sqlite-database", sql=sql))
