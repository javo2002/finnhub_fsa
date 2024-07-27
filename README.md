# Finviz Financial Sentiment Analysis

## Project Overview

This project is designed to perform comprehensive financial sentiment analysis using data from a finviz financial API. The primary goal is to analyze stock sentiment and visualize the results to aid in making informed investment decisions. The project includes several scripts that handle data retrieval, processing, sentiment analysis, and visualization.

## Repository Structure

- **Scripts:**
  - `main.py`: Script that runs `fv_api_screener.py`, `centralizer.py` and `logger.py` on scheduled times for automation of processes and real-time data retreval.
  - `fv_api_screener.py`: Script to screen financial data using API.
  - `fv_screener_processor.py`: Processor for handling the screened financial data.
  - `centralizer.py`: Main script integrating various components for Finviz data analysis.
  - `sentiment.py`: Script for performing sentiment analysis on financial news data.
  - `stock_ch.py`: Script retrieve stock changes from screener script.
  - `visual.py`: Script to visualize the financial sentiment analysis results.
  - `logger.py`: Logs the sentiment data to a file for later analysis.
- **Data Files:**
  - `screener.csv`: CSV file containing screened financial data.
  - `news_data_with_sentiments.csv`: CSV file containing financial news data with sentiment analysis results.
  - `sentiment_analysis.log`: .log file that will keep track of sentiment scores through the duration of execution
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
- It is recommended to install through the terminal so if any errors occur, a detailed explanation of the issue is explained. Here are some solutions to reoccuring issues when setting up projects
  - ```bash
    pip install --upgrade setuptools wheel
    pip install python-dotenv
    ```
### 3. Supporting Code Indications
  - Throughout the code there will be commented out print functions that will help aid in understanding where the code might have gone wrong

## Usage

### 1. Input API Key into `.env` file
- Open `.env`.
- Input your API key in the designated variable.
  
### 2. Configure `fv_api_screener.py`
- Open `fv_api_screener.py`.
- Configure the screener settings according to your needs.
- Update the scheduling times to define when the screener should run.

### 3. Run `fv_api_screener` (Optional)
- Execute `fv_api_screener.py` to ensure that the script exports the screened data.
```bash
python fv_api_screener.py
```
- You may need to uncomment printing the API token to ensure that it is fetched

### 4. Run `fv_screener_processor.py` to Process Screened Data (Optional)
- Open `fv_screener_processor.py`
- Execute `fv_screener_processor.py` to view the processed financial data.
```bash
python fv_screener_processor.py
```

### 5. Configure Dates in `centralizer.py`
- This script integrates other functional scripts such as `fv_screener_processor.py`, `stock_ch.py`, `sentiment.py`, and `visual.py`, to centralize the data for analysis and visualization.
- Open `centralizer.py`.
- Input the desired start and end dates for your analysis in correct format.

### 6. Run `centralizer.py` (Optional)
- Execute `centralizer.py` to ensure proper analysis and visualization can be achieved.
```bash
python centralizer.py
```

### 7.Configure Scheduled and Incremental Loop Times in `main.py`
- Before finalizing scheduled times, configure for execution to be done within the next few minutes to ensure that the script will begin on time
- Ensure that jobs are not scheduled to run at same times, as the order in which data should be recieved will result in failure if executed in the wrong order
  - Tip: Recommended executions should be (job1 -> initial time, job2 -> +3 seconds after job1, job3 -> +15 seconds after job2)

### 8. Run `main.py`
- Make sure that your computer is running and is connected to a power source for optimal connectivity. Failure to maintain connection will break the pending code.
```bash
python main.py
```

### 9. Final Analysis
- View **news_data_with_sentiments.csv:** and graph to inspect analyze results

### 10. Compare Sentiment Tools (Optional)
- Starting sentiment analyzer in use is NLTK
- To switch to finVader change `from sentiment_nltk import body_sentiment, stock_statistical_values` in `main_finviz.py` to `from sentiment_finVader import body_sentiment, stock_statistical_values`

### 11. Analyze Logger
- Utilize the search command to target specific dates or tickers
  - Time example: "2024-07-27 19:45:34"
  - Ticker search example: "TSLA"

## Data Files

- **screener.csv:** Contains the screened financial data.
- **news_data_with_sentiments.csv:** Contains financial news data along with sentiment analysis results.

## Advanced Configuration

### Customizing Sentiment Analysis
In `sentiment.py`, you can customize the sentiment analysis parameters to better suit your needs. This includes adjusting the sentiment thresholds and integrating additional sentiment analysis tools.

### Visualization Settings
In `visual.py`, you can configure various visualization settings to enhance the graphical representation of your data. This includes setting specific colors, labels, and plotting styles.

### Customizing Logger Output
In `Logger.py`, you can customize the way data is retrieved from `news_data_with_sentiments.csv` for narrowing down on the retrieved data. This can aid in later analysis and cooperative analysis.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact creator at [jnw5354@psu.edu](mailto:jnw5354@psu.edu).

---

Feel free to provide additional details or specific enhancements you would like included in the README.
