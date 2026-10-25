"""
Connecting a Python application to a database with SQLAlchemy.

The examples use MariaDB.

Every application that talks to a database must:
1. Use a library that can communicate with databases from your language (here, SQLAlchemy for Python).
2. Have a driver that knows how to talk to a specific database server (here, a MariaDB/MySQL driver).
3. Establish a connection. A connection needs the same information you give DBeaver:
       username, password, host (localhost or 127.0.0.1), port (3306), and database name.
   Tip: DBeaver shows its drivers under Database -> Driver Manager.
Then the application can:
4. Make requests of the database (run SQL) and work with the results.
"""
import configparser

# ---------------------------------------------------------------------------
# Install the packages
# ---------------------------------------------------------------------------
# Packages are installed once per project (virtual environment), not in the code.
#
# We need to add the following packages:
#
# PyCharm Package Manager (preferred):
#   Left Click the interpreter label in the lower right of the PyCharm window
#   (for example "venv [Python 3.x]"), then click Manage Packages. See Fig. 1
#   Search for each package below and install the latest version.
#   (See the figures in the accompanying documentation.)  See Fig. 2
#       sqlalchemy
#       pymysql
#       mariadb
#
# Terminal (same result):
#   Left click on the "Hamburger" Menu and then go to View->Tool Windows->Terminal and Left Click See.Fig 3
#   pip install sqlalchemy pymysql
#
#   sqlalchemy - the library that builds and runs database requests
#   pymysql    - the driver that speaks to MariaDB/MySQL servers
#
# Standard-library modules such as getpass and sqlite3 come with Python and are
# never installed with pip.
#
# Using the MariaDB native connector
#   pip install mariadb  (this needs the MariaDB C connector on your computer first)
#   then change DRIVER below to "mariadb+mariadbconnector".

# ---------------------------------------------------------------------------
# Section 2 - Imports
# ---------------------------------------------------------------------------
# "from X import Y" and "import X" both work with any module, whether it ships
# with Python or was installed with pip. The only difference is how you name
# things afterward:
#     from getpass import getpass   ->  getpass("Password: ")
#     import getpass                ->  getpass.getpass("Password: ")
from sqlalchemy import create_engine, text, TextClause, ForeignKey
from sqlalchemy.engine import URL
from sqlalchemy.exc import OperationalError, ProgrammingError

from sqlalchemy import Table, Column, Integer, String, CHAR, MetaData
from sqlalchemy import select, insert
#########################  NEW  ##################################
# STEP NEW.1
# Import new packages
from sqlalchemy import update, func, delete, join, outerjoin
from sqlalchemy.exc import SQLAlchemyError


#########################  NEW  ##################################


# create_engine - creates the engine that manages connections to the database
# text          - marks a string as SQL so the engine can send it to the database
# URL           - builds the connection information from separate named pieces
# OperationalError / ProgrammingError - errors we expect to see in this lesson
#     (can't connect / bad SQL such as a misspelled table name)


