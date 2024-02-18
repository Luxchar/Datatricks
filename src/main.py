from logger import Logger
from database import Database
from app import App

def main():
    """ Main function """

    try:
        logger = Logger() # init custom logger
        logger.log("Application started", "INFO")

        db = Database('./database.db', logger) # init database
        app = App(db) # init app
        logger.set_log_box(app.log_box) # set log box to logger

        app.mainloop()
        logger.log("Application closed", "INFO")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
