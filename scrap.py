import requests
from bs4 import BeautifulSoup
import pandas as pd

import urllib.request  # we are going to need to generate a Request object
from bs4 import BeautifulSoup as soup


import csv


csv_file_path = 'country_leagues.csv'
country_league_dict = {}

# dict for shortnames
with open(csv_file_path, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        country = row['Country']
        league_shortname = row['League_Shortname']
        country_league_dict[country] = league_shortname



def club_values(league_shortname, season):
    my_url = "https://www.transfermarkt.com/premier-league/startseite/wettbewerb/" + league_shortname + "/plus/?saison_id=" + str(
        season)

    print(league_shortname, season)
    # here we define the headers for the request
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'}

    # this request object will integrate your URL and the headers defined above
    req = urllib.request.Request(url=my_url, headers=headers)

    # calling urlopen this way will automatically handle closing the request
    with urllib.request.urlopen(req) as response:
        html_content = response.read()

    if "Total market value" not in str(html_content):  # case when total market values for season dont exist yet
        return club_values(league_shortname, season - 1)

    # Parse the HTML content using BeautifulSoup
    soup1 = BeautifulSoup(html_content, 'html.parser')
    soup = soup1.find('div', class_='responsive-table')

    # Find all rows in the table body
    rows = soup.find_all('tr', class_=['odd', 'even'])

    # Prepare lists to store club names and their total market values
    clubs = []
    total_market_values = []

    # Loop through each row and extract the club name and total market value
    for row in rows:
        club_name = row.find_all('a')[1].get_text()

        total_market_value = row.find_all('td', class_='rechts')[-1].get_text()
        clubs.append(club_name)
        total_market_values.append(total_market_value)

    # Create a DataFrame to store the data
    df = pd.DataFrame({
        'Club': clubs,
        'Total Market Value': total_market_values
    })

    def convert_market_value(value):
        """Convert market value from string to float."""
        value = value.replace('€', '').strip()  # Remove the Euro symbol and any extra spaces

        if 'bn' in value:
            # If the value is in billions, multiply by 1e9
            return float(value.replace('bn', '').replace(',', '')) * 1e9
        elif 'm' in value:
            # If the value is in millions, multiply by 1e6
            return float(value.replace('m', '').replace(',', '')) * 1e6
        elif 'k' in value:
            # If the value is in millions, multiply by 1e6
            return float(value.replace('k', '').replace(',', '')) * 1e3
        else:
            # Handle if there is no 'bn' or 'm', fallback just to float conversion
            return float(value.replace(',', ''))

    df['Total Market Value'] = df['Total Market Value'].apply(convert_market_value)

    return df