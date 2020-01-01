import requests
from bs4 import BeautifulSoup
import csv
import re

MASTER_PLAYER_ARRAY = []
MASTER_TRANSACTION_ARRAY = []
MASTER_TEAM_ARRAY = []
MASTER_SEASON_ARRAY = []
MASTER_RECORD_ARRAY = []
SEASON_PRIMARY_ID = 1
RECORD_PRIMARY_ID = 1
YEAR = 2013
TRANSACTION_PRIMARY_ID = 1


class ExitTransaction:
    def __init__(self, id_=None, player_ID=None, date=None, exitTeam=None, transaction_type="Exit"):
        self.id = id_
        self.player_ID = player_ID
        self.date = date
        self.exitTeam = exitTeam
        self.transaction_type = transaction_type

    def print(self):
        return self.id + "," + self.date + "," + self.player_ID + "," + self.exitTeam + "," + self.transaction_type


class TransferTransaction:
    def __init__(self, id_=None, player_ID=None, date=None, prevTeam=None, newTeam=None, transaction_type="Transfer"):
        self.id = id_
        self.player_ID = player_ID
        self.date = date
        self.prevTeam = prevTeam
        self.newTeam = newTeam
        self.transaction_type = transaction_type

    def print(self):
        return self.id + "," + self.date + "," + self.player_ID + "," + self.prevTeam + "," + self.newTeam + "," + self.transaction_type


class SigningTransaction:
    def __init__(self, id_=None, player_ID=None, date=None, newTeam=None, transaction_type="Signing"):
        self.id = id_
        self.player_ID = player_ID
        self.date = date
        self.newTeam = newTeam
        self.transaction_type = transaction_type

    def print(self):
        return self.id + "," + self.date + "," + self.player_ID + "," + self.newTeam + "," + self.transaction_type


class Team:
    def __init__(self, id_=None, name=None, link=None):
        self.id = id_
        self.name = name
        self.link = link

    def print(self):
        return self.id + "," + self.name + "," + self.link


class Season:
    def __init__(self, id_=None, league_ID=None, team_ID=None, year=None):
        self.id = id_
        self.league_ID = league_ID
        self.team_ID = team_ID
        self.year = year

    def print(self):
        return self.id + "," + self.league_ID + "," + self.team_ID + "," + self.year


class Player:
    def __init__(self, id_=None, name=None, link=None):
        self.id = id_
        self.name = name
        self.link = link

    def print(self):
        return self.id + "," + self.name + "," + self.link


class Record:
    def __init__(self, id_=None, team_ID=None, transaction_ID=None):
        self.id = id_
        self.team_ID = team_ID
        self.transaction_ID = transaction_ID


def date_converter(date):
    # Dates are done like YYYY-MM-DD in SQLite
    month = date[0]
    day = date[1]
    year = date[2]

    month_swtich = {
        'January': '01',
        'February': '02',
        'March': '03',
        'April': '04',
        'May': '05',
        'June': '06',
        'July': '07',
        'August': '08',
        'September': '09',
        'October': '10',
        'November': '11',
        'December': '12'
    }

    month = month_swtich.get(month)

    # If day only has a single digit, prepend a zero
    if int(day) < 10:
        day = '0' + day

    return year + "-" + month + "-" + day


# Function to read in player data from scraping
def player_data(player):

    # Split array for manageable access of data
    player_entry = player['href'].split('/')

    # Add player data to new player object and return
    new_player = Player()
    new_player.id = player_entry[-1]
    new_player.name = player.string
    new_player.link = "https://basketball.realgm.com/player/" + \
        player_entry[2] + "/Summary/" + new_player.id

    return new_player


# Function to read in season data from scraping
def season_data(season_instance):
    # id league_ID team_ID year
    # Use gloabl variable SEASON_PRIMARY_ID for season primary keys
    global SEASON_PRIMARY_ID

    season = Season()
    season.id = str(season_instance[3]) + \
        str(season_instance[6]) + str(YEAR - 2010)
    season.league_ID = season_instance[3]
    season.team_ID = season_instance[6]
    season.year = str(YEAR - 1) + "-" + str(YEAR)

    MASTER_SEASON_ARRAY.append(season)
    SEASON_PRIMARY_ID += 1


