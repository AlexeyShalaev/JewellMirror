import os
import sys
import schedule
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from Background.jobs.system import stop_system, start_system
from Background.jobs.data import manage_data

schedule.every().day.at("23:00").do(manage_data)
schedule.every().friday.at("12:00").do(stop_system)  # min start of shabbat
schedule.every().saturday.at("23:00").do(start_system)  # max end of shabbat

while True:
    schedule.run_pending()
    time.sleep(1)
