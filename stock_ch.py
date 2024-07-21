import fv_screener_processor


def extract_change(ticker_symbol):
    change = fv_screener_processor.ticker_change_dict[ticker_symbol]
    change = change.replace("%", "")
    return float(change)