# Function to read in team data from scraping
def team_data(team_instance, a):
    # Create a team to keep track of team data
    team = Team()
    team.id = team_instance[-2]
    team.name = a.string
    team.link = "https://basketball.realgm.com/international/league/" + \
                team_instance[3] + "/" + team_instance[4] + \
                "/team/" + team_instance[6] + "/" + team_instance[7]

    MASTER_TEAM_ARRAY.append(team)

    season_data(team_instance)


# Function to read in record data from scraping
def record_data(record_instance, transaction_ID):
    record = Record()

    # Set global variable
    global RECORD_PRIMARY_ID

    record.id = RECORD_PRIMARY_ID
    record.team_ID = record_instance[-2]
    record.transaction_ID = transaction_ID

    RECORD_PRIMARY_ID += 1

    MASTER_RECORD_ARRAY.append(record)


# Function to read in transfer transaction data from scraping
def transfer_transaction_data(transfer_transaction_values, date):
    # Set counter for seeing which a tag we are at
    counter = 1
    # Declare a transfer transaction to keep track transaction of data
    transfer_transaction = TransferTransaction()

    # Input date and id
    transfer_transaction.date = date
    # Declare gloabl TRANSACTION_PRIMARY_ID
    global TRANSACTION_PRIMARY_ID

    transfer_transaction.id = str(TRANSACTION_PRIMARY_ID)

    a_list = transfer_transaction_values("a")

    for a in a_list:
        if len(a_list) < 2:
            return
        elif counter == 1:
            player_entry = a['href'].split('/')

            # Error checking for false entry
            if player_entry[0] == '#' or player_entry[1] == '#':
                return

            transfer_transaction.player_ID = player_entry[-1]
        elif counter == 2:
            previousTeam = a['href'].split('/')

            # Error checking for false entry
            if previousTeam[0] == '#' or previousTeam[1] == '#':
                return

            transfer_transaction.prevTeam = previousTeam[-2]

            team_data(previousTeam, a)

        elif counter == 3:
            newTeam = a['href'].split('/')

            # Error checking for false entry
            if newTeam[0] == '#' or newTeam[1] == '#':
                return

            transfer_transaction.newTeam = newTeam[-2]

            team_data(newTeam, a)
            record_data(newTeam, transfer_transaction.id)

        counter += 1

    MASTER_TRANSACTION_ARRAY.append(transfer_transaction)
    TRANSACTION_PRIMARY_ID += 1


# Function to read in signing transaction data from scraping
def signing_transaction_data(signing_transaction_values, date):
    # Set counter for seeing which a tag we are at
    counter = 1
    # Declare a signing transaction to keep track of data
    signing_transaction = SigningTransaction()

    # Set date and id
    signing_transaction.date = date
    # Declare gloabl TRANSACTION_PRIMARY_ID
    global TRANSACTION_PRIMARY_ID

    signing_transaction.id = str(TRANSACTION_PRIMARY_ID)

    a_list = signing_transaction_values("a")

    for a in a_list:
        if len(a_list) < 2:
            return
        if counter == 1:
            player_entry = a['href'].split('/')

            # Error checking for false entry
            if player_entry[0] == '#' or player_entry[1] == '#':
                return None

            signing_transaction.player_ID = player_entry[-1]
        elif counter == 2:
            newTeam = a['href'].split('/')

            # Error checking for false entry
            if newTeam[0] == '#' or newTeam[1] == '#':
                return

            signing_transaction.newTeam = newTeam[-2]

            team_data(newTeam, a)
            record_data(newTeam, signing_transaction.id)

        counter += 1

    MASTER_TRANSACTION_ARRAY.append(signing_transaction)
    TRANSACTION_PRIMARY_ID += 1


