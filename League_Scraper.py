import requests
from bs4 import BeautifulSoup
import csv


# This function scrapes the leagues off of an HTML page for a given year
def scraper(year):
    # Open page
    page = requests.get(
        'https://basketball.realgm.com/international/transactions/' + str(year) + '#')
    soup = BeautifulSoup(page.text, 'html.parser')

    # Get all divs with page-nav-option clearfix as class
    league_list = soup.find_all(class_='page-nav-option clearfix')
    # Grab the second div with the same class and get only the option tag
    league_items = league_list[1].find_all('option')
    # Now we have all leagues in their option tags with their values put info into array as text
    # Array to hold all league data
    league_array = []

    # Open file for writing league data
    f = csv.writer(open('Data_Files/League_Data/League_' + str(year - 1) +
                        '-' + str(year) + '.csv', 'w'))

    for league in league_items:
        league_listing = league['value'].split('/')
        if (league_listing[2] == 'transactions'):
            # Do nothing
            continue
        elif (league_listing[2] == 'league'):
            id_ = str(league_listing[3])
            name = league.string
            link = "https://basketball.realgm.com/international/league/" + \
                id_ + "/" + league_listing[4]

            # Add each league to a file
            f.writerow([id_, name, link])


# This function repeats the scraper function above given seasons
def League_Scraper():
    seasons = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

    for year in seasons:
        scraper(year)
        print(str(year) + " season league scrapping finished")
