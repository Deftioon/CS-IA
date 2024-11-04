import streamlit as st
import sqlite3
import pandas as pd

st.title("Admin Dashboard")

# Initialize session state variables
if 'show_form' not in st.session_state:
    st.session_state.show_form = False
if 'show_user_form' not in st.session_state:
    st.session_state.show_user_form = False

# Buttons to edit the database
col1, col2 = st.columns(2)

with col1:
    st.write("### Welcome to the Admin Panel")

with col2:
    if st.button("Add User"):
        st.session_state.show_user_form = True

    if st.button("Add Entry"):
        st.session_state.show_form = True

# Add Entry Form
if st.session_state.show_form:
    with st.form("add_entry_form"):
        student_id = st.number_input("Student ID", min_value=1, step=1, format="%d")
        demerit_id = st.number_input("Demerit ID", min_value=1, step=1, format="%d")
        num = st.number_input("Number of Demerits", min_value=1, step=1, format="%d")
        comment = st.text_input("Comment")
        added_by = st.number_input("Added By (Teacher ID)", min_value=1, step=1, format="%d")
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            try:
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO History (StudentID, DemeritID, Num, Comment, AddedBy)
                    VALUES (?, ?, ?, ?, ?)
                """, (student_id, demerit_id, num, comment, added_by))
                conn.commit()
                conn.close()
                st.success("Entry added successfully.")
                st.session_state.show_form = False
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Add User Form
if st.session_state.show_user_form:
    with st.form("add_user_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        permission = st.selectbox("Permission", ["admin", "teacher", "student", "parent"])
        
        # Optional IDs
        student_id = st.number_input("Student ID (optional)", min_value=0, step=1, format="%d", value=0)
        teacher_id = st.number_input("Teacher ID (optional)", min_value=0, step=1, format="%d", value=0)
        admin_id = st.number_input("Admin ID (optional)", min_value=0, step=1, format="%d", value=0)
        parent_id = st.number_input("Parent ID (optional)", min_value=0, step=1, format="%d", value=0)
        
        # Conditional fields based on permission
        if permission == "student":
            student_name = st.text_input("Student Name")
            class_id = st.number_input("Class ID", min_value=1, step=1, format="%d")
        elif permission == "teacher":
            teacher_name = st.text_input("Teacher Name")
        elif permission == "admin":
            admin_name = st.text_input("Admin Name")
        elif permission == "parent":
            parent_name = st.text_input("Parent Name")
            contact_info = st.text_input("Contact Info")
        
        submitted_user = st.form_submit_button("Submit")
        
        if submitted_user:
            try:
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                
                # Insert into User table
                cursor.execute("""
                    INSERT INTO User (Username, Password, Permission, StudentID, TeacherID, AdminID, ParentID)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    username, 
                    password, 
                    permission, 
                    student_id if student_id != 0 else None, 
                    teacher_id if teacher_id != 0 else None, 
                    admin_id if admin_id != 0 else None, 
                    parent_id if parent_id != 0 else None
                ))
                
                user_id = cursor.lastrowid  # Get the ID of the newly created user

                # Insert into respective tables based on permission
                if permission == "student":
                    cursor.execute("""
                        INSERT INTO Student (Name, ClassID)
                        VALUES (?, ?)
                    """, (student_name, class_id))
                elif permission == "teacher":
                    cursor.execute("""
                        INSERT INTO Teacher (Name)
                        VALUES (?)
                    """, (teacher_name,))
                elif permission == "admin":
                    cursor.execute("""
                        INSERT INTO Admin (Name)
                        VALUES (?)
                    """, (admin_name,))
                elif permission == "parent":
                    cursor.execute("""
                        INSERT INTO Parent (Name, ContactInfo)
                        VALUES (?, ?)
                    """, (parent_name, contact_info))
                
                conn.commit()
                conn.close()
                st.success("User added successfully.")
                st.session_state.show_user_form = False
            except sqlite3.IntegrityError as ie:
                st.error(f"Integrity Error: {ie}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Display the history table with sorting and filtering
conn = sqlite3.connect('database.db')
df_history = pd.read_sql_query("""
    SELECT History.HistoryID, Student.Name as StudentName, Demerit.Reason, History.Num, 
           History.Comment, Teacher.Name as AddedBy, History.DateAdded
    FROM History
    LEFT JOIN Student ON History.StudentID = Student.StudentID
    LEFT JOIN Demerit ON History.DemeritID = Demerit.DemeritID
    LEFT JOIN Teacher ON History.AddedBy = Teacher.TeacherID
""", conn)
conn.close()

st.write("### History Table")
st.dataframe(df_history.sort_values(by="DateAdded", ascending=False))

# Display the user table with permissions
conn = sqlite3.connect('database.db')
df_users = pd.read_sql_query("""
    SELECT 
        User.UserID, 
        User.Username, 
        User.Permission, 
        Student.Name as StudentName, 
        Teacher.Name as TeacherName,
        Admin.Name as AdminName, 
        Parent.Name as ParentName
    FROM User
    LEFT JOIN Student ON User.StudentID = Student.StudentID
    LEFT JOIN Teacher ON User.TeacherID = Teacher.TeacherID
    LEFT JOIN Admin ON User.AdminID = Admin.AdminID
    LEFT JOIN Parent ON User.ParentID = Parent.ParentID
""", conn)
conn.close()

# Replace None with empty strings for better display
df_users.fillna('', inplace=True)

# Create a new column for Associated Name based on Permission
def get_associated_name(row):
    if row['Permission'] == 'student':
        return row['StudentName']
    elif row['Permission'] == 'teacher':
        return row['TeacherName']
    elif row['Permission'] == 'admin':
        return row['AdminName']
    elif row['Permission'] == 'parent':
        return row['ParentName']
    else:
        return ''

df_users['AssociatedName'] = df_users.apply(get_associated_name, axis=1)

# Select relevant columns
df_users_display = df_users[['UserID', 'Username', 'Permission', 'AssociatedName']]

st.write("### User Table with Permissions")
st.dataframe(df_users_display.sort_values(by="Username"))