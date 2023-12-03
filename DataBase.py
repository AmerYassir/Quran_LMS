import sqlite3
class DataBase():
    def __init__(self,DB_name):
        self.conn = sqlite3.connect(DB_name)
        self.c = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS students (
            
            name TEXT PRIMARY KEY,
            age INTEGER NOT NULL,
            level TEXT NOT NULL
        )""")

        self.c.execute("""CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY,
            student_name Text NOT NULL,
            surah TEXT NOT NULL,
            ayat_start INTEGER NOT NULL,
            ayat_end INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (student_name) REFERENCES students(name)
        )""")

        self.c.execute("""CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY,
            student_name Text NOT NULL,
            achievement TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (student_name) REFERENCES students(name)
        )""")

        self.c.execute("""CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            notes TEXT
        )""")

        self.conn.commit()

    def retrieve_kid_names(self):
        self.c.execute("SELECT name FROM students")
        students_data = self.c.fetchall()
        return students_data