# Function to read in exit transaction data from scraping
def exit_transaction_data(exit_transaction_values, date):
    # Set counter for seeing which a tag we are at
    counter = 1
    # Declare a signing transaction to keep track of data
    exit_transaction = ExitTransaction()

    # Set date and id
    exit_transaction.date = date
    # Declare gloabl TRANSACTION_PRIMARY_ID
    global TRANSACTION_PRIMARY_ID

    exit_transaction.id = str(TRANSACTION_PRIMARY_ID)

    a_list = exit_transaction_values("a")

    for a in a_list:
        if len(a_list) < 2:
            return
        if counter == 1:
            player_entry = a['href'].split('/')

            # Error checking for false entry
            if player_entry[0] == '#' or player_entry[1] == '#':
                return

            exit_transaction.player_ID = player_entry[-1]
        elif counter == 2:
            exitTeam = a['href'].split('/')

            # Error checking for false entry
            if exitTeam[0] == '#' or exitTeam[1] == '#':
                return

            exit_transaction.exitTeam = exitTeam[-2]

            team_data(exitTeam, a)
            record_data(exitTeam, exit_transaction.id)

        counter += 1

    MASTER_TRANSACTION_ARRAY.append(exit_transaction)
    TRANSACTION_PRIMARY_ID += 1


def write_to_file(array_name):
    if array_name == "MASTER_PLAYER_ARRAY":
        # Open player file from that year
        f = csv.writer(open('Data_Files/Player_Data/Player_' + str(YEAR - 1) +
                            '-' + str(YEAR) + '.csv', 'w'))
        for player in MASTER_PLAYER_ARRAY:
            f.writerow([player.id, player.name, player.link])

        print("--- Player Data scrapped into file")
    elif array_name == "MASTER_SEASON_ARRAY":
        # Open season file from that year
        f = csv.writer(open('Data_Files/Season_Data/Season_' + str(YEAR - 1) +
                            '-' + str(YEAR) + '.csv', 'w'))
        for season in MASTER_SEASON_ARRAY:
            f.writerow([season.id, season.league_ID,
                        season.team_ID, season.year])

        print("--- Season Data scrapped into file")
    elif array_name == "MASTER_TEAM_ARRAY":
        # Open team file from that year
        f = csv.writer(open('Data_Files/Team_Data/Team_' + str(YEAR - 1) +
                            '-' + str(YEAR) + '.csv', 'w'))
        for team in MASTER_TEAM_ARRAY:
            f.writerow([team.id, team.name, team.link])

        print("--- Team Data scrapped into file")
    elif array_name == "MASTER_TRANSACTION_ARRAY":
        # Open transaction file from that year
        f = csv.writer(open('Data_Files/Transaction_Data/Transaction_' + str(YEAR - 1) +
                            '-' + str(YEAR) + '.csv', 'w'))
        for transaction in MASTER_TRANSACTION_ARRAY:
            if transaction.transaction_type == "Signing":
                f.writerow([transaction.id, transaction.date, transaction.player_ID,
                            transaction.newTeam, transaction.transaction_type])
            elif transaction.transaction_type == "Transfer":
                f.writerow([transaction.id, transaction.date, transaction.player_ID,
                            transaction.prevTeam, transaction.newTeam, transaction.transaction_type])
            elif transaction.transaction_type == "Exit":
                f.writerow([transaction.id, transaction.date, transaction.player_ID,
                            transaction.exitTeam, transaction.transaction_type])
            else:
                print("ERROR posting transaction to file")
                print(transaction.print())

        print("--- Transaction Data scrapped into file")
    elif array_name == "MASTER_RECORD_ARRAY":
        f = csv.writer(open('Data_Files/Record_Data/Record_' + str(YEAR - 1) +
                            '-' + str(YEAR) + '.csv', 'w'))
        for record in MASTER_RECORD_ARRAY:
            f.writerow([record.id, record.team_ID, record.transaction_ID])

        print("--- Record Data scrapped into file")


