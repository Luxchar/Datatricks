import tkinter as tk
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from database import Database
from tkinter import messagebox

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    """ Main application window """
    def __init__(self, db: Database):
        super().__init__()

        self.db = db

        # configure window
        self.title("Datatricks")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Datatricks", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.get_file_path, text="Download Data")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=db.clear, text="Clear Database")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create logs box
        self.log_box = customtkinter.CTkEntry(self)
        self.log_box.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.log_box.insert(0, "Logs will appear here")
        self.log_box.configure(state="readonly")
        
        self.combobox_1 = customtkinter.CTkComboBox(self,values=db.get_values(), command=self.plot_data)
        self.combobox_1.grid(row=0, column=1, padx=20, pady=(10, 10))
        
        self.combobox_2 = customtkinter.CTkComboBox(self,values=db.get_values(), command=self.plot_data)
        self.combobox_2.grid(row=0, column=2, padx=20, pady=(10, 10))

        # create plot frame
        self.plot_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.plot_frame.grid(row=1, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.plot_frame.grid_columnconfigure(0, weight=1)
        self.plot_frame.grid_rowconfigure(0, weight=1)

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        
    def plot_data(self):
        """ Plot data from the database """
        column_1 = self.combobox_1.get()
        column_2 = ""
        
        if column_1 == "" or column_2 == "":
            messagebox.showerror("Error", "Please select columns")
            return
        
        row1 = self.db.get_data_from_column(column_1)
        row2 = self.db.get_data_from_column(column_2)
        if row1 is None or row2 is None:
            messagebox.showerror("Error", "Error getting data from database")
            return
        
        data = pd.DataFrame({column_1: row1, column_2: row2})
        fig, ax = plt.subplots()
        ax.plot(data["x"], data["y"])
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Data Plot")
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def get_file_path(self):
        """ Open a CTkFileDialog """
        dialog = tk.filedialog.askopenfilename()
        self.db.add_data(dialog)

    def open_input_dialog_event(self):
        """ Open a CTkInputDialog """
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """ Change the appearance mode """
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        """ Change the UI scaling """
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        """" Sidebar button click event """
        print("sidebar_button click")