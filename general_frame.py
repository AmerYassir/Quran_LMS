import tkinter as tk
from tkinter import ttk
from DataBase import DataBase

class GeneralFrame(ttk.Frame):

    def __init__(self, master,config):
        super().__init__(master)
        self.master = master
        self.config=config
        self.DB=config.DB
        self.combobox=config.combobox
        self.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def show_frame(self):
        self.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def hide_frame(self):
        self.pack_forget()
    def create_UI(self):
        pass
    def delete_item(self):
        pass
    def add_item(self):
        pass    
    def  retrieve_data(self):
        pass
