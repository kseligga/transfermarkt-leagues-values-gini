from datetime import datetime

import numpy as np
import csv
import pandas as pd

from scrap import club_values


# Function to calculate Gini coefficient
def gini_coefficient(values):
    sorted_values = np.sort(values)
    n = len(values)
    cumulative_sum = np.cumsum(sorted_values)
    sum_values = cumulative_sum[-1]
    gini = (2 * np.sum((np.arange(1, n + 1) * sorted_values))) / (n * sum_values) - (n + 1) / n
    return gini


def calculate_gini_coefficients(season):
    # Path to your CSV file
    csv_file_path = 'country_leagues.csv'

    # Initialize list to store results
    results = []

    # Read the CSV and iterate through each league shortname
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            country = row['Country']
            league_shortname = row['League_Shortname']

            df = club_values(league_shortname, season)

            market_values = df['Total Market Value'].values
            total_market_value = np.sum(market_values)
            gini = gini_coefficient(market_values)
            average_market_value = df['Total Market Value'].mean()

            results.append((country, gini, total_market_value, average_market_value))

    # Convert results to a DataFrame for better visualization
    results_df = pd.DataFrame(results,
                              columns=['Country', 'Gini Coefficient', 'Total Market Value', 'Average Market Value'])

    # Print the results
    print(results_df)

    now = datetime.now()
    date = now.strftime("%d%m%Y")

    # Save to CSV if needed
    results_df.to_csv(f'league_gini_coefficients_{season}_{date}.csv', index=False, encoding='utf-8')