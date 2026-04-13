import pymysql
from flask import g
from pymysql.cursors import DictCursor


class MySQL:
    def init_app(self, app):
        self.app = app
        app.teardown_appcontext(self.teardown)

    def connect(self):
        return pymysql.connect(
            host=self.app.config["MYSQL_HOST"],
            user=self.app.config["MYSQL_USER"],
            password=self.app.config["MYSQL_PASSWORD"],
            db=self.app.config["MYSQL_DB"],
            cursorclass=DictCursor,
            charset="utf8mb4",
            autocommit=False,
        )

    @property
    def connection(self):
        if "mysql_connection" not in g:
            g.mysql_connection = self.connect()
        return g.mysql_connection

    def teardown(self, exception):
        conn = g.pop("mysql_connection", None)
        if conn is not None:
            conn.close()


mysql = MySQL()
