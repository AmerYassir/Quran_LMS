from datetime import datetime
from general_frame import GeneralFrame
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class StudentProgressFrame(GeneralFrame):

    def __init__(self, master,config):
        super().__init__(master,config)
        # Your StudentProgressFrame initialization code here
        #self.pack(side=tk.BOTTOM)
        self.create_UI()
        

    def create_UI(self):
        self.student_progress_entry_frame=ttk.Frame(self)
        self.student_progress_entry_frame.pack(side=tk.TOP)

        self.delete_progress_button = ttk.Button(self.student_progress_entry_frame, text="مسح عنصر", command=self.delete_item)
        self.add_progress_button = ttk.Button(self.student_progress_entry_frame, text="اضافة عنصر", command=self.add_item)

        self.delete_progress_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.add_progress_button.pack(side=tk.LEFT, padx=5, pady=5)
        # Create a treeview to display student progress
        self.student_progress_treeview = ttk.Treeview(self, columns=("std_ID","Surah", "Ayat Start", "Ayat End", "Date"))
        self.student_progress_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Set column headings
        self.student_progress_treeview.heading("#0", text="رقم")  # The default ID column
        self.student_progress_treeview.heading("std_ID", text="اسم الطالب")
        self.student_progress_treeview.heading("Surah", text="السورة")
        self.student_progress_treeview.heading("Ayat Start", text="اية البدأ")
        self.student_progress_treeview.heading("Ayat End", text="اية الانتهاء")
        self.student_progress_treeview.heading("Date", text="التاريخ")
        self.student_progress_treeview.column('#0', minwidth = 0, width = 0, stretch = True)
        
        
        self.progress_surah_label = ttk.Label(self.student_progress_entry_frame, text=": السورة")
        self.progress_surah_label.pack(side=tk.RIGHT, padx=5, pady=5)

        self.progress_surah_entry = ttk.Entry(self.student_progress_entry_frame)
        self.progress_surah_entry.pack(side=tk.RIGHT, padx=5, pady=5)

        self.progress_ayat_start_label = ttk.Label(self.student_progress_entry_frame, text=": اية البدأ")
        self.progress_ayat_start_label.pack(side=tk.RIGHT, padx=5, pady=5)

        self.progress_ayat_start_entry = ttk.Entry(self.student_progress_entry_frame)
        self.progress_ayat_start_entry.pack(side=tk.RIGHT, padx=5, pady=5)

        self.progress_ayat_end_label = ttk.Label(self.student_progress_entry_frame, text=": اية الانتهاء")
        self.progress_ayat_end_label.pack(side=tk.RIGHT, padx=5, pady=5)

        self.progress_ayat_end_entry = ttk.Entry(self.student_progress_entry_frame)
        self.progress_ayat_end_entry.pack(side=tk.RIGHT, padx=5, pady=5)

    def delete_item(self):
        # Delete selected rows from the 'progress' table

        # Get selected items from the treeview
        selected_items = self.student_progress_treeview.selection()

        if not selected_items:
            # If no item is selected, display an error message or handle it as needed
            # For simplicity, we print an error message to the console
            print("No item selected for deletion.")
            messagebox.showinfo("Info", "اختر عنصرا اولا ")
            return

        for item in selected_items:
            # Retrieve the values of the selected row
            values = self.student_progress_treeview.item(item, 'values')

            # Extract the relevant information (assuming 'id' is the first column)
            progress_name = values[0]

            # Delete the row from the 'progress' table
            self.DB.c.execute("DELETE FROM progress WHERE student_name=?", (progress_name,))
            self.DB.conn.commit()

            # Remove the item from the treeview
            self.student_progress_treeview.delete(item)

        # Optionally, update the display or perform other actions
        # For example, you might want to refresh the displayed list of students
        # You can call a function similar to retrieve_student_progress here

        # For simplicity, we print a message to the console
        print("Selected items deleted successfully.")
        messagebox.showinfo("Info", "تم الحذف بنجاح ")

    def add_item(self):
        # Retrieve values from entry fields
        surah = self.progress_surah_entry.get()
        ayat_start = self.progress_ayat_start_entry.get()
        ayat_end = self.progress_ayat_end_entry.get()
        date=str(datetime.today().date())
        name=self.combobox.get()
        print(name)
        
        # Check if all fields are filled
        if not all([surah, ayat_start, ayat_end]):
            # Display an error message or handle the case where not all fields are filled
            # For simplicity, we print an error message to the console
            print("Please fill in all fields.")
            messagebox.showinfo("Info", "برجاء ملئ جميع المدخلات")
            return

        # Insert the new student into the 'students' table
        self.DB.c.execute("INSERT INTO progress (student_name,surah, ayat_start, ayat_end,date) VALUES (?, ?, ?,?,?)", (name,surah, ayat_start, ayat_end,date))
        self.DB.conn.commit()

        # Clear the entry fields
        self.progress_surah_entry.delete(0, tk.END)
        self.progress_ayat_start_entry.delete(0, tk.END)
        self.progress_ayat_end_entry.delete(0, tk.END)
    
    def retrieve_data(self,name=""):
        # Clear existing items in the treeview
        for item in self.student_progress_treeview.get_children():
            self.student_progress_treeview.delete(item)
        if name !="":
            self.DB.c.execute("SELECT * FROM progress where student_name=?",(name,))
            progress_data = self.DB.c.fetchall()
        else:    
            # Retrieve data from the 'progress' table
            self.DB.c.execute("SELECT * FROM progress")
            progress_data = self.DB.c.fetchall()

        #progress_data=list(progress_data[0])[1:]
        # Display data in the treeview
        for row in progress_data:
            row=list(row)
            print(row)
            self.student_progress_treeview.insert("", "end", values=row[1:])
            


