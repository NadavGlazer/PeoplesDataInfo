import psycopg2
from psycopg2 import pool, extras
import yaml
import logging


class PostgresApi():
    def __init__(self) -> None:
       
        yaml_file = open("postgresConnection.yaml", encoding="utf-8")
        connection_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
        self.postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(
            1,
            5,
            user=connection_data["user"],
            password=connection_data["password"],
            host=connection_data["host"],
            port=connection_data["port"],
            database=connection_data["database"]
        )

        if self.postgreSQL_pool:
            logging.info("Connection pool created successfully")
    
    def execute_query(self, query):
        ps_connection = self.postgreSQL_pool.getconn()
        ps_connection.autocommit = True

        try:
            with ps_connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as ps_cursor:
                ps_cursor.execute(query)
                try:
                    return ps_cursor.fetchall()
                except:
                    pass
                
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error("Error while connecting to PostgreSQL", error)    
        finally:
            self.postgreSQL_pool.putconn(ps_connection)

