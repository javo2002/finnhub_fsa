from dotenv import load_dotenv
import os
import requests
import time
import schedule
from datetime import datetime


def export_screener_data():
    # Define the base screener URL
    base_url = "https://elite.finviz.com/export.ashx"
    filters = "v=152&p=i1&f=cap_0.01to,geo_usa|china|france|europe|australia|belgium|canada|chinahongkong|germany|hongkong|iceland|japan|newzealand|ireland|netherlands|norway|singapore|southkorea|sweden|taiwan|unitedarabemirates|unitedkingdom|switzerland|spain,sh_curvol_o100,sh_price_u50,sh_relvol_o2,ta_change_u&ft=4&o=sharesfloat&r=81&ar=10"


    # Load environment variables from .env file
    load_dotenv()

    # Access the environment variable
    auth_token = os.getenv("FINVIZ_API_TOKEN")
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
schedule.every().day.at("7:00:00").do(job)

# Keep the script running and stop at 12:00:00
while True:
    current_time = datetime.now().time()
    if current_time >= datetime.strptime("12:00:00", "%H:%M:%S").time():
        print(" Screener.csv stopped updating at 12:00:00")
        break
    schedule.run_pending()
    time.sleep(1)
