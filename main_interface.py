import tkinter as tk
from tkinter import ttk
import sqlite3

class QuranLMSApp:
    def __init__(self, master):
        self.master = master
        master.title("Quran LMS")

        # Connect to the SQLite database
        self.conn = sqlite3.connect('quran_lms.db')
        self.c = self.conn.cursor()

        # Create tables if they don't exist
        self.create_tables()

        # Create a frame for buttons at the top
        self.button_frame = ttk.Frame(self.master)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        self.kid_combobox = ttk.Combobox(self.button_frame, values=self.retrieve_kid_names())
        self.kid_combobox.set("Select Kid")
        self.kid_combobox.pack(side=tk.LEFT, padx=5, pady=5)

        # Create frames
        self.create_student_info_frame()
        self.create_student_progress_frame()
        self.create_student_achievements_frame()
        self.create_student_sessions_frame()
        self.show_student_info()
        # Pack the default frame (student_info_frame)
        self.student_info_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create buttons to switch between frames
        self.create_button("Show Student Info", self.show_student_info)
        self.create_button("Show Student Progress", self.show_student_progress)
        self.create_button("Show Student Achievements", self.show_student_achievements)
        self.create_button("Show Student Sessions", self.show_student_sessions)

        # Create a button to retrieve and display student progress
        
        

    def create_tables(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            level TEXT NOT NULL
        )""")

        self.c.execute("""CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            surah TEXT NOT NULL,
            ayat_start INTEGER NOT NULL,
            ayat_end INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )""")

        self.c.execute("""CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            achievement TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )""")

        self.c.execute("""CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            duration INTEGER NOT NULL,
            notes TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )""")

        self.conn.commit()

    def create_button(self, text, command):
        button = ttk.Button(self.button_frame, text=text, command=command)
        button.pack(side=tk.LEFT, padx=5, pady=5)

    def show_student_info(self):
        # Show the student_info_frame and hide others
        self.student_info_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.student_progress_frame.pack_forget()
        self.student_achievements_frame.pack_forget()
        self.student_sessions_frame.pack_forget()

    def show_student_progress(self):
        # Show the student_progress_frame and hide others
        self.student_info_frame.pack_forget()
        self.student_progress_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.student_achievements_frame.pack_forget()
        self.student_sessions_frame.pack_forget()

        # Create a button to delete selected rows from the progress table
        
        # Optionally, update the displayed progress
        self.retrieve_student_progress()

    def show_student_achievements(self):
        # Show the student_achievements_frame and hide others
        self.student_info_frame.pack_forget()
        self.student_progress_frame.pack_forget()
        self.student_achievements_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.student_sessions_frame.pack_forget()

        # Optionally, update the displayed achievements
        # Call a function similar to retrieve_student_achievements here

    def show_student_sessions(self):
        # Show the student_sessions_frame and hide others
        self.student_info_frame.pack_forget()
        self.student_progress_frame.pack_forget()
        self.student_achievements_frame.pack_forget()
        self.student_sessions_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        

    def create_student_info_frame(self):
        #region student info frame
        self.student_info_frame = ttk.Frame(self.master)
        self.student_info_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create labels and entry fields for student information
        self.student_name_label = ttk.Label(self.student_info_frame, text="Student Name:")
        self.student_name_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.student_name_entry = ttk.Entry(self.student_info_frame)
        self.student_name_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.student_age_label = ttk.Label(self.student_info_frame, text="Student Age:")
        self.student_age_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.student_age_entry = ttk.Entry(self.student_info_frame)
        self.student_age_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.student_level_label = ttk.Label(self.student_info_frame, text="Student Level:")
        self.student_level_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.student_level_entry = ttk.Entry(self.student_info_frame)
        self.student_level_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # Create a button to add a new student
        self.add_student_button = ttk.Button(self.student_info_frame, text="add student", command=self.add_student)
        self.add_student_button.pack(side=tk.TOP, padx=5, pady=5)

        
        #endregion student info frame

    def add_student(self):
        # Retrieve values from entry fields
        student_name = self.student_name_entry.get()
        student_age = self.student_age_entry.get()
        student_level = self.student_level_entry.get()

        # Check if all fields are filled
        if not all([student_name, student_age, student_level]):
            # Display an error message or handle the case where not all fields are filled
            # For simplicity, we print an error message to the console
            print("Please fill in all fields.")
            return

        # Insert the new student into the 'students' table
        self.c.execute("INSERT INTO students (name, age, level) VALUES (?, ?, ?)", (student_name, student_age, student_level))
        self.conn.commit()

        # Clear the entry fields
        self.student_name_entry.delete(0, tk.END)
        self.student_age_entry.delete(0, tk.END)
        self.student_level_entry.delete(0, tk.END)

        # Optionally, update the display or perform other actions
        # For example, you might want to refresh the displayed list of students
        # You can call a function similar to retrieve_student_progress here

        # For simplicity, we print a message to the console
        print(f"Student '{student_name}' added successfully.")

    def create_student_progress_frame(self):
        self.student_progress_frame = ttk.Frame(self.master)
        self.student_progress_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.delete_progress_button = ttk.Button(self.student_progress_frame, text="Delete Progress", command=self.delete_selected_progress)
        self.retrieve_progress_button = ttk.Button(self.student_progress_frame, text="Retrieve Progress", command=self.retrieve_student_progress)
        self.retrieve_progress_button.pack(side=tk.TOP, padx=5, pady=5)
        self.delete_progress_button.pack(side=tk.TOP, padx=5, pady=5)
        # Create a treeview to display student progress
        self.student_progress_treeview = ttk.Treeview(self.student_progress_frame, columns=("Surah", "Ayat Start", "Ayat End", "Date"))
        self.student_progress_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Set column headings
        self.student_progress_treeview.heading("#0", text="ID")  # The default ID column
        #self.student_progress_treeview.heading("ID", text="ID")
        self.student_progress_treeview.heading("Surah", text="Surah")
        self.student_progress_treeview.heading("Ayat Start", text="Ayat Start")
        self.student_progress_treeview.heading("Ayat End", text="Ayat End")
        self.student_progress_treeview.heading("Date", text="Date")
    def create_student_achievements_frame(self):
        self.student_achievements_frame = ttk.Frame(self.master)
        self.student_achievements_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a treeview to display student achievements
        self.student_achievements_treeview = ttk.Treeview(self.student_achievements_frame, columns=("Achievement", "Date"))
        self.student_achievements_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def create_student_sessions_frame(self):
        self.student_sessions_frame = ttk.Frame(self.master)
        self.student_sessions_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a treeview to display student sessions
        # self.student_sessions_treeview = ttk.Treeview(self.student_sessions_frame, columns=("...

    def retrieve_kid_names(self):
        self.c.execute("SELECT name FROM students")
        students_data = self.c.fetchall()
        return students_data
    def retrieve_student_progress(self):
        # Retrieve and display student progress data

        # Clear existing items in the treeview
        for item in self.student_progress_treeview.get_children():
            self.student_progress_treeview.delete(item)

        # Retrieve data from the 'progress' table
        self.c.execute("SELECT * FROM progress")
        progress_data = self.c.fetchall()

        print(progress_data)
        # Display data in the treeview
        for row in progress_data:
            self.student_progress_treeview.insert("", "end", values=row)

    def delete_selected_progress(self):
        # Delete selected rows from the 'progress' table

        # Get selected items from the treeview
        selected_items = self.student_progress_treeview.selection()

        if not selected_items:
            # If no item is selected, display an error message or handle it as needed
            # For simplicity, we print an error message to the console
            print("No item selected for deletion.")
            return

        for item in selected_items:
            # Retrieve the values of the selected row
            values = self.student_progress_treeview.item(item, 'values')

            # Extract the relevant information (assuming 'id' is the first column)
            progress_id = values[0]

            # Delete the row from the 'progress' table
            self.c.execute("DELETE FROM progress WHERE id=?", (progress_id,))
            self.conn.commit()

            # Remove the item from the treeview
            self.student_progress_treeview.delete(item)

        # Optionally, update the display or perform other actions
        # For example, you might want to refresh the displayed list of students
        # You can call a function similar to retrieve_student_progress here

        # For simplicity, we print a message to the console
        print("Selected items deleted successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuranLMSApp(root)
    root.mainloop()
