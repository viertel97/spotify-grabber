import json
import os
from datetime import datetime

from loguru import logger

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)


def get_config(file_path):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/config/", file_path), encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_value(value, row, config):
    return next(i for i in config if i[row] == value)


CURSORS_FILE_PATH = os.path.join("data", "cursors.txt")


def unix_to_date(ts):
    return datetime.utcfromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S")


def read_old_cursors():
    try:
        cursors = json.load(open(CURSORS_FILE_PATH))
        if cursors:
            logger.info("READ: " + str(cursors))
            logger.info(
                "READ:\nafter: {after}\nbefore: {before}".format(
                    after=unix_to_date(int(cursors["after"])), before=unix_to_date(int(cursors["before"]))
                )
            )
            return cursors
        else:
            logger.error("Datei ist leer: " + CURSORS_FILE_PATH)
            return None
    except json.JSONDecodeError:
        logger.error("Datei ist leer: " + CURSORS_FILE_PATH)
        return None
    except FileNotFoundError:
        logger.error("Datei nicht gefunden: " + CURSORS_FILE_PATH)
        return None


def write_new_cursors(cursors):
    logger.info("WRITE:" + str(cursors))
    logger.info(
        "WRITE:\n after: {after}\n before: {before}".format(
            after=unix_to_date(int(cursors["after"])), before=unix_to_date(int(cursors["before"]))
        )
    )
    json.dump(cursors, open(CURSORS_FILE_PATH, "w+"))
