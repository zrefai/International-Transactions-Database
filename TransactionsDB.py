import sqlite3
import csv

FILE_PATH = '/Users/zakirefai/Desktop/'


def createTables():
    # Create the connection to Transactions.db
    conn = sqlite3.connect('Transactions.db')
    c = conn.cursor()

    # Drop tables
    c.execute('''DROP TABLE IF EXISTS Season''')
    c.execute('''DROP TABLE IF EXISTS Record''')
    c.execute('''DROP TABLE IF EXISTS League''')
    c.execute('''DROP TABLE IF EXISTS Team''')
    c.execute('''DROP TABLE IF EXISTS Player_Transaction''')
    c.execute('''DROP TABLE IF EXISTS Exit''')
    c.execute('''DROP TABLE IF EXISTS Transfer''')
    c.execute('''DROP TABLE IF EXISTS Signing''')
    c.execute('''DROP TABLE IF EXISTS Player''')

    # Create tables
    c.execute('''CREATE TABLE League
                (league_ID INTEGER,
                name TEXT,
                link TEXT);''')
    c.execute('''CREATE TABLE Team
                (team_ID INTEGER,
                name TEXT,
                link TEXT);''')
    c.execute('''CREATE TABLE Player
                (player_ID INTEGER,
                name TEXT,
                link TEXT);''')
    c.execute('''CREATE TABLE Player_Transaction
                (transaction_ID INTEGER,
                date DATE,
                type TEXT,
                player_ID INTEGER,
                FOREIGN KEY(player_ID) REFERENCES Player(player_ID));''')
    c.execute('''CREATE TABLE Signing
                (transaction_ID INTEGER,
                newTeam TEXT,
                player_ID INTEGER,
                FOREIGN KEY(transaction_ID) REFERENCES Player_Transaction(transaction_ID)
                FOREIGN KEY(player_ID) REFERENCES Player(player_ID));''')
    c.execute('''CREATE TABLE Transfer
                (transaction_ID INTEGER,
                prevTeam TEXT,
                newTeam TEXT,
                player_ID INTEGER,
                FOREIGN KEY(transaction_ID) REFERENCES Player_Transaction(transaction_ID)
                FOREIGN KEY(player_ID) REFERENCES Player(player_ID));''')
    c.execute('''CREATE TABLE Exit
                (transaction_ID INTEGER,
                exitTeam TEXT,
                player_ID INTEGER,
                FOREIGN KEY(transaction_ID) REFERENCES Player_Transaction(transaction_ID)
                FOREIGN KEY(player_ID) REFERENCES Player(player_ID));''')
    c.execute('''CREATE TABLE Season
                (season_ID INTEGER,
                league_ID INTEGER,
                team_ID INTEGER,
                season TEXT,
                FOREIGN KEY (league_ID) REFERENCES League(league_ID),
                FOREIGN KEY (team_ID) REFERENCES Team(team_ID))''')
    c.execute('''CREATE TABLE Record
                (record_ID INTEGER,
                team_ID INTEGER,
                transaction_ID INTEGER,
                FOREIGN KEY (team_ID) REFERENCES Team(team_ID),
                FOREIGN KEY(transaction_ID) REFERENCES Player_Transaction(transaction_ID))''')

    conn.commit()
    conn.close()


def send_query(query):
    # Create the connection to Transactions.db
    conn = sqlite3.connect('Transactions.db')
    c = conn.cursor()

    for row in c.execute(query):
        print(row)


def write_season_to_HTML(query, title):
    # Create the connection to Transactions.db
    conn = sqlite3.connect('Transactions.db')
    c = conn.cursor()

    html_file = open(
        "HTML_File_Outputs/2019-2020_Season_Transactions.html", "w")
    html_header = '<!DOCTYPE html> <html> <head> <title>' + \
        title + '</title> </head> <h1> ' + title + ' </h1> <body> <ul>'

    html_file.write(html_header)

    for row in c.execute(query):
        if (row[2] == "Signing"):
            html_file.write(
                '<li> ' + row[-1] + ' -- <a href=' + row[1] + '>' + row[0] + '</a> has signed with <a href=' + row[4] + '>' + row[3] + '</a>.</li>')
        elif (row[2] == "Transfer"):
            html_file.write(
                '<li> ' + row[-1] + ' -- <a href=' + row[1] + '>' + row[0] + '</a> transfered to <a href=' + row[4] + '>' + row[3] + '</a>.</li>')
        else:
            html_file.write(
                '<li> ' + row[-1] + ' -- <a href=' + row[1] + '>' + row[0] + '</a> has left <a href=' + row[4] + '>' + row[3] + '</a>.</li>')

    html_file.write('''
    </ul> 
        </body> 
    </html>''')
    html_file.close()
    conn.close()


