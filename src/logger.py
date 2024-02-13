import logging
import tkinter as tk
import customtkinter
import sys

logging.basicConfig(level=logging.INFO)

# add color to logging
logging.addLevelName(logging.INFO, "\033[1;32m%s\033[1;0m" % logging.getLevelName(logging.INFO))
logging.addLevelName(logging.WARNING, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName(logging.ERROR, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
logging.addLevelName(logging.DEBUG, "\033[1;34m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))

class Logger(logging.StreamHandler):
    """ Logger class to handle logging """
    def __init__(self):
        logging.StreamHandler.__init__(self) # initialize parent
        self.log_box = None
        
    def set_log_box(self, log_box):
        """ Set the log box """
        self.log_box = log_box

    def log(self, msg, level):
        """ print log message """
        try:
            msg = self.format_msg(msg, level)
            if self.log_box:
                self.log_box.configure(state="normal")
                self.log_box.delete(0, "end")  # This will clear the log_box
                self.log_box.insert("end", msg)
                self.log_box.configure(state="disabled")
        except Exception as e:
            sys.exit(1)
        
        
    def format_msg(self, msg, level):
        """ Format log message """
        if level == "INFO":
            logging.info(msg)
            return f"{msg}"
        if level == "ERROR":
            logging.error(msg)
            return f"{msg}"
        return f"{level}: {msg}"