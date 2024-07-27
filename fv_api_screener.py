from dotenv import load_dotenv
import os
import requests


def export_screener_data():
    # Define the base screener URL
    base_url = "https://elite.finviz.com/export.ashx"
    filters = "v=152&p=i1&f=cap_0.01to,geo_usa%7Cchina%7Cfrance%7Ceurope%7Caustralia%7Cbelgium%7Ccanada%7Cchinahongkong%7Cgermany%7Chongkong%7Ciceland%7Cjapan%7Cnewzealand%7Cireland%7Cnetherlands%7Cnorway%7Csingapore%7Csouthkorea%7Csweden%7Ctaiwan%7Cunitedarabemirates%7Cunitedkingdom%7Cswitzerland%7Cspain,sh_curvol_o100,sh_price_u50,sh_relvol_o2,ta_change_u&ft=4&o=sharesfloat&ar=10&c=0,1,2,5,6,25,26,27,28,29,30,84,45,50,51,68,60,61,63,64,67,65,66"


    # Load environment variables from .env file
    load_dotenv()
    
    # print(os.getenv("FINVIZ_API_TOKEN"))

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

if __name__ == "__main__":
    export_screener_data()
