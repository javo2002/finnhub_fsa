import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def visualize_correlation(file):
    # Load the expanded CSV file

    data = pd.read_csv(file)

    # Define the threshold values for sentiment
    body_threshold = 0  # Adjust as necessary
    trend_threshold = 0  # Adjust as necessary

    # Scatter plot with quadrants and colored points
    plt.figure(figsize=(10, 6))

    # Plot scatter points in black
    scatter = sns.scatterplot(x='Body Sentiment', y='Trend Sentiment', data=data, color='black', edgecolor='k', s=100,
                              legend=False)

    # Define the quadrant boundaries
    plt.axhline(trend_threshold, color='black', linewidth=1.5)
    plt.axvline(body_threshold, color='black', linewidth=1.5)

    # Annotate points with Body Sentiment and Trend Sentiment values
    for index, row in data.iterrows():
        plt.annotate(f"{row['Quote']}",
                     (row['Body Sentiment'], row['Trend Sentiment']),
                     textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8, color='blue')

    # Add quadrant names
    plt.text(body_threshold + 0.8, trend_threshold + 0.8, 'Optimistic\n1', fontsize=15, ha='center', va='bottom',
             alpha=0.5)
    plt.text(body_threshold + 0.8, trend_threshold - 0.8, 'Conflicted\n2', fontsize=15, ha='center', va='top',
             alpha=0.5)
    plt.text(body_threshold - 0.8, trend_threshold + 0.8, 'Contrarian\n3', fontsize=15, ha='center', va='bottom',
             alpha=0.5)
    plt.text(body_threshold - 0.8, trend_threshold - 0.8, 'Pessimistic\n4', fontsize=15, ha='center', va='top',
             alpha=0.5)

    # Add titles and labels
    plt.title('Sentiment Analysis of Financial Stocks')
    plt.xlabel('Article Sentiment')
    plt.ylabel('Stock Trend Sentiment')
    plt.grid(True)

    # Set axis limits for better visualization
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)

    plt.tight_layout()
    return plt.show()

'''
Quadrant 1
+ Body Sentiment, + Stock Trend Sentiment: Optimistic:
Reason: Both the sentiment about the news (body sentiment) and the stock trend are positive, indicating general optimism and confidence in the stock's performance.

Quadrant 2
+ Body Sentiment, - Stock Trend Sentiment: Conflicted:
Reason: Positive news sentiment but a declining stock trend suggests a conflict between the news and market behavior, indicating uncertainty or mixed reactions from investors.

Quadrant 3
- Body Sentiment, + Stock Trend Sentiment: Contrarian:
Reason: Negative news sentiment but a rising stock trend suggests contrarian behavior, where investors are betting against the prevailing negative news.

Quadrant 4
- Body Sentiment, - Stock Trend Sentiment: Pessimistic:
Reason: Both the news sentiment and the stock trend are negative, reflecting overall pessimism and lack of confidence in the stock's future performance.
'''
