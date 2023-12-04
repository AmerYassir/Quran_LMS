import tkinter as tk
from tkinter import ttk
from student_info_frame import StudentInfoFrame
from student_progress_frame import StudentProgressFrame
from student_achievements_frame import StudentAchievementsFrame
from student_sessions_frame import StudentSessionsFrame
from DataBase import DataBase
from Config import Configuration
class QuranLMSApp:
    def __init__(self, master):
        self.master = master
        master.title("Quran LMS")
        self.fixed_frame=ttk.Frame(self.master)
        self.fixed_frame.pack(side=tk.TOP)
        self.Buttons_frame=ttk.Frame(self.fixed_frame)
        self.Buttons_frame.pack(side=tk.TOP)

        # Create DataBase Tables 
        self.config=Configuration()
        self.DB=DataBase('quran_lms.db')

        self.kid_combobox = ttk.Combobox(self.Buttons_frame, values=self.DB.retrieve_kid_names())
        self.kid_combobox.set("اختر الطالب")
        self.kid_combobox.pack(side=tk.LEFT, padx=5, pady=5)

        self.config.combobox=self.kid_combobox
        self.config.DB=self.DB

        # Create frames
        self.create_student_info_frame()
        self.create_student_progress_frame()
        self.create_student_achievements_frame()
        self.create_student_sessions_frame()
        
        # Create buttons to switch between frames
        self.create_button("اضف طالب", self.show_student_info)
        self.create_button("تقدم الطلبة", self.show_student_progress)
        #self.create_button("Show Student Achievements", self.show_student_achievements)
        self.create_button("ملاحظات الحصص", self.show_student_sessions)

        # Set the default frame to show
        self.show_student_info()

    def create_button(self, text, command):
        button = ttk.Button(self.Buttons_frame, text=text, command=command)
        button.pack(side=tk.LEFT, padx=5, pady=5)

    def show_student_info(self):
        self.hide_all_frames()
        self.student_info_frame.show_frame()

    def show_student_progress(self):
        self.hide_all_frames()
        self.student_progress_frame.show_frame()
        if self.kid_combobox.get()== "" or self.kid_combobox.get()=="اختر الطالب":
            self.student_progress_frame.retrieve_data()
        else:
            self.student_progress_frame.retrieve_data(self.kid_combobox.get())

    def show_student_achievements(self):
        self.hide_all_frames()
        self.student_achievements_frame.show_frame()

    def show_student_sessions(self):
        self.hide_all_frames()
        self.student_sessions_frame.show_frame()
        self.student_sessions_frame.retrieve_data()

    def hide_all_frames(self):
        for frame in [
            self.student_info_frame,
            self.student_progress_frame,
            self.student_achievements_frame,
            self.student_sessions_frame
        ]:
            frame.hide_frame()

    def create_student_info_frame(self):
        self.student_info_frame = StudentInfoFrame(self.fixed_frame,self.config)

    def create_student_progress_frame(self):
        self.student_progress_frame = StudentProgressFrame(self.fixed_frame,self.config)

    def create_student_achievements_frame(self):
        self.student_achievements_frame = StudentAchievementsFrame(self.fixed_frame,self.config)
        
    def create_student_sessions_frame(self):
        self.student_sessions_frame = StudentSessionsFrame(self.fixed_frame,self.config)

        

