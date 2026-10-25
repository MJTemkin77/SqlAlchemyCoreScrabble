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
from sqlalchemy import create_engine, text, TextClause
from sqlalchemy.engine import URL
from sqlalchemy.exc import OperationalError, ProgrammingError

#########################  NEW  ##################################
# STEP NEW.1
## NEW IMPORTS for SQLAlchemy Core
from sqlalchemy import Table, Column, Integer, String, CHAR, MetaData
from sqlalchemy import select, insert


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

    #########################  NEW  ##################################
    # STEP NEW.3
    # Create the Table Object that matches the Scrabble_Games_Initial table.
    # This code was generated by using Claude Chat although any AI (CoPilot, OpenAI, Perplexity) should be able to this.
    # See the additional Canvas page about code generation.
    # "Table objects are initialized in SQLAlchemy Core in a supplied MetaData object
    # by calling the Table constructor with the table name and metadata; any additional arguments are assumed to be column objects."
    # Additional Reading: https://docs.sqlalchemy.org/en/21/tutorial/metadata.html#components-of-table
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
        Column("winnerSysId", Integer, nullable=False, server_default=text("-1")),
        Column("loserSysId", Integer, nullable=False, server_default=text("-1")),
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

    minimum_score = input("Enter the lowest winner score: ")
    if minimum_score.isnumeric():
        minimum_score = int(minimum_score)
    else:
        minimum_score = 0

    # -----------------------------------------------------------------------
    # Section 4 - Connect and run a query
    # -----------------------------------------------------------------------
    # Try this first: run the program as is. Then break it on purpose by
    # changing the password, port, host, or database name and read the error.
    # For example, a wrong port produces something like:
    #   sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError)
    #   (2003, "Can't connect to MySQL server on 'localhost'")
    try:
        # "with" opens the connection and guarantees it is closed when the
        # indented block ends, even if an error happens.
        # Additional reading: https://docs.sqlalchemy.org/en/21/tutorial/dbapi_transactions.html#getting-a-connection
        with (engine.connect() as connection):
            print("Successfully connected to MariaDB!")

            #########################  NEW  ##################################
            # STEP NEW.4
            # NOTE: Using A and B to identify the two different types of using SQL Alchemy
            # Use the Select Syntax SQL Expresssion Construct (B) rather than using the connection for  statement execution (A)
            # The following reading refers to the first way that we learned to retrieve data from the database.
            # Additional reading: https://docs.sqlalchemy.org/en/21/tutorial/dbapi_transactions.html#basics-of-statement-execution  (A)
            # The next reading refers to the select() SQL Expresssion Construct (B)
            # https://docs.sqlalchemy.org/en/21/tutorial/data_select.html#the-select-sql-expression-construct

            # Retrieve all games where the winning score is at least some value.
            # :winnerscore is a placeholder. The value is passed separately, so
            # it is always treated as data and never as SQL. This is what
            # protects an application from SQL injection. Never build SQL by
            # gluing user input into the string.
            """
            # THIS CODE is commented out with the multi-line comment that starts at line 205 and ends at line 213
            # Method A --using the connection for  statement execution  (A)
            statement = text(
                "SELECT gameid, tourneyid, winnerSysId, loserSysId, winnerscore, loserscore "
                "FROM scrabble_games_initial "
                "WHERE winnerscore >= :winnerscore Limit 5"
            )
            """
            # Method B -- Use the Select Syntax SQL Expresssion Construct (B)
            # The following statement will retrieve all the scrabble_games_intial columns.
            # This follows the example at https://docs.sqlalchemy.org/en/21/tutorial/data_select.html#setting-the-columns-and-from-clause
            # .where(scrabble_games_initial.c.winnerscore > minimum_score).limit(5)
            results = connection.execute(select(scrabble_games_initial))

            # Iterate through the results for the first five records in order to limit output in the console.
            print("Iterating through the results")
            i = 0
            for row in results:
                print(row.gameid, row.winnerscore)
                i = i + 1
                if i > 5:
                    break
            # Another way is to use the .mappings() method on results and
            # then use the Table.c accessor. An advantage of the Table.c accessor is
            # when there is a join and there are column names in both tables in the join that have the same name.
            # The Table.c accessor acts like an alias in SQL.
            # See: https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.c
            results = connection.execute(select(scrabble_games_initial))
            i = 0
            for row in results.mappings():
                print(row[scrabble_games_initial.c.gameid], row[scrabble_games_initial.c.winnerscore])
                i = i + 1
                if i > 5:
                    break

            # There are examples where be build up the statement using variables.
            # For example the previous could be written by saving the select expression to a variable.
            stmt = select(scrabble_games_initial)
            # Notice that the execute uses the select expression
            results = connection.execute(stmt)
            # Retrieving the data remains the same.
            # Iterate through the results for the first five records in order to limit output in the console.
            i = 0
            for row in results.mappings():
                print(row["gameid"], row["winnerscore"])
                i = i + 1
                if i > 5:
                    break

            #########################  NEW  ##################################
            # STEP NEW.5
            # Specifying columns using the Tables c reference

            stmt = select(scrabble_games_initial.c.gameid,
                          scrabble_games_initial.c.winnername,
                          scrabble_games_initial.c.winnerscore,
                          scrabble_games_initial.c.losername,
                          scrabble_games_initial.c.loserscore)

            results = connection.execute(stmt)
            # Retrieving the data remains the same.
            # Iterate through the results for the first five records in order to limit output in the console.
            i = 0
            for row in results.mappings():
                print(row[scrabble_games_initial.c.gameid], ",",
                      row[scrabble_games_initial.c.winnername], ",",
                      row[scrabble_games_initial.c.winnerscore], ",",
                      row[scrabble_games_initial.c.losername], ",",
                      row[scrabble_games_initial.c.loserscore], ",")
                i = i + 1
                if i > 5:
                    break

            # Alternate: using a variable that refers to scrabble_games_initial.c so that the syntax is shorter.
            print("Print using an shorthand notation")
            c = scrabble_games_initial.c
            stmt = select(c.gameid,
                          c.winnername,
                          c.winnerscore,
                          c.losername,
                          c.loserscore)
            results = connection.execute(stmt)
            i = 0
            for row in results.mappings():
                print(row[c.gameid], ",",
                      row[c.winnername], ",",
                      row[c.winnerscore], ",",
                      row[c.losername], ",",
                      row[c.loserscore])
                ",",
                i = i + 1
                if i > 5:
                    break

            # The second argument supplies the placeholder values as a dictionary.
            # result = connection.execute(stmt )
            result = connection.execute(stmt)
            # {"winnerscore": minimum_score}

            #########################  NEW  ##################################
            # STEP NEW.6
            # Using the where clause,limit and order by
            # Where: https://docs.sqlalchemy.org/en/21/tutorial/data_select.html#the-where-clause
            # Order By: https://docs.sqlalchemy.org/en/21/tutorial/data_select.html#order-by
            stmt = select(c.gameid,
                          c.winnername,
                          c.winnerscore,
                          c.losername,
                          c.loserscore).where(c.winnerscore < minimum_score).order_by(
                c.winnerscore.desc()).order_by(c.winnername).limit(5)

            results = connection.execute(stmt)

            print("Print using a where clause, order_by, and limit to the first 5")
            for row in results.mappings():
                print(row[c.gameid], ",",
                      row[c.winnername], ",",
                      row[c.winnerscore], ",",
                      row[c.losername], ",",
                      row[c.loserscore])

            #########################  NEW  ##################################
            # STEP NEW.7
            # Use the above query and ask the user if we want to schedule a new match by inserting
            # the two players into a new match record.
            # Before this is done, notice that a Match Table definition has also been created below Scrabble_Games_Initial
            # https://docs.sqlalchemy.org/en/21/tutorial/data_insert.html#tutorial-core-insert
            #

            stmt = select(c.gameid,
                          c.winnername,c.winnerSysId,
                          c.winnerscore,
                          c.losername,c.loserSysId,
                          c.loserscore).where(c.winnerscore < minimum_score).order_by(
                c.winnerscore.desc()).order_by(c.winnername).limit(5)

            results = connection.execute(stmt)
            print("Ask if there needs to be a rematch")
            for row in results.mappings():
                print(row[c.gameid], ",",
                      row[c.winnername], ",",
                      row[c.winnerscore], ",",
                      row[c.losername], ",",
                      row[c.loserscore])

                ans = input("Want a rematch")
                if ans == "Y":
                    statement = insert(matches).values(PlayerA_Id=row[c.winnerSysId], PlayerB_Id=row[c.loserSysId])
                    #statement = text("Insert into matches (PlayerA_Id, PlayerB_Id) values (:playerA, :playerB)")
                    result = connection.execute(statement)
                    connection.commit()
                    print(result)




    except OperationalError as e:
        # Could not connect: wrong credentials, host, port, or the server is not running.
        print(f"Connection error: {e}")
    except ProgrammingError as e:
        # Connected, but the SQL was rejected: misspelled table or column name, etc.
        print(f"SQL error: {e}")

    print("End database connection test")


# This line means "run main() only when this file is run directly".
# Without it, importing this file from another program would also run the test.
if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# Section 5 (optional) - The same idea with SQLite
# ---------------------------------------------------------------------------
# SQLite has no server, username, password, host, or port. The "database" is a
# single file, so the only thing that changes is the URL. Python includes SQLite
# support, so there is nothing to install.
#
#     engine = create_engine("sqlite:///scrabble.db", echo=False)
#
# Everything after that (connect, text(), execute, loop over the rows) is
# exactly the same code. That is the point of using SQLAlchemy: one way of
# working, many databases.
