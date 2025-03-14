import sqlite3
import os
from termcolor import colored

# Ensure that you are in the correct directory
print(f"Current Working Directory: {os.getcwd()}")

# Specify the correct path for the 'urls.db' in the 'instance' folder
project_directory = os.path.dirname(os.path.abspath(__file__))  # Get the directory of this script
db_path = os.path.join(project_directory, 'instance', 'urls.db')  # Create the absolute path

# Check if the database file exists at the expected location
if not os.path.exists(db_path):
    print(f"Error: The database file does not exist at {db_path}")
else:
    print(f"Database file found at {db_path}")

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

Konec = False
vstupy = ["removeall", "remove", "list", "exit"]

def confirm():
    check = input("To confirm write 'yes' to delete: ")
    return check.lower() == "yes"

while not Konec:
    print("\nAvailable Actions:")
    for i in vstupy:
        print(f"Akce: {i}")
    
    mezi = input("\nEnter Action: ")

    if mezi == vstupy[0]:
        if confirm():
            cursor.execute("DELETE FROM URL")
            conn.commit()
            print("All URLs deleted.")
        else:
            print("Action cancelled.")

    elif mezi == vstupy[1]:
        if confirm():
            short_url = input("Enter the short URL to remove: ")
            cursor.execute("DELETE FROM URL WHERE short_url=?", (short_url,))
            conn.commit()
            print("URL deleted.")
        else:
            print("Action cancelled.")

    elif mezi == vstupy[2]:
        cursor.execute("SELECT * FROM URL")
        rows = cursor.fetchall()

        if rows:
            print("\nListing all URLs:")
            for row in rows:
                print(colored(row, "green"))
        else:
            print(colored("No URLs found in the database.", "green"))

    elif mezi == vstupy[3]:
        print("Exiting...")
        Konec = True
    else:
        print("Invalid action. Please try again.")

conn.close()