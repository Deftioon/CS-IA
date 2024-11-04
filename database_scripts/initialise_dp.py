import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Define the SQL script
sql_script = """
CREATE TABLE Class (
    ClassID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(50) NOT NULL,
    Grade INTEGER NOT NULL,
    Division VARCHAR(10),
    AcademicYear VARCHAR(9)
);

CREATE TABLE Student (
    StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(100) NOT NULL,
    ClassID INTEGER,
    FOREIGN KEY (ClassID) REFERENCES Class(ClassID)
);

CREATE TABLE Teacher (
    TeacherID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(100) NOT NULL
);

CREATE TABLE Admin (
    AdminID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(100) NOT NULL
);

CREATE TABLE Parent (
    ParentID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(100) NOT NULL,
    ContactInfo VARCHAR(255)
);

CREATE TABLE User (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Permission VARCHAR(20) NOT NULL,
    StudentID INTEGER,
    TeacherID INTEGER,
    AdminID INTEGER,
    ParentID INTEGER,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (TeacherID) REFERENCES Teacher(TeacherID),
    FOREIGN KEY (AdminID) REFERENCES Admin(AdminID),
    FOREIGN KEY (ParentID) REFERENCES Parent(ParentID)
);

CREATE TABLE Demerit (
    DemeritID INTEGER PRIMARY KEY AUTOINCREMENT,
    Reason VARCHAR(255) NOT NULL,
    Notes TEXT,
    Type VARCHAR(50),
    CoreValueViolation VARCHAR(100)
);

CREATE TABLE History (
    HistoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    StudentID INTEGER,
    DemeritID INTEGER,
    Num INTEGER NOT NULL,
    Comment TEXT,
    AddedBy INTEGER,
    DateAdded DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (DemeritID) REFERENCES Demerit(DemeritID),
    FOREIGN KEY (AddedBy) REFERENCES Teacher(TeacherID)
);
"""

# Execute the SQL script
cursor.executescript(sql_script)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database with User, Admin, and Parent tables created successfully!")