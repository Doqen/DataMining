import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

# Load the data
df = pd.read_excel('2019_a_star_is_born_user_reviews.xlsx', engine='openpyxl')

# Initialize the sentiment intensity analyzer
sid = SentimentIntensityAnalyzer()

# Define function for sentiment analysis
def analyze_sentiment(text):
    analysis = sid.polarity_scores(text)
    return analysis['compound']  # return the compound score

# Apply sentiment analysis to the 'Review' column
df['Sentiment'] = df['Review'].apply(analyze_sentiment)

# Calculate averages
sentiment_average = df['Sentiment'].mean()
rating_average = df['Rating'].mean()

# Create a new DataFrame with the averages
averages_df = pd.DataFrame({'Sentiment': [sentiment_average], 'Rating': [rating_average]}, index=['Average'])

# Append averages to the bottom of the original DataFrame
df_with_averages = df.append(averages_df)

# Save the results
df_with_averages.to_excel('2019_a_star_is_born_user_reviews_sentiment.xlsx', index=False)

