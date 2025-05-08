from datetime import timedelta, datetime
from core.content_manager import ContentManager
import random
import schedule
from time import sleep
import logging
import logging.config
import os
import sys
import json
from utils import get_file_data, custom_print


def main():
    manager = ContentManager("config.json")
    manager.post_content()


def main_task():
    main()

    # After the main task is done, schedule the next task
    schedule_next_task()


def schedule_next_task():
    # clear previous schedule
    schedule.clear()

    # Initialize the static variable on the first function call
    if not hasattr(schedule_next_task, "prev_offset_minutes"):
        setattr(schedule_next_task, "prev_offset_minutes", 0)

    config              = get_file_data("config.json")

    hour_interval       = int(config["hour_interval"])          or 0
    rand_hour_offset    = int(config["random_hour_offset"])     or 0
    rand_min_offset     = int(config["random_min_offset"])      or 0

    # Calculate the total interval in minutes, including the random offsets
    total_offset_minutes    =  random.randint(0, rand_hour_offset * 60) + random.randint(0, rand_min_offset)
    total_minutes_interval  = (hour_interval * 60) + total_offset_minutes - schedule_next_task.prev_offset_minutes
    schedule_next_task.prev_offset_minutes = total_offset_minutes

    # Compute the exact datetime for the next task
    next_run_time = datetime.now() + timedelta(minutes=total_minutes_interval)
    formatted_next_run_time = next_run_time.strftime('%Y-%m-%d %H:%M:%S')

    custom_print(f"Scheduled to run on {formatted_next_run_time}")

    schedule.every(total_minutes_interval).minutes.do(main_task)

def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "default",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": log_level,
        },
    }

    logging.config.dictConfig(logging_config)

if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Application started")
    # Run main() once initially
    main()

    # Start the process by scheduling the first task
    schedule_next_task()

    while True:
        schedule.run_pending()
        sleep(1)
