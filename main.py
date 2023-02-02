import os

from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger

import cronjobs

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)

if __name__ == "__main__":
    cronjobs.grab_recently_played()
    if not os.name == "nt":
        scheduler = BlockingScheduler()

        scheduler.add_job(
            cronjobs.grab_recently_played,
            "interval",
            minutes=25,
            id="grab_recently_played",
        )
        logger.info("jobs: \n")
        jobs = scheduler.get_jobs()
        for job in jobs:
            logger.info("    %s" % job)
        logger.info("start scheduler")
        scheduler.start()
