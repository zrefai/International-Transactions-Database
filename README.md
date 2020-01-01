# RealGM-International-Transactions-Database

A database of all transactions of international basketball team from 2012 - 2019

# Running Main_Program

SETUP: If you want to run the entire program, please first open TransactionsDB.py. On line4 there is the prepend to an absolute path. This absolute path is used to open the data files generated. To run the program properly, you need to replace my prepend absolute path to the project folder with your own absolute path. I'd advise putting the whole project on your Desktop, finding the absolute path of the project folder, and copying and pasting it into the line specified above. If you followed what i've outlined, you will need to delete "/Users/zakirefai/Dekstop/" and replace it with your own absolute file path. The rest of the path is included in the program, so you will need to stop at your Desktop folder if the main project folder is on your Desktop. To see an example of the rest of the path, scroll to line 171. If there's any trouble with the setup please email me! You may also need to install bs4 and python requests. Use these lines to install it.

'''
pip install bs4
pip install requests
'''

One can run the entire program by running the Main_Program.py file. This will step through all the functions necessary to gather the right data, format it, create the database, and populate it. Please run Main_Program.py to refresh the data files if new transactions were made after submission (which is December 13th 2019). The main program will take anywhere from 5 - 10 minutes depending on your internet connection. If any errors occur, it's because of your internet connection. If you run into an error, re-run Main_Program.py until no errors appear. Main_Program.py will also update you on what stage it's at in the program.

You can also just run individual portions of Main_Program.py. League_Scraper() will generate all league files across each season. Major_Scraper() will generate the necessary data to populate the database by gathering data on seasons, players, teams, transactions, and other information to link these files together in the DB.
execute_creation_and_populate() will create the database and populate it with the files created from League_Scraper() and Major_Scraper().

# Running Queries on Database

There is a send_query(query) function in TransactionsDB.py. It takes a query as a parameter and prints out the response from the Transactions.db to the console. You can find example queries at the bottom of TransactionsDB.py

# Running HTML Functions

I really tried to do the bonus portion of this project, but my time was needed for another project. So I created functions that query the database and print its output to an HTML file. The queries for these HTML files are located at the bottom of TransactionsDB.py. These HTML files can be viewed by going to HTML_File_Outputs folder. You can compares these HTML files to the RealGM website and find that they have the same results.

If you ran Main_Program.py, you'll want to uncomment the functions on line 374, 385, and 396 and run the TransactionsDB.py file to re-generate the HTML files with updated transactions.
