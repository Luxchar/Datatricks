from logger import Logger
from database import Database
from app import App

def main():
    """ Main function """
      
    # init custom logger
    logger = Logger()
    logger.log("Application started", "INFO")
    
    db = Database('./database.db', logger)
    app = App(db)
    logger.set_log_box(app.log_box)
    
    app.mainloop()
    logger.log("Application closed", "INFO")

if __name__ == "__main__":
    main()