# Perform scraping for all data types
def scrape_data(year, flag):
    # Open page
    page = requests.get(
        'https://basketball.realgm.com/international/transactions/' + str(year) + '#')
    soup = BeautifulSoup(page.text, 'html.parser')

    # Get all divs with page-nav-option clearfix as class
    # Transaction_list is seperated by month
    transaction_list = soup.find_all(class_='portal widget fullpage')

    # Iterate through transaction list
    for transaction in transaction_list:
        # Get the date and convert to proper format
        date = date_converter(re.split(' |, ', transaction.find('h3').string))

        # Get all list of transactions from a month
        single_month_transactions = transaction.find_all('li')

        # Count through the list of li in single_month_transactions to get player data
        for one_transaction in single_month_transactions:
            # Getting 1 player transaction out a month
            player_transaction = one_transaction.find_all('a')

            # Find transaction type
            if "previously with" in one_transaction.get_text():  # Signing Transaction
                if (flag == 1):
                    print(transaction)
                    print(
                        "-------------------------------------------------------------------------------------------------------------")
                    print(one_transaction)
                    print(
                        "-------------------------------------------------------------------------------------------------------------")
                # Send through function
                transfer_transaction_data(
                    one_transaction, date)
            elif "has signed with" in one_transaction.get_text():  # Transfer Transaction
                if (flag == 1):
                    print(transaction)
                    print(
                        "-------------------------------------------------------------------------------------------------------------")
                    print(one_transaction)
                    print(
                        "-------------------------------------------------------------------------------------------------------------")
                # Send through function
                signing_transaction_data(
                    one_transaction, date)
            elif "has left" in one_transaction.get_text():  # Exit Transaction
                if (flag == 1):
                    print(transaction)
                    print(
                        "-------------------------------------------------------------------------------------------------------------")
                    print(one_transaction)
                    print(
                        "-------------------------------------------------------------------------------------------------------------")
                # Send through function
                exit_transaction_data(
                    one_transaction, date)
            elif "has joined" in one_transaction.get_text():  # Transfer Transaction
                if (flag == 1):
                    print(transaction)
                    print(
                        "-------------------------------------------------------------------------------------------------------------")
                    print(one_transaction)
                    print(
                        "-------------------------------------------------------------------------------------------------------------")
                # Send through function
                signing_transaction_data(
                    one_transaction, date)
            else:  # Error Checking
                print("ERROR: COULD NOT DETERMINE TRANSACTION")
                print(one_transaction)
                continue

            # Get player out of player transaction
            MASTER_PLAYER_ARRAY.append(
                player_data(player_transaction[0]))


# Performs loop of scrape_data function for all seasons
def Major_Scraper():
    # Year needs to change based globally
    global YEAR
    global MASTER_PLAYER_ARRAY
    global MASTER_SEASON_ARRAY
    global MASTER_TEAM_ARRAY
    global MASTER_TRANSACTION_ARRAY
    global MASTER_RECORD_ARRAY
    
    seasons = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

    for year in seasons:

        YEAR = year
        print(str(YEAR) + " season scrapping")
        
        # Set flag as 1 to check each transaction
        scrape_data(year, 0)

        print(str(YEAR) + " scrapping done. Uploading to files")

        arrays = ["MASTER_RECORD_ARRAY", "MASTER_TEAM_ARRAY",
                  "MASTER_SEASON_ARRAY", "MASTER_TRANSACTION_ARRAY", "MASTER_PLAYER_ARRAY"]

        # Create file writer
        for array in arrays:
            write_to_file(array)

        # Erase memory in array
        MASTER_PLAYER_ARRAY = []
        MASTER_SEASON_ARRAY = []
        MASTER_TEAM_ARRAY = []
        MASTER_TRANSACTION_ARRAY = []
        MASTER_RECORD_ARRAY = []

        print(str(YEAR) + " major scrape done")
