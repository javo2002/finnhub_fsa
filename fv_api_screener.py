import requests
import time
import schedule
from datetime import datetime


def export_screener_data():
    # Define the base screener URL and API token
    base_url = "https://elite.finviz.com/export.ashx"
    filters = "v=111&f=sh_curvol_o2000,sh_relvol_o5&ft=4&ar=60"
    auth_token = "475d27c7-997a-45f9-b8be-c668eb0482d5"

    # Construct the full URL
    url = f"{base_url}?{filters}&auth={auth_token}"

    # Make the request to the constructed URL
    response = requests.get(url)

    # Write the content to a CSV file
    with open("screener.csv", "wb") as file:
        file.write(response.content)

    print("Exported data to screener.csv")


def job():
    export_screener_data()
    schedule.every(1).minutes.do(export_screener_data)


# Schedule the job to start at 07:00:00
schedule.every().day.at("10:27:10").do(job)

# Keep the script running and stop at 10:00:00
while True:
    current_time = datetime.now().time()
    if current_time >= datetime.strptime("20:00:00", "%H:%M:%S").time():
        print(" Screener.csv stopped updating at 10:00:00")
        break
    schedule.run_pending()
    time.sleep(1)
