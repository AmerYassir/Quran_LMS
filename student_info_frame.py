from tkinter import messagebox
from general_frame import GeneralFrame
import tkinter as tk
from tkinter import ttk
class StudentInfoFrame(GeneralFrame):
    def __init__(self, master,config):
        super().__init__(master,config)
        # Your StudentInfoFrame initialization code here
        self.create_UI()
    def create_UI(self):
        self.student_info_frame = ttk.Frame(self)
        self.student_info_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create labels and entry fields for student information
        self.student_name_label = ttk.Label(self.student_info_frame, text=": اسم الطالب")
        self.student_name_label.pack(side=tk.RIGHT, padx=5, pady=5)

        self.student_name_entry = ttk.Entry(self.student_info_frame)
        self.student_name_entry.pack(side=tk.RIGHT, padx=5, pady=5)

        self.student_age_label = ttk.Label(self.student_info_frame, text=": عمر الطالب")
        self.student_age_label.pack(side=tk.RIGHT, padx=5, pady=5)

        self.student_age_entry = ttk.Entry(self.student_info_frame)
        self.student_age_entry.pack(side=tk.RIGHT, padx=5, pady=5)

        self.student_level_label = ttk.Label(self.student_info_frame, text=": مستوى الطالب")
        self.student_level_label.pack(side=tk.RIGHT, padx=5, pady=5)

        self.student_level_entry = ttk.Entry(self.student_info_frame)
        self.student_level_entry.pack(side=tk.RIGHT, padx=5, pady=5)

        # Create a button to add a new student
        self.add_student_button = ttk.Button(self.student_info_frame, text="اضف الطالب", command=self.add_item)
        self.add_student_button.pack(side=tk.TOP, padx=5, pady=5)

        self.delete_student_button = ttk.Button(self.student_info_frame, text="امسح اطالب", command=self.delete_item)
        self.delete_student_button.pack(side=tk.TOP, padx=5, pady=5)

    def add_item(self):
        # Retrieve values from entry fields
        student_name = self.student_name_entry.get()
        student_age = self.student_age_entry.get()
        student_level = self.student_level_entry.get()

        # Check if all fields are filled
        if not all([student_name, student_age, student_level]):
            # Display an error message or handle the case where not all fields are filled
            # For simplicity, we print an error message to the console
            print("Please fill in all fields.")
            messagebox.showinfo("Info", "برجاء ملئ جميع المدخلات")
            return

        # Insert the new student into the 'students' table
        self.DB.c.execute("INSERT INTO students (name, age, level) VALUES (?, ?, ?)", (student_name, student_age, student_level))
        self.DB.conn.commit()

        # Clear the entry fields
        self.student_name_entry.delete(0, tk.END)
        self.student_age_entry.delete(0, tk.END)
        self.student_level_entry.delete(0, tk.END)

        current_items = self.combobox['values']
    
        # Add the new item to the list
        updated_items = list(current_items) + [student_name]
        
        # Update the Combobox with the new list of items
        self.combobox['values'] = updated_items
        # Optionally, update the display or perform other actions
        # For example, you might want to refresh the displayed list of students
        # You can call a function similar to retrieve_student_progress here

        # For simplicity, we print a message to the console
        print(f"Student '{student_name}' added successfully.")   
        messagebox.showinfo("Info",f"{student_name} \nتم تسجيل الطالب   ") 
    
    def delete_item(self):
        # Delete selected rows from the 'progress' table

        # Get selected items from the treeview
        selected_items = self.combobox.get()

        if not selected_items:
            # If no item is selected, display an error message or handle it as needed
            # For simplicity, we print an error message to the console
            print("No item selected for deletion.")
            messagebox.showinfo("Info", "اختر عنصرا اولا ")
            return

        
        # Delete the row from the 'progress' table
        self.DB.c.execute("DELETE FROM students WHERE name=?", (selected_items,))
        self.DB.conn.commit()
        messagebox.showinfo("Info", f"{selected_items}\nتم مسح الطالب ")
        # Get the list of current values
        current_items = list(self.combobox['values'])
        
        # Get the selected item
        selected_item = self.combobox.get()

        # Check if an item is selected
        if selected_item:
            # Remove the selected item from the list
            current_items.remove(selected_item)

            # Update the Combobox with the new list
            self.combobox["values"]=current_items


