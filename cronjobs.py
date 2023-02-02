import os

from loguru import logger

import helper
from services.database_service import close_server_connection, create_server_connection, insert_recently_played
from services.spotify_service import get_recently_played

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", os.path.basename(__file__), ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)


def grab_recently_played():
    logger.info("start - grab recently played")
    old_cursors = helper.read_old_cursors()
    items, cursors = get_recently_played(old_cursors)
    if len(items) > 0:
        connection = create_server_connection()
        added, not_added = insert_recently_played(connection, items)
        logger.info(
            "\n{len_added} songs added\n{len_not_added} songs not added".format(
                len_added=len(added), len_not_added=len(not_added)
            )
        )
        close_server_connection(connection)
        helper.write_new_cursors(cursors)
    logger.info("end - grab recently played")
