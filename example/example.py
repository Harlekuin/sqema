from sqema import Sqema
from simqle import ConnectionManager

from logging import getLogger, StreamHandler
from yaml import safe_load


logger = getLogger("sqema")
logger.addHandler(StreamHandler())
logger.setLevel("DEBUG")

sql_logger = getLogger("simqle")
sql_logger.addHandler(StreamHandler())
sql_logger.setLevel("DEBUG")

cm = ConnectionManager("./.connections.yaml")

with open("./sqema.yaml", "r") as sqema_file:
    sqema = safe_load(sqema_file.read())

sq = Sqema(sqema=sqema, cm=cm)

sql = """
    select *
    from vHighScores
    """

rst = cm.recordset(
    con_name="sqlite-db",
    sql=sql
)

print(rst.headings, rst.data)

sql = """
    select type, name, tbl_name, sql
    FROM sqlite_master
    WHERE type='index'
    """

rst = cm.recordset(
    con_name="sqlite-db",
    sql=sql
)

print(rst.headings, rst.data)
