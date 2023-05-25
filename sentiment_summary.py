import os
import pandas as pd

# Define your directory
directory = 'C:/Users/Marcos/Desktop/Uni/PI/DataMining/2023'


# Prepare a dictionary to store the data
data = {'Filename': [], 'Sentiment_Average': [], 'Rating_Average': []}

# Iterate over each file in the directory
for filename in os.listdir(directory):
    # Only process sentiment analysis .xlsx files
    if filename.endswith('_sentiment.xlsx'):
        # Load the data
        df = pd.read_excel(os.path.join(directory, filename), engine='openpyxl')
        
        # Get the averages row
        averages_row = df.iloc[-1]  # Get the last row
        
        # Add the filename and the averages to the data dictionary
        data['Filename'].append(filename)
        data['Sentiment_Average'].append(averages_row['Sentiment'])
        data['Rating_Average'].append(averages_row['Rating'])

# Convert the data dictionary to a DataFrame
summary_df = pd.DataFrame(data)

# Sort the summary DataFrame by 'Sentiment_Average' in descending order
summary_df = summary_df.sort_values(by='Sentiment_Average', ascending=False)

# Save the summary DataFrame to an Excel file
summary_df.to_excel(os.path.join(directory, 'summary_sentiment.xlsx'), index=False)