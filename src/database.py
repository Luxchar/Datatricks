import sqlite3
from logger import Logger

class Database:
    """ Database class to access and modify the database"""
    def __init__(self, url: str, logger: Logger):
        self.logger = logger
        self.connection = self.connect_to_database(url)
        
    def connect_to_database(self, url: str):
        """ Connect to the database"""
        try:
            connection = sqlite3.connect(url)
            self.logger.log("Connected to database", "INFO")
            return connection
        except Exception as e:
            self.logger.log("Error connecting to database: " + str(e), "ERROR")
            
    def database_request(self, request):
        """Execute a request on the database and return the result"""
        try:
            cur = self.connection.cursor()
            cur.execute(request)
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as e:
            self.logger.log("Error executing request: " + str(e), "ERROR")

    def add_data(self):
        """ Add data to the database """
        self.database_request("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")

    def clear(self):
        """ Clear the database """ # drop everything
        self.database_request("DROP TABLE users")