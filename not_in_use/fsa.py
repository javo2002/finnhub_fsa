import finnhub
finnhub_client = finnhub.Client(api_key="cpmethpr01quf620vds0cpmethpr01quf620vdsg")

print(finnhub_client.company_news('AAPL', _from="2024-06-01", to="2024-06-10"))
