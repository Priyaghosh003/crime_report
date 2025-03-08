import sqlite3
import os
import datetime

DB_NAME = "crime_system.db"

# Initialize the database and create necessary tables
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Users table: stores id, username, password, and role (citizen or police)
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT
                )''')
    # Crime reports table: stores report details
    c.execute('''CREATE TABLE IF NOT EXISTS crime_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    description TEXT,
                    location TEXT,
                    category TEXT,
                    image_path TEXT,
                    video_path TEXT,
                    status TEXT,
                    date TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )''')
    conn.commit()
    conn.close()

# Command-line based application
class CrimeApp:
    def __init__(self):
        self.current_user = None
        self.run()

    def run(self):
        while True:
            if not self.current_user:
                print("1. Login\n2. Register\n3. Exit")
                choice = input("Select an option: ")
                if choice == "1":
                    self.login()
                elif choice == "2":
                    self.register()
                elif choice == "3":
                    break
                else:
                    print("Invalid option, try again.")
            else:
                if self.current_user["role"] == "citizen":
                    self.citizen_dashboard()
                else:
                    self.police_dashboard()

    def login(self):
        username = input("Username: ").strip()

        password = input("Password: ").strip()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id, role FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone()
        conn.close()
        if result:
            self.current_user = {"id": result[0], "username": username, "role": result[1]}
            print("Login successful!")
        else:
            print("Invalid credentials!")

    def register(self):
        username = input("Choose a username: ").strip()
        password = input("Choose a password: ").strip()
        role = input("Role (citizen/police): ").strip().lower()
        if role not in ["citizen", "police"]:
            print("Invalid role!")
            return
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
            print("Registration successful! Please login.")
        except sqlite3.IntegrityError:
            print("Username already exists!")
        conn.close()

    def citizen_dashboard(self):
        print("\nCitizen Dashboard\n1. Report a Crime\n2. Logout")
        choice = input("Select an option: ")
        if choice == "1":
            self.report_crime()
        elif choice == "2":
            self.current_user = None
        else:
            print("Invalid option, try again.")

    def report_crime(self):
        description = input("Describe the crime: ").strip()
        location = input("Location: ").strip()
        category = input("Category: ").strip()
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO crime_reports (user_id, description, location, category, status, date) VALUES (?, ?, ?, ?, ?, ?)",
                  (self.current_user["id"], description, location, category, "Pending", date))
        conn.commit()
        conn.close()
        print("Crime reported successfully!")

    def police_dashboard(self):
        print("\nPolice Dashboard\n1. View Reports\n2. Logout")
        choice = input("Select an option: ")
        if choice == "1":
            self.view_reports()
        elif choice == "2":
            self.current_user = None
        else:
            print("Invalid option, try again.")

    def view_reports(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM crime_reports")
        reports = c.fetchall()
        conn.close()
        if reports:
            for report in reports:
                print(f"ID: {report[0]}, User ID: {report[1]}, Description: {report[2]}, Location: {report[3]}, Category: {report[4]}, Status: {report[7]}, Date: {report[8]}")
        else:
            print("No reports available.")
    
    # write a function to update status of crime report
    # give option to police to update crime report
    # explore how to update tsble in sql data base
    import sqlite3

def update_crime_status(report_id, new_status):
    """
    Updates the status of a crime report in the database.
    :param report_id: ID of the crime report to be updated
    :param new_status: New status to be assigned to the crime report
    """
    try:
        # Connect to the database
        conn = sqlite3.connect('crime_reports.db')  # Change to your database name
        cursor = conn.cursor()
        
        # Update query
        cursor.execute("""
            UPDATE crime_reports
            SET status = ?
            WHERE id = ?
        """, (new_status, report_id))
        
        # Commit changes and close connection
        conn.commit()
        print(f"Crime report ID {report_id} updated to status: {new_status}")
    except sqlite3.Error as e:
        print("Error updating crime report:", e)
    finally:
        conn.close()

# Example usage
if __name__ == "__main__":
    report_id = int(input("Enter Crime Report ID: "))
    new_status = input("Enter New Status: ")
    update_crime_status(report_id, new_status)
1
    

if __name__ == "__main__":
    init_db()
    CrimeApp()
