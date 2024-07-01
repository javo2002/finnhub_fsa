import matplotlib.pyplot as plt
import numpy as np

class SentimentAdjuster:
    def __init__(self, baseline_threshold=0.3):
        self.baseline_threshold = baseline_threshold

    def adjust_sentiment(self, sentiment, change):
        if sentiment == 'Negative' and change < -self.baseline_threshold:
            return 'Negative'
        elif sentiment == 'Positive' and change < -self.baseline_threshold:
            return 'Negative'
        elif sentiment == 'Negative' and change > self.baseline_threshold:
            return 'Positive'
        elif sentiment == 'Positive' and change > self.baseline_threshold:
            return 'Positive'
        return sentiment

class SentimentPlotter:
    def __init__(self, quotes, sentiments, changes):
        self.quotes = quotes
        self.sentiments = sentiments
        self.changes = changes

    def plot_changes(self, adjusted_sentiments):
        fig, ax = plt.subplots()

        x = np.arange(len(self.quotes))
        y = self.changes

        # Plot changes
        ax.plot(x, y, marker='o', linestyle=' ', color='b')

        # Shading the green area between -0.3 and 0.3 across the entire plot
        ax.axhspan(-0.3, 0.3, facecolor='grey', alpha=0.3)

        # Shading the red areas outside the range -0.3 to 0.3
        ax.axhspan(-1, -0.3, facecolor='red', alpha=0.3)
        ax.axhspan(0.3, 1, facecolor='green', alpha=0.3)

        # Adding labels
        for i, txt in enumerate(self.quotes):
            ax.annotate(txt, (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')

        ax.set_xlabel('Quotes')
        ax.set_ylabel('Sentiment of %Change')
        ax.set_title('Sentiment Adjustment Based on Percentage Change')
        ax.axhline(y=0, color='black', linestyle='--')
        ax.axhline(y=-0.3, color='black', linestyle='--')
        ax.axhline(y=0.3, color='black', linestyle='--')

        # Set y-axis limits
        ax.set_ylim(-1, 1)

        # Set x-axis tick labels
        ax.set_xticks(x)
        ax.set_xticklabels(self.quotes)

        plt.show()

# Sample data
quotes = ["Quote 1 (-)", "Quote 2 (+)", "Quote 3", "Quote 4", "Quote 5"]
sentiments = ["Positive", "Negative", "Positive", "Negative", "Positive"]
changes = [0.5, -0.4, 0.2, 0.35, -0.5]

# Create SentimentAdjuster instance
adjuster = SentimentAdjuster()

# Apply sentiment adjustment
adjusted_sentiments = [adjuster.adjust_sentiment(sentiment, change) for sentiment, change in zip(sentiments, changes)]

# Create SentimentPlotter instance
plotter = SentimentPlotter(quotes, sentiments, changes)

# Plot the changes
plotter.plot_changes(adjusted_sentiments)
