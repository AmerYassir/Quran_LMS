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

        
        #self.sessions_frame.grid_columnconfigure(0, weight=1)

        self.delete_session_button = ttk.Button(self.sessions_frame, text="امسح العنصر", command=self.delete_item)
        self.add_session_button = ttk.Button(self.sessions_frame, text="اضف عنصر", command=self.add_item)

        self.delete_session_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.add_session_button.pack(side=tk.RIGHT, padx=5, pady=5)
        # Create a treeview to display student progress
        self.student_sessions_treeview = ttk.Treeview(self, columns=("id","date","notes"))
        self.student_sessions_treeview.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        #self.student_sessions_treeview.grid(row = 0, column = 0, sticky='we')
        # Set column headings
        self.student_sessions_treeview.heading("#0", text="")  # The default ID column
        self.student_sessions_treeview.heading("id", text="رقم الحصة")
        self.student_sessions_treeview.heading("date", text="التاريخ")
        self.student_sessions_treeview.heading("notes", text="ملاحظات")

        self.student_sessions_treeview.column('#0', minwidth = 0, width = 0, stretch = True)
        self.student_sessions_treeview.column('#1', minwidth = 70, width = 70, stretch = True)
        self.student_sessions_treeview.column('#2', minwidth = 70, width = 70, stretch = True)  # Try to change the value of stretch here.
        self.student_sessions_treeview.column('#3', minwidth = 70, width = 500, stretch = True)
        #self.student_sessions_treeview.column('#4', minwidth = 70, width = 70, stretch = True)

        self.notes_label = ttk.Label(self.sessions_frame, text=": ملاحظات")
        self.notes_label.pack(side=tk.RIGHT, padx=5, pady=5)

        self.notes_entry = ttk.Entry(self.sessions_frame)
        self.notes_entry.pack(side=tk.RIGHT, padx=5, pady=5)
    
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
            max_text_length = max(len(text) for text in row[2])
            #s#elf.student_sessions_treeview.columnconfigure(0, stretch='pad')

    def delete_item(self):
        # Delete selected rows from the 'progress' table

        # Get selected items from the treeview
        selected_items = self.student_sessions_treeview.selection()

        if not selected_items:
            # If no item is selected, display an error message or handle it as needed
            # For simplicity, we print an error message to the console
            print("No item selected for deletion.")
            return

        for item in selected_items:
            # Retrieve the values of the selected row
            values = self.student_sessions_treeview.item(item, 'values')

            # Extract the relevant information (assuming 'id' is the first column)
            progress_name = values[0]

            # Delete the row from the 'progress' table
            self.DB.c.execute("DELETE FROM sessions WHERE id=?", (progress_name,))
            self.DB.conn.commit()

            # Remove the item from the treeview
            self.student_sessions_treeview.delete(item)

        # Optionally, update the display or perform other actions
        # For example, you might want to refresh the displayed list of students
        # You can call a function similar to retrieve_student_progress here

        # For simplicity, we print a message to the console
        print("Selected items deleted successfully.")