def write_team_to_HTML(query, title):
    # Create the connection to Transactions.db
    conn = sqlite3.connect('Transactions.db')
    c = conn.cursor()

    html_file = open("HTML_File_Outputs/2019-2020_Team_Transactions.html", "w")
    html_header = '<!DOCTYPE html> <html> <head> <title>' + \
        title + '</title> </head> <h1> ' + title + ' </h1> <body> <ul>'

    html_file.write(html_header)

    for row in c.execute(query):
        html_file.write(
            '<li> <a href=' + row[1] + '>' + row[0] + '</a>')

    html_file.write('''
    </ul> 
        </body> 
    </html>''')
    html_file.close()
    conn.close()


def write_all_team_transactions_to_HTML(query, title):
    # Create the connection to Transactions.db
    conn = sqlite3.connect('Transactions.db')
    c = conn.cursor()

    html_file = open(
        "HTML_File_Outputs/All_Real_Madrid_Transactions.html", "w")
    html_header = '<!DOCTYPE html> <html> <head> <title>' + \
        title + '</title> </head> <h1> ' + title + ' </h1> <body> <ul>'

    html_file.write(html_header)

    for row in c.execute(query):
        html_file.write(
            '<li>' + row[0] + ' -- <a href=' + row[2] + '>' + row[1] + '</a> --' + row[-1] + '</li>')

    html_file.write('''
    </ul> 
        </body> 
    </html>''')
    html_file.close()
    conn.close()


def read_in_player_data(year):
    # Create the connection to Transactions.db
    conn = sqlite3.connect('Transactions.db')
    c = conn.cursor()

    with open(FILE_PATH + 'OKCT Project/Data_Files/Player_Data/Player_' + str(year - 1) + '-' + str(year) + '.csv') as csv_file:
        for row in csv_file:
            data = row.split(',')

            query = "INSERT INTO Player (player_ID, name, link) VALUES (?, ?, ?)"

            if (len(data) > 3):
                # Format names with Jr. in them
                name = (data[1] + ',' + data[2]).replace('"', '')
                # Format links
                link = data[3].replace('\n', '')

                c.execute(query, (data[0], name, link))
            else:
                name = data[1].replace('"', '')
                # Format links
                link = data[2].replace('\n', '')
                c.execute(query, (data[0], name, link))

    # Delete duplicate players
    c.execute(
        "DELETE FROM Player WHERE rowid NOT IN (SELECT MIN(rowid) FROM Player GROUP BY player_ID)")

    conn.commit()
    conn.close()


def read_in_team_data(year):
    # Create the connection to Transactions.db
    conn = sqlite3.connect('Transactions.db')
    c = conn.cursor()

    with open(FILE_PATH + 'OKCT Project/Data_Files/Team_Data/Team_' + str(year - 1) + '-' + str(year) + '.csv') as csv_file:
        for row in csv_file:
            data = row.split(',')

            query = "INSERT INTO Team (team_ID, name, link) VALUES (?, ?, ?)"

            link = data[2].replace('\n', '')

            c.execute(query, (data[0], data[1], link))

    # Delete duplicate teams
    c.execute(
        "DELETE FROM Team WHERE rowid NOT IN (SELECT MIN(rowid) FROM Team GROUP BY team_ID)")

    conn.commit()
    conn.close()


def read_in_league_data(year):
    # Create the connection to Transactions.db
    conn = sqlite3.connect('Transactions.db')
    c = conn.cursor()

    with open(FILE_PATH + 'OKCT Project/Data_Files/League_Data/League_' + str(year - 1) + '-' + str(year) + '.csv') as csv_file:
        for row in csv_file:
            data = row.split(',')

            query = "INSERT INTO League (league_ID, name, link) VALUES (?, ?, ?)"

            link = data[2].replace('\n', '')

            c.execute(query, (data[0], data[1], link))

    # Delete duplicate leagues
    c.execute(
        "DELETE FROM League WHERE rowid NOT IN (SELECT MIN(rowid) FROM League GROUP BY league_ID)")

    conn.commit()
    conn.close()


def read_in_season_data(year):
    # Create the connection to Transactions.db
    conn = sqlite3.connect('Transactions.db')
    c = conn.cursor()

    with open(FILE_PATH + 'OKCT Project/Data_Files/Season_Data/Season_' + str(year - 1) + '-' + str(year) + '.csv') as csv_file:
        for row in csv_file:
            data = row.split(',')

            query = "INSERT INTO Season (season_ID, league_ID, team_ID, season) VALUES (?, ?, ?, ?)"

            season = data[3].replace('\n', '')

            c.execute(query, (data[0], data[1], data[2], season))

    # Delete duplicate players
    c.execute(
        "DELETE FROM Season WHERE rowid NOT IN (SELECT MIN(rowid) FROM Season GROUP BY season_ID)")

    conn.commit()
    conn.close()


