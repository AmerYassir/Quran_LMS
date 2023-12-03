from datetime import datetime
from general_frame import GeneralFrame
import tkinter as tk
from tkinter import ttk
class StudentSessionsFrame(GeneralFrame):
    def __init__(self, master,config):
        super().__init__(master,config)
        self.create_UI()

    def create_UI(self):
        self.sessions_frame=ttk.Frame(self)
        self.sessions_frame.pack(side=tk.TOP)

        self.delete_session_button = ttk.Button(self.sessions_frame, text="Delete Progress", command=self.delete_item)
        self.add_session_button = ttk.Button(self.sessions_frame, text="add Progress", command=self.add_item)

        self.delete_session_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.add_session_button.pack(side=tk.LEFT, padx=5, pady=5)
        # Create a treeview to display student progress
        self.student_sessions_treeview = ttk.Treeview(self, columns=("id","date","notes"))
        self.student_sessions_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Set column headings
        self.student_sessions_treeview.heading("#0", text="index")  # The default ID column
        self.student_sessions_treeview.heading("id", text="session_ID")
        self.student_sessions_treeview.heading("date", text="Date")
        self.student_sessions_treeview.heading("notes", text="Notes")

        

        self.notes_label = ttk.Label(self.sessions_frame, text="Notes:")
        self.notes_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.notes_entry = ttk.Entry(self.sessions_frame)
        self.notes_entry.pack(side=tk.LEFT, padx=5, pady=5)
    
    def add_item(self):
        notes=self.notes_entry.get()
        date=str(datetime.today().date())

        # Check if all fields are filled
        if not all([notes, date]):
            # Display an error message or handle the case where not all fields are filled
            # For simplicity, we print an error message to the console
            print("Please fill in all fields.")
            return

        # Insert the new student into the 'students' table
        self.DB.c.execute("INSERT INTO sessions (date,notes) VALUES (?, ?)", (date,notes))
        self.DB.conn.commit()
        print("added notes succyesful")
        # Clear the entry fields
        self.notes_entry.delete(0, tk.END)

    def retrieve_data(self):
        # Clear existing items in the treeview
        for item in self.student_sessions_treeview.get_children():
            self.student_sessions_treeview.delete(item)
        self.DB.c.execute("SELECT * FROM sessions")
        progress_data = self.DB.c.fetchall()
        for row in progress_data:
            #row=list(row)
            print(row)
            self.student_sessions_treeview.insert("", "end", values=row)
