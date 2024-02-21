import sqlite3
from logger import Logger
import json
import pandas as pd

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
            return None
            
    def database_request(self, request, params=None):
        """Execute a request on the database and return the result"""
        try:
            cur = self.connection.cursor()
            if params:
                cur.execute(request, params)
            else:
                cur.execute(request)
            data = cur.fetchall()
            if request.lower().startswith(("insert", "update", "delete")):
                self.connection.commit()  # commit the changes
            cur.close()
            return data
        except Exception as e:
            self.logger.log("Error executing request: " + str(e), "ERROR")
            return None
        
    def get_data_from_column(self, column: str):
        """ Get data from a column"""
        data = self.database_request("SELECT " + column + " FROM data")
        if data is None:
            return None
        return [d[0] for d in data]

    def get_values(self):
        """ Get all columns names from the database """
        data = self.database_request("PRAGMA table_info(data)")
        if data is None:
            return None
        return [d[1] for d in data]

    def add_data(self, file_path: str):
        """ Add data to the database """
        
        # check if table data has data
        if self.database_request("SELECT * FROM data") is not None:
            self.logger.log("Database already has data", "INFO")
            return

        # read the data from the file
        df = pd.read_json(file_path)

        # convert lists to strings
        df = df.map(lambda x: json.dumps(x) if isinstance(x, list) else x)

        # add data to the database
        df.to_sql('data', self.connection, if_exists='replace', index=False)
        self.logger.log("Data added to database", "INFO")

    def clear(self):
        """ Clear the database """ # drop everything
        self.database_request("DROP TABLE data")
        self.logger.log("Database cleared", "INFO")