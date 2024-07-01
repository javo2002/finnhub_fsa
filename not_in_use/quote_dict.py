from collections import defaultdict
import re

def stock_dict(dict):
    return dict

stock_dict_yahoo_finance = {
    # Technology
    'AAPL': {'apple': 10, 'iphone': 9, 'mac': 8, 'ipad': 7, 'tim cook': 6, 'ios': 5, 'apple watch': 5, 'macbook': 7, 'app store': 4, 'siri': 3},
    'GOOGL': {'google': 10, 'alphabet': 9, 'android': 8, 'search': 7, 'larry page': 6, 'sergey brin': 6, 'sundar pichai': 6, 'chrome': 5, 'gmail': 5, 'youtube': 5},
    'MSFT': {'microsoft': 10, 'windows': 9, 'azure': 8, 'office': 7, 'satya nadella': 6, 'xbox': 6, 'surface': 5, 'microsoft office': 7, 'outlook': 5, 'onedrive': 4},
    'AMZN': {'amazon': 10, 'aws': 9, 'prime': 8, 'jeff bezos': 6, 'andy jassy': 6, 'echo': 5, 'kindle': 5, 'alexa': 5, 'amazon prime': 7, 'amazon web services': 8},
    'META': {'facebook': 10, 'meta': 9, 'mark zuckerberg': 8, 'instagram': 7, 'whatsapp': 6, 'oculus': 5, 'facebook messenger': 5, 'meta platforms': 6},
    'NVDA': {'nvidia': 10, 'nvda': 9, 'geforce': 8, 'gpu': 7, 'jen-hsun huang': 6, 'graphics card': 6, 'rtx': 5, 'quadro': 5},

    # Financials
    'JPM': {'jpmorgan': 10, 'chase': 9, 'jamie dimon': 8, 'jpm': 7, 'jp morgan chase': 8, 'investment bank': 5, 'jpmorgan chase': 8},
    'GS': {'goldman': 10, 'sachs': 9, 'david solomon': 8, 'gs': 7, 'goldman sachs': 8, 'investment banking': 7, 'goldman sachs group': 7},
    'MS': {'morgan stanley': 10, 'james gorman': 8, 'ms': 7, 'investment management': 7, 'morgan stanley wealth management': 6},
    'BAC': {'bank of america': 10, 'bofa': 9, 'brian moynihan': 8, 'bac': 7, 'banking': 5, 'bank of america corporation': 7},
    'C': {'citigroup': 10, 'citi': 9, 'jane fraser': 8, 'c': 7, 'citibank': 7, 'citi group': 7, 'citigroup inc': 7},
    'WFC': {'wells fargo': 10, 'wfc': 9, 'wells fargo & co': 8, 'wells fargo bank': 7},
    'USB': {'us bancorp': 10, 'usb': 9, 'u.s. bancorp': 8, 'us bank': 7, 'u.s. bank': 7},
    'TFC': {'truist financial': 10, 'tfc': 9, 'bb&t': 7, 'suntrust': 7, 'truist bank': 8},
    'PNC': {'pnc financial': 10, 'pnc': 9, 'pnc bank': 8, 'pnc financial services': 7},
    'BK': {'bank of new york mellon': 10, 'bk': 9, 'bny mellon': 8, 'the bank of new york mellon corporation': 7},
    'SCHW': {'charles schwab': 10, 'schw': 9, 'schwab': 8, 'charles schwab corporation': 7},
    'BLK': {'blackrock': 10, 'blk': 9, 'black rock': 8, 'blackrock inc': 7, 'larry fink': 7},

    # Healthcare
    'JNJ': {'johnson & johnson': 10, 'jnj': 9, 'johnson and johnson': 8, 'pharmaceutical': 5, 'healthcare': 5},
    'PFE': {'pfizer': 10, 'pfe': 9, 'vaccine': 8, 'albert bourla': 7, 'pharmaceutical': 5, 'covid-19 vaccine': 6},
    'MRK': {'merck': 10, 'mrk': 9, 'pharmaceutical': 5, 'kenilworth': 4, 'medicine': 5, 'merck & co': 7},
    'ABBV': {'abbvie': 10, 'abbv': 9, 'pharmaceutical': 5, 'research-based biopharmaceutical company': 6},
    'LLY': {'eli lilly': 10, 'lly': 9, 'pharmaceutical': 5, 'healthcare': 5, 'eli lilly and company': 7},
    'GILD': {'gilead': 10, 'gild': 9, 'gilead sciences': 8, 'biopharmaceutical': 6, 'healthcare': 5},
    'BMY': {'bristol-myers': 10, 'bmy': 9, 'bristol-myers squibb': 8, 'pharmaceutical': 6, 'healthcare': 5},

    # Consumer Discretionary
    'TSLA': {'tesla': 10, 'elon musk': 9, 'model s': 8, 'model 3': 8, 'model x': 8, 'model y': 8, 'electric vehicle': 7, 'ev': 6},
    'NKE': {'nike': 10, 'nke': 9, 'swoosh': 8, 'sportswear': 7, 'athletic': 6, 'footwear': 5},
    'MCD': {'mcdonald\'s': 10, 'mcd': 9, 'fast food': 8, 'restaurant': 7, 'big mac': 6, 'mcnuggets': 6},
    'SBUX': {'starbucks': 10, 'sbux': 9, 'coffee': 8, 'cafe': 7, 'latte': 6, 'frappuccino': 6},

    # Industrials
    'BA': {'boeing': 10, 'ba': 9, 'aerospace': 8, 'aircraft': 7, 'defense': 6, 'boeing company': 6},
    'CAT': {'caterpillar': 10, 'cat': 9, 'heavy equipment': 8, 'construction': 7, 'machinery': 7, 'caterpillar inc': 6},
    'GE': {'general electric': 10, 'ge': 9, 'energy': 8, 'industrial': 7, 'ge power': 6, 'ge renewable energy': 6},

    # Energy
    'XOM': {'exxon': 10, 'mobil': 9, 'exxonmobil': 9, 'xom': 8, 'oil': 7, 'gas': 7, 'energy': 6},
    'CVX': {'chevron': 10, 'cvx': 9, 'oil': 8, 'gas': 8, 'energy': 7, 'chevron corporation': 6},
    'COP': {'conocophillips': 10, 'cop': 9, 'oil': 8, 'gas': 8, 'energy': 7, 'conoco phillips': 6},

    # Utilities
    'DUK': {'duke energy': 10, 'duk': 9, 'electricity': 8, 'utilities': 7, 'power': 6, 'energy': 5},
    'SO': {'southern company': 10, 'so': 9, 'utilities': 8, 'energy': 7, 'power': 7, 'electricity': 6},
    'NEE': {'nextera energy': 10, 'nee': 9, 'electricity': 8, 'utilities': 7, 'power': 7, 'energy': 6},

    # Real Estate
    'AMT': {'american tower': 10, 'amt': 9, 'real estate': 8, 'reit': 7, 'wireless infrastructure': 6},
    'PLD': {'prologis': 10, 'pld': 9, 'real estate': 8, 'reit': 7, 'logistics': 6, 'warehousing': 6},
    'CCI': {'crown castle': 10, 'cci': 9, 'real estate': 8, 'reit': 7, 'wireless infrastructure': 6},

    # Consumer Staples
    'PG': {'procter & gamble': 10, 'pg': 9, 'consumer goods': 8, 'household products': 7, 'procter and gamble': 7},
    'KO': {'coca-cola': 10, 'ko': 9, 'beverage': 8, 'soft drink': 7, 'coke': 7, 'coca cola company': 6},
    'PEP': {'pepsico': 10, 'pep': 9, 'beverage': 8, 'snacks': 7, 'pepsi': 7, 'pepsico inc': 6},

    # Telecommunications
    'VZ': {'verizon': 10, 'vz': 9, 'telecommunications': 8, 'wireless': 7, 'broadband': 7, 'verizon communications': 6},
    'T': {'at&t': 10, 't': 9, 'telecommunications': 8, 'wireless': 7, 'broadband': 7, 'at&t inc': 6},
    'TMUS': {'t-mobile': 10, 'tmus': 9, 'telecommunications': 8, 'wireless': 7, 'broadband': 7, 't mobile us': 6},

    # Materials
    'LIN': {'linde': 10, 'lin': 9, 'industrial gases': 8, 'chemicals': 7, 'linde plc': 6},
    'APD': {'air products': 10, 'apd': 9, 'industrial gases': 8, 'chemicals': 7, 'air products and chemicals': 6},
    'SHW': {'sherwin-williams': 10, 'shw': 9, 'paint': 8, 'coatings': 7, 'chemicals': 6, 'sherwin williams company': 6},

    # Pharmaceuticals
    'RHHBY': {'roche': 10, 'rhhby': 9, 'pharmaceutical': 8, 'biotechnology': 7, 'healthcare': 6, 'roche holding ag': 6},
    'NVS': {'novartis': 10, 'nvs': 9, 'pharmaceutical': 8, 'biotechnology': 7, 'healthcare': 6, 'novartis ag': 6},
    'SNY': {'sanofi': 10, 'sny': 9, 'pharmaceutical': 8, 'biotechnology': 7, 'healthcare': 6, 'sanofi sa': 6}
}

stock_dict_output = stock_dict(stock_dict_yahoo_finance)

#
# def guess_stock(headline, stock_dict):
#     headline = headline.lower()
#     scores = defaultdict(int)
#
#     for stock, keywords in stock_dict.items():
#         print(keywords.items())
#         for keyword, weight in keywords.items():
#             if keyword in headline and re.search(r'\b' + re.escape(keyword) + r'\b', headline, re.IGNORECASE):
#                 scores[stock] += weight
#
#     if scores:
#         # Return the stock with the highest score
#         return max(scores, key=scores.get)
#     else:
#         return None
#
#
# # Example usage
# headline = "Prediction: This Will Be t pg linde Wall Street's First $5 Trillion Stock"
# guessed_stock = guess_stock(headline, stock_dict_yahoo_finance)
# print(f"Guessed Stock: {guessed_stock}")
