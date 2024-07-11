import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def visualize_correlation(file):
    # Load the expanded CSV file

    data = pd.read_csv(file)

    # Display the first few rows and summary statistics of the data
    print(data.head())

    # Define the threshold values for sentiment
    body_threshold = 0  # Adjust as necessary
    trend_threshold = 0  # Adjust as necessary

    # Define the colormap and normalization for volatility
    volatility_min = 0
    volatility_max = 1
    norm = plt.Normalize(volatility_min, volatility_max)

    # Map volatility to colors from red (low) to green (high) by reversing the colormap
    colors = plt.cm.RdYlGn_r(norm(data['Volatility']))  # '_r' reverses the colormap

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
        plt.annotate(f"({row['Body Sentiment']:.2f}, {row['Trend Sentiment']:.2f})",
                     (row['Body Sentiment'], row['Trend Sentiment']),
                     textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8, color='blue')

    # Add colorbar
    num_ticks = 11  # Number of ticks, including endpoints
    volatility_ticks = np.linspace(volatility_min, volatility_max, num=num_ticks)

    sm = plt.cm.ScalarMappable(cmap='RdYlGn_r', norm=norm)  # Use RdYlGn_r for reversed colormap
    sm.set_array([])
    cb = plt.colorbar(sm, ax=plt.gca(), ticks=volatility_ticks, label='Volatility',
                      alpha=0.5)  # Set alpha to 0.5 for transparency

    # Add line indicating volatility on the colorbar
    volatility_value = data['Volatility'].values[0]

    if volatility_value > 1:
        volatility_value = 1  # Cap volatility at 1 for display purposes
        cb.ax.axhline(volatility_value, color='black', linestyle='-',
                      linewidth=2)  # Adjust color, linestyle, and linewidth
        cb.ax.annotate(f'{volatility_value:.0f}+', xy=(0, volatility_value), xytext=(-4.8, 0),
                       textcoords='offset points',
                       va='center', ha='right', fontsize=10, color='blue',
                       bbox=dict(boxstyle='round,pad=0.3', fc='gray', alpha=0.3))
    else:
        cb.ax.axhline(volatility_value, color='black', linestyle='-',
                      linewidth=2)  # Adjust color, linestyle, and linewidth
        cb.ax.annotate(f'{volatility_value:.2f}', xy=(0, volatility_value), xytext=(-4.8, 0),
                       textcoords='offset points',
                       va='center', ha='right', fontsize=10, color='blue',
                       bbox=dict(boxstyle='round,pad=0.3', fc='gray', alpha=0.3))

    # Add labels to the colorbar ends
    cb.ax.text(1.05, 1.05, 'High Risk', va='bottom', ha='center', fontsize=12, color='red')
    cb.ax.text(1.05, -0.05, 'Low Risk', va='top', ha='center', fontsize=12, color='green')

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
    plt.title('Sentiment Analysis of Financial Stocks with Volatility')
    plt.xlabel('Body Sentiment')
    plt.ylabel('Trend Sentiment')
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
