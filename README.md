# Finnhub Financial Sentiment Analysis

## Project Overview

This project is designed to perform comprehensive financial sentiment analysis using data from a finviz financial API. The primary goal is to analyze stock sentiment and visualize the results to aid in making informed investment decisions. The project includes several scripts that handle data retrieval, processing, sentiment analysis, and visualization.

## Repository Structure

- **Scripts:**
  - `fv_api_screener.py`: Script to screen financial data using API.
  - `fv_screener_processor.py`: Processor for handling the screened financial data.
  - `main_finviz.py`: Main script integrating various components for Finviz data analysis.
  - `sentiment.py`: Script for performing sentiment analysis on financial news data.
  - `stock_ch.py`: Script retrieve stock changes from screener script.
  - `visual.py`: Script to visualize the financial sentiment analysis results.
- **Data Files:**
  - `screener.csv`: CSV file containing screened financial data.
  - `news_data_with_sentiments.csv`: CSV file containing financial news data with sentiment analysis results.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/javo2002/finnhub_fsa.git
cd finnhub_fsa
```

### 2. Install Required Packages
```bash
pip install -r requirements.txt
```

## Usage

### 1. Configure API Key and Screener in `fv_api_screener.py`
- Open `fv_api_screener.py`.
- Input your API key in the designated variable.
- Configure the screener settings according to your needs.
- Update the scheduling times to define when the screener should run.

### 2. Run the Screener
```bash
python fv_api_screener.py
```

### 3. Process Screened Data (Optional)
- Execute `fv_screener_processor.py` to view the processed financial data.
```bash
python fv_screener_processor.py
```

### 4. Configure Dates in `main_finviz.py`
- Open `main_finviz.py`.
- Input the desired start and end dates for your analysis in correct format.

### 5. Run the Main Script
- This integrates various components such as `fv_screener_processor.py`, `stock_ch.py`, `sentiment.py`, and `visual.py`, to performs the primary data analysis.
```bash
python main_finviz.py
```

### 6. Final Analysis
- View **news_data_with_sentiments.csv:** and graph to inspect analyze results


## Data Files

- **screener.csv:** Contains the screened financial data.
- **news_data_with_sentiments.csv:** Contains financial news data along with sentiment analysis results.

## Advanced Configuration

### Customizing Sentiment Analysis
In `sentiment.py`, you can customize the sentiment analysis parameters to better suit your needs. This includes adjusting the sentiment thresholds and integrating additional sentiment analysis tools.

### Visualization Settings
In `visual.py`, you can configure various visualization settings to enhance the graphical representation of your data. This includes setting specific colors, labels, and plotting styles.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact Javo at [javi22.college@gmail.com](mailto:jnw5354@psu.edu).

---

Feel free to provide additional details or specific enhancements you would like included in the README.
