from League_Scraper import League_Scraper
from Major_Scraper import Major_Scraper
from TransactionsDB import execute_creation_and_populate

'''
    This is the main program that runs through every major function created.
    It generates new data files by overwriting old data files with the scraped
    data from RealGM International Transactions website. Running this program 
    will take less than 10 minutes. 

    It will gather all league data
    Then gather data on each transaction, season, player, and team in association with a league
    Then it will create the Transactions.db file from scratch and populate it.
'''
League_Scraper()
print("--------------------------League Scrapping Finished!--------------------------")
Major_Scraper()
print("--------------------------Overall Scrapping Finished!-------------------------")
execute_creation_and_populate()
print("All Done!")
