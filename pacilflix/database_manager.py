# Database Connection Manager

import psycopg2
import psycopg2.extras
import environ

# Reference : https://www.psycopg.org/docs/usage.html

env = environ.Env()
environ.Env.read_env('.env')


class DatabaseManager:
    connection = psycopg2.connect(
        user=env('DB_USER'),
        password=env('DB_PASS'),
        host=env('DB_HOST'),
        port=env('DB_PORT'),
        dbname=env('DB_NAME')
    )

    def get_cursor():
        print('get_cursor')
        return DatabaseManager.connection.cursor()

    def get_dict_cursor():
        return DatabaseManager.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def commit():
        DatabaseManager.connection.commit()

    def rollback():
        DatabaseManager.connection.rollback()
