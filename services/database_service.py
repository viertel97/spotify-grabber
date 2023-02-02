import os

import pymysql.cursors
from loguru import logger
from quarter_lib.config import get_target, get_secrets

CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN = get_secrets(
    ['microsoft/client_id', 'microsoft/client_secret', 'microsoft/refresh_token'])

DB_USERNAME, DB_HOST, DB_PASSWORD, DB_PORT, DB_NAME = get_target("private")

COLUMNS = ["track_album_uri", "track_uri", "context_uri", "played_at"]
COLUMNS_WITHOUT_CONTEXT = ["track_album_uri", "track_uri", "played_at"]

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)


def create_server_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=int(DB_PORT),
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
    )


def close_server_connection(connection):
    connection.close()


def insert_recently_played(connection, items):
    not_added_tuples = []
    tuples = generate_sql_tuples(items)
    if len(tuples) > 0:
        for tuple in tuples:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO spotify (track_album_uri, track_uri, context_uri, played_at) values (%s,%s,%s,%s)",
                        tuple,
                    )
                    connection.commit()
            except pymysql.err.IntegrityError as e:
                logger.error("IntegrityError: {error}".format(error=e))
                not_added_tuples.append(tuple)
                continue
    return list(set(tuples).symmetric_difference(set(not_added_tuples))), not_added_tuples


def generate_sql_tuples(items):
    tuple_list = []
    for item in items:
        if "context_uri" in item.keys():
            tuple_list.append(
                (
                    item["track_album_uri"],
                    item["track_uri"],
                    item["context_uri"],
                    item["played_at"],
                )
            )
        else:
            tuple_list.append(
                (
                    item["track_album_uri"],
                    item["track_uri"],
                    None,
                    item["played_at"],
                )
            )
    return tuple_list