def main():
    print("Start database connection test")

    # -----------------------------------------------------------------------
    # Section 3 - Define the connection
    # -----------------------------------------------------------------------
    # Never type a password into your code: code gets shared, emailed, and
    # uploaded. getpass() asks for it when the program runs and does not echo it.

    # Initialize parser and read the file
    config = configparser.RawConfigParser()
    config.read('config.ini', encoding='utf-8')

    # Access credentials
    USERNAME = config.get('credentials', 'username')
    password = config.get('credentials', 'password')

    print(f"Username: {USERNAME}, Password: {password}")

    DRIVER = "mariadb+pymysql"  # the database type + the driver
    HOST = "localhost"  # check your connection settings in DBeaver to confirm host and port
    PORT = 3306
    DATABASE = "scrabbledb"

    # URL.create has one argument for each field in DBeaver's connection dialog.
    # It also handles special characters in the password (like @), so you do
    # not have to escape anything yourself.
    database_url = URL.create(
        DRIVER,
        username=USERNAME,
        password=password,
        host=HOST,
        port=PORT,
        database=DATABASE,
    )

    print(database_url)

    # The engine holds the connection information. It does not connect yet.
    # echo=True prints every SQL statement the engine sends, which is useful for
    # comparing against what DBeaver runs. Start with False so the output is easy
    # to read, then switch it to True and run again.
    # NEW: Additional Reading: https://docs.sqlalchemy.org/en/21/tutorial/engine.html
    engine = create_engine(database_url, echo=False)

    #########################  NEW  ##################################
    # STEP NEW.2
    # Declare the metadata instance. This is required before we can use the Table and Column objects.
    # From Essential SQLAlchemy, 2nd Edition
    # "Metadata is used to tie together the database structure so it can be quickly accessed inside SQLAlchemy.
    # It’s often useful to think of metadata as a kind of catalog of Table objects with optional information about the engine and the connection.
    # Additional Reading: https://docs.sqlalchemy.org/en/21/tutorial/metadata.html#setting-up-metadata-with-table-objects
    metadata = MetaData()

    scrabble_games_initial = Table(
        "scrabble_games_initial",
        metadata,
        Column("gameid", Integer, nullable=True),
        Column("tourneyid", Integer, nullable=True),
        Column("tie", CHAR(6), nullable=True),
        Column("winnerid", Integer, nullable=True),
        Column("winnername", String(50), nullable=True),
        Column("winnerscore", Integer, nullable=True),
        Column("winneroldrating", Integer, nullable=True),
        Column("winnernewrating", Integer, nullable=True),
        Column("winnerpos", Integer, nullable=True),
        Column("loserid", Integer, nullable=True),
        Column("losername", String(50), nullable=True),
        Column("loserscore", Integer, nullable=True),
        Column("loseroldrating", Integer, nullable=True),
        Column("losernewrating", Integer, nullable=True),
        Column("loserpos", Integer, nullable=True),
        Column("round", Integer, nullable=True),
        Column("division", Integer, nullable=True),
        Column("date", String(50), nullable=True),
        Column("lexicon", CHAR(6), nullable=True),
        Column("Id", Integer, primary_key=True, autoincrement=True, nullable=False),
        #### NEW.5 DEPENDENCY
        ### NEW For New.5 Need to add the foreign key relationship to person  as the third parameter
        Column("winnerSysId", Integer, ForeignKey("persons.ID"), nullable=False, server_default=text("-1")),
        ### NEW For New.5 Need to add the foreign key relationship to person as the third parameter
        Column("loserSysId", Integer, ForeignKey("persons.ID"), nullable=False, server_default=text("-1")),
        #### END OF NEW.5 DEPENDENCY
        mysql_engine="InnoDB",
        mysql_auto_increment=5790,
        mysql_default_charset="utf8mb4",
        mysql_collate="utf8mb4_uca1400_ai_ci"
    )

    matches = Table("matches", metadata,
                    Column("id", Integer, primary_key=True, autoincrement=True, nullable=False),
                    Column("PlayerA_Id", Integer, nullable=False),
                    Column("PlayerB_Id", Integer, nullable=False),
                    mysql_engine="InnoDB",
                    mysql_auto_increment=5790,
                    mysql_default_charset="utf8mb4",
                    mysql_collate="utf8mb4_uca1400_ai_ci"
                    )
    #########################  NEW  ##################################
    # STEP NEW.2
    # Create the Table Object that matches the Person Table
    # Notice that there are two new columns First and Last Name which will be initialized in the
    # example below.
    #########################  NEW  ##################################

    persons = Table(
        "person",
        metadata,
        Column("ID", Integer, primary_key=True, autoincrement=True),
        Column("FullName", String(50), nullable=False),
        Column("origId", Integer, nullable=False),
        # NEW.3 Dependency - Add FirstName and LastName to the Person table in your ScrabbleDb database.
        Column("FirstName", String(50), nullable=False),
        Column("LastName", String(50), nullable=False),
        # END OF NEW.3 Dependency.
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_uca1400_ai_ci",
        mysql_auto_increment=675,
    )

    #########################  NEW  ##################################
    # STEP NEW.3
    # Split the FullName and update the Last and First Name fields
    #########################  NEW  ##################################
    # Which rows will be updated (in this case all)
    # See: https://docs.sqlalchemy.org/en/21/tutorial/data_update.html#the-update-sql-expression-construct
    updateStatement = update(persons).values(
        # See: https://mariadb.com/docs/server/reference/sql-functions/string-functions/substring_index
        # func allows SQLAlchemy to call SQL functions see: https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#working-with-sql-functions
        FirstName=func.substring_index(persons.c.FullName, " ", 1),
        LastName=func.substring_index(persons.c.FullName, " ", -1),
    )
    # use the print function to see the actual SQL command
    print(updateStatement)

    #########################  NEW  ##################################
    # STEP NEW.4
    # Delete a scrabble_initial_games record
    # Delete the records where the winnernewrating has a score less than or equal to 400
    # See: https://docs.sqlalchemy.org/en/21/tutorial/data_update.html#the-update-sql-expression-construct
    minDelete = 400
    deleteStatement = delete(scrabble_games_initial).where(scrabble_games_initial.c.winnernewrating <= minDelete)
    print(deleteStatement)

    # Other version where the scrabble_initial_games records are deleted when
    # both the winnernewrating and losernewrating are less than or equal to 400
    deleteStatement2 = delete(scrabble_games_initial).where(
        scrabble_games_initial.c.winnernewrating <= minDelete).where(
        scrabble_games_initial.c.losernewrating <= minDelete
    )
    print(deleteStatement2)
    #########################  NEW  ##################################

    #########################  NEW  ##################################
    # STEP NEW.5
    # Show the winners tourney, new rating, leaderboard rating along with their First and Last Name
    # Get references to the columns (c) to make the joinColumns syntax smaller
    # Limit the data to the top 10 teams for TourneyID = 9760. Since teams have three players (it seems)
    # the limit is set to 30
    # The distinct keyword is used so that the top thirty unique players are listed. Otherwise we see the same person many times.
    # See: https://docs.sqlalchemy.org/en/21/tutorial/data_update.html#the-update-sql-expression-construct
    TourneyID = 9760
    NumTeams = 10
    MembersPerTeam = 3

    joinStatement = (select(scrabble_games_initial.c.tourneyid,
                            scrabble_games_initial.c.winnerpos,
                            persons.c.FirstName, persons.c.LastName).
                     join(persons, scrabble_games_initial.c.winnerSysId == persons.c.ID).
                     where(scrabble_games_initial.c.tourneyid == TourneyID).
                     distinct().
                     order_by(scrabble_games_initial.c.winnerpos).order_by(persons.c.LastName).
                     order_by(persons.c.FirstName).
                     limit(NumTeams * MembersPerTeam))

    print(joinStatement)

    try:
        # "with" opens the connection and guarantees it is closed when the
        # indented block ends, even if an error happens.
        # Additional reading: https://docs.sqlalchemy.org/en/21/tutorial/dbapi_transactions.html#getting-a-connection
        with (engine.connect() as connection):
            print("Successfully connected to MariaDB!")
            # execute the update statement for New.3
            connection.execute(updateStatement)
            # will not be saved to the database until the commit method is used.
            connection.commit()

            # execute the delete statement for New.4
            connection.execute(deleteStatement2)
            # will not be saved to the database until the commit method is used.
            connection.commit()

            # execute the join statement for New.5
            # Reminder: queries do not require a commit as no changes to the database are being made.
            # Generate the header with the column names (Capitalize the first letter in each name)

            print("======================================")
            print(f"Top ten in the leaderboard for Tournament: {TourneyID}")
            print()
            # This join is a Python method of concatenating the elements of an array to create a string
            print("\tFirst Name Last Name")
            print("======================================")

            results = connection.execute(joinStatement.order_by(persons.c.LastName))
            currentWinnerPos = -1

            for row in results:
                if currentWinnerPos != row.winnerpos:
                    print("-----------------------------------------")
                    print(f"Team at:{row.winnerpos}")
                    currentWinnerPos = row.winnerpos
                print(f"\t{row.FirstName} {row.LastName}")



    except OperationalError as e:
        # Could not connect: wrong credentials, host, port, or the server is not running.
        print(f"Connection error: {e}")
    except ProgrammingError as e:
        # Connected, but the SQL was rejected: misspelled table or column name, etc.
        print(f"SQL error: {e}")
        ######################################## NEW ##############################
        # X. Catching all other SQLAlchemy errors
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        ######################################## NEW ##############################
        # X. Catching all other Python errors
    except Exception as e:
        print(f"Unexpected non-SQLAlchemy error: {e}")


# This line means "run main() only when this file is run directly".
# Without it, importing this file from another program would also run the test.
if __name__ == "__main__":
    main()
