import schedule
import time
import subprocess
from datetime import datetime


def run_fv_api_screener():
    # Run fv_api_screener.py
    subprocess.run(['python3', 'fv_api_screener.py'])


def run_centralizer():
    # Run centralizer.py
    subprocess.run(['python3', 'centralizer.py'])


def run_logger():
    # Run centralizer.py
    subprocess.run(['python3', 'logger.py'])


def job1():
    run_fv_api_screener()
    schedule.every(1).minutes.do(run_fv_api_screener)


def job2():
    run_centralizer()
    schedule.every(1).minutes.do(run_centralizer)


def job3():
    run_logger()
    schedule.every(1).minutes.do(run_logger)


# Schedule the jobs to start at specific times
schedule.every().day.at("20:39:40").do(job1)
schedule.every().day.at("07:32:05").do(job2)
schedule.every().day.at("07:32:25").do(job3)

# Keep the script running and stop at 10:00:00
while True:
    current_time = datetime.now().time()
    if datetime.strptime("10:00:00", "%H:%M:%S").time() <= current_time <= datetime.strptime("10:01:00",
                                                                                             "%H:%M:%S").time():
        print("Jobs stopped updating at 10:00:00")
        break  # Sleep for a minute before checking the time again
    else:
        schedule.run_pending()
        time.sleep(1)