def read_in_transaction_data(year):
    # Create the connection to Transactions.db
    conn = sqlite3.connect('Transactions.db')
    c = conn.cursor()

    with open('/Users/zakirefai/Desktop/OKCT Project/Data_Files/Transaction_Data/Transaction_' + str(year - 1) + '-' + str(year) + '.csv') as csv_file:
        for row in csv_file:
            data = row.split(',')

            type_ = data[-1].replace("\n", '')

            if type_ == "Signing":  # If transaction is signing
                query = "INSERT INTO Player_Transaction (transaction_ID, date, type, player_ID) VALUES (?, ?, ?, ?)"
                c.execute(query, (data[0], data[1], type_, data[2]))

                query_sign = "INSERT INTO Signing (transaction_ID, newTeam, player_ID) VALUES (?, ?, ?)"
                c.execute(query_sign, (data[0], data[3], data[2]))

            elif type_ == "Transfer":  # If transaction is transfer
                query = "INSERT INTO Player_Transaction (transaction_ID, date, type, player_ID) VALUES (?, ?, ?, ?)"
                c.execute(query, (data[0], data[1], type_, data[2]))

                query_transfer = "INSERT INTO Transfer (transaction_ID, prevTeam, newTeam, player_ID) VALUES (?, ?, ?, ?)"
                c.execute(query_transfer, (data[0], data[3], data[4], data[2]))

            elif type_ == "Exit":  # If transaction is exit
                query = "INSERT INTO Player_Transaction (transaction_ID, date, type, player_ID) VALUES (?, ?, ?, ?)"
                c.execute(query, (data[0], data[1], type_, data[2]))

                query_exit = "INSERT INTO Exit (transaction_ID, exitTeam, player_ID) VALUES (?, ?, ?)"
                c.execute(query_exit, (data[0], data[3], data[2]))

    conn.commit()  # Commit this into db

    conn.close()


def read_in_record_data(year):
    # Create the connection to Transactions.db
    conn = sqlite3.connect('Transactions.db')
    c = conn.cursor()

    with open(FILE_PATH + 'OKCT Project/Data_Files/Record_Data/Record_' + str(year - 1) + '-' + str(year) + '.csv') as csv_file:
        for row in csv_file:
            data = row.split(',')

            query = "INSERT INTO Record (record_ID, team_ID, transaction_ID) VALUES (?, ?, ?)"

            transaction_ID = data[2].replace('\n', '')

            c.execute(query, (data[0], data[1], transaction_ID))

    conn.commit()
    conn.close()


def populate(file_type):
    seasons = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

    if (file_type == "League"):
        for year in seasons:
            read_in_league_data(year)
            print(str(year) + " League Data entered into database")
    elif (file_type == "Team"):
        for year in seasons:
            read_in_team_data(year)
            print(str(year) + " Team Data entered into database")
    elif (file_type == "Player"):
        for year in seasons:
            read_in_player_data(year)
            print(str(year) + " Player Data entered into database")
    elif (file_type == "Transaction"):
        for year in seasons:
            read_in_transaction_data(year)
            print(str(year) + " Transaction Data entered into database")
    elif (file_type == "Season"):
        for year in seasons:
            read_in_season_data(year)
            print(str(year) + " Season Data entered into database")
    elif (file_type == "Record"):
        for year in seasons:
            read_in_record_data(year)
            print(str(year) + " Record Data entered into database")


def execute_creation_and_populate():

    # Create tables
    createTables()

    # File types
    file_type = ["League", "Team", "Player", "Transaction", "Season", "Record"]

    # Loop through and populate each type of data
    for type_ in file_type:
        populate(type_)
        print("All " + type_ + " files loaded")


# Get all players and their teams who had a transaction in 2019-2020 season
season_transactions = '''SELECT P.name, P.link, PT.type, T.name, T.link, PT.date
            FROM Player AS P JOIN Player_Transaction AS PT 
                ON P.player_ID = PT.player_ID 
                JOIN Record R ON PT.transaction_ID = R.transaction_ID 
                JOIN Team T ON R.team_ID = T.team_ID 
                JOIN Season S ON T.team_ID = S.team_ID
            WHERE S.season = '2019-2020' AND PT.date BETWEEN '2019-06-01' AND '2019-12-12'
            ORDER BY PT.date DESC, T.name
            '''
#write_season_to_HTML(season_transactions, '2019-2020 Season Transactions')

team_transactions = '''SELECT P.name, P.link
            FROM Player AS P JOIN Player_Transaction AS PT
                ON P.player_ID = PT.player_ID 
                JOIN Record R ON PT.transaction_ID = R.transaction_ID 
                JOIN Team T ON R.team_ID = T.team_ID 
                JOIN Season S ON T.team_ID = S.team_ID
            WHERE S.Season = '2019-2020' AND T.name = 'Real Madrid' AND PT.date BETWEEN '2019-06-01' AND '2019-12-12'
            ORDER BY PT.date DESC
            '''
#write_team_to_HTML(team_transactions,'2019-2020 Season Transactions from Real Madrid')


overall_transactions = '''SELECT DISTINCT PT.date, P.name, P.link, PT.type
            FROM Player AS P JOIN Player_Transaction AS PT
                ON P.player_ID = PT.player_ID 
                JOIN Record R ON PT.transaction_ID = R.transaction_ID 
                JOIN Team T ON R.team_ID = T.team_ID
            WHERE T.name = 'Real Madrid'
            ORDER BY PT.date
            '''
#write_all_team_transactions_to_HTML(overall_transactions, 'All transactions of Real Madrid')
