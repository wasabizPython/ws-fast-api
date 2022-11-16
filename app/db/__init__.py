import logging

import pymysql
from decouple import config

logger = logging.getLogger(config('LOG_NAME'))


class Database:
    def __init__(self, ws_id: str):
        self.ws_id = ws_id
        self.conn = None

        self.__create_conn__()

    def __create_conn__(self):
        """
        create database connection
        :return:
        """
        try:
            logger.info(
                f'{self.ws_id} - established database connection {config("DB_HOST")}:{config("DB_PORT")}')
            self.conn = pymysql.connect(
                host=config("DB_HOST"),
                port=int(config("DB_PORT")),
                user=config("DB_USERNAME"),
                password=config("DB_PASSWORD"),
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as e:
            logger.error(f'{self.ws_id} - {e}', exc_info=True)

    def select(self, sql: str, value: [str, tuple], fetch_all=False):
        """
        select database query
        :param fetch_all:
        :param sql:
        :param value:
        :return:
        """
        logger.info(f"{self.ws_id} - {sql}")
        with self.conn.cursor() as cursor:
            cursor.execute(sql, value)
            if fetch_all:
                return cursor.fetchall()
            else:
                return cursor.fetchone()

    def update(self, sql: str, value: [str, tuple]) -> None:
        """
        update database query
        :param value:
        :param sql:
        :return:
        """
        with self.conn.cursor() as cursor:
            logger.info(f"{self.ws_id} - {sql}")
            cursor.execute(sql, value)
            self.conn.commit()
        logger.info(
            f"{self.ws_id} - {self.conn.cursor().rowcount} record updated")

    def insert(self, sql: str, value: [str, tuple]) -> None:
        """
        insert database query
        :param value:
        :param sql:
        :return:
        """
        with self.conn.cursor() as cursor:
            logger.info(f"{self.ws_id} - {sql}")
            cursor.execute(sql, value)
            self.conn.commit()
        logger.info(
            f"{self.ws_id} - {self.conn.cursor().rowcount} record inserted")

    def close(self) -> None:
        """
        close database connection
        :return:
        """
        try:
            self.conn.close()
        except Exception as e:
            logger.error(f'{self.ws_id} - {e}', exc_info=True)
