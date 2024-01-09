import mysql.connector
import pandas as pd
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Database connection parameters
db_config = {
    'user': 'yono',
    'password': 'Demo@4300',
    'host': 'localhost',
    'database': 'apprentissage'
}

# Connect to the MySQL database
try:
    mydb = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        passwd=db_config['password'],
        database=db_config['database'],
        auth_plugin="mysql_native_password"
    )
except mysql.connector.Error as e:
    print(f"Error connecting to MySQL Database: {e}")
    exit(1)

def query_database(query):
    """Execute a query and return the result as a DataFrame."""
    cursor = mydb.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    print(type(result))
    cursor.close()
    return pd.DataFrame(result, columns=['ID','Age', 'Sexe', 'libelle_nationalite', 'Type_contrat', 'Code_P', 'Ville'])

def display_data(data):
    """Display data in a new window."""
    new_window = tk.Toplevel(root)
    new_window.title("Query Results")
    table = ttk.Treeview(new_window)
    table["columns"] = data.columns.tolist()
    table["show"] = "headings"

    for column in table["columns"]:
        table.heading(column, text=column)
        table.column(column, width=100)

    for index, row in data.iterrows():
        table.insert("", "end", values=list(row))

    table.pack(expand=True, fill="both")

def get_student_info():
    """Retrieve information for a specific student by ID."""
    student_id = int(student_id_entry.get())
    print(student_id)
    query = f"SELECT * FROM Etudiant WHERE ID_E = {student_id}"
    data = query_database(query)
    display_data(data)

def get_students_by_establishment():
    """Retrieve students associated with a specific establishment."""
    establishment_id = establishment_id_entry.get()
    query = f"""
    SELECT Etudiant.*
    FROM Etudiant
    JOIN Cerfa ON Etudiant.ID_E = Cerfa.ID_E
    WHERE Cerfa.id_siteformation = {establishment_id}
    """
    data = query_database(query)
    display_data(data)

def get_apprentices_by_company():
    """Retrieve apprentices associated with a specific company."""
    company_code = company_code_entry.get()
    query = f"""
    SELECT Etudiant.*
    FROM Etudiant
    JOIN Cerfa ON Etudiant.ID_E = Cerfa.ID_E
    WHERE Cerfa.code_insee_entreprise = {company_code}
    """
    data = query_database(query)
    display_data(data)

def get_students_by_diploma():
    """Retrieve students associated with a specific diploma."""
    diploma_id = diploma_id_entry.get()
    query = f"""
    SELECT Etudiant.*
    FROM Etudiant
    JOIN Cerfa ON Etudiant.ID_E = Cerfa.ID_E
    WHERE Cerfa.ID_D = {diploma_id}
    """
    data = query_database(query)
    display_data(data)

def filter():
    """Retrieve information for a specific student by ID."""
    Age = Age_entry.get()
    Sex = Sex_entry.get()
    nat = Nationality_entry.get()
    ville = ville_entry.get()

    query = f"SELECT * FROM Etudiant WHERE (1=1"
    
    if Age != '':
        query = query + f" AND AGE = {Age}"

    if Sex != '':
        query = query + f" AND Sexe = '{Sex}'"

    if nat != '':
        query = query + f" AND libelle_nationalite = '{nat}'"
    
    if ville != '':
        query = query + f" AND Ville = '{ville}'"
        
    query = query + ")"

    print('query=',query)
    data = query_database(query)
    display_data(data)

# GUI Layout
root = tk.Tk()
root.title("Apprentissage Database")

# Set the window size
#root.geometry("800x600")  # Width x Height

# Set the window icon
icon_path = 'MIOM_large.png'  # Path to the icon image
icon_image = Image.open(icon_path)
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(False, icon_photo)

# Load an image to be displayed at the top
header_image_path = 'back.png'  # Path to your header image
header_image = Image.open(header_image_path)
#header_image = header_image.resize((800, 200), Image.ANTIALIAS)  # Resize image to fit the window width
header_photo = ImageTk.PhotoImage(header_image)


# Define colors
frame_color = "#ffffff"
button_color = "#ff0000"
text_color = "#000000"

# Create a frame
frame = tk.Frame(root, bg=frame_color)
frame.pack(padx=10, pady=10)


# Display the image at the top of the window
header_label = tk.Label(frame, image=header_photo, bg=frame_color)
header_label.grid(row=0, column=0, columnspan=2)  # Spanning across all columns



# Student Info
tk.Label(frame, text="Enter Student ID:", bg=frame_color, fg=text_color).grid(row=1, column=0)
student_id_entry = tk.Entry(frame)
student_id_entry.grid(row=2, column=0)
tk.Button(frame, text="Get Student Info", command=get_student_info, bg=button_color).grid(row=3, column=0)

# Students by Establishment
tk.Label(frame, text="Enter Establishment ID:", bg=frame_color, fg=text_color).grid(row=4, column=0)
establishment_id_entry = tk.Entry(frame)
establishment_id_entry.grid(row=5, column=0)
tk.Button(frame, text="Get Students by Establishment", command=get_students_by_establishment, bg=button_color).grid(row=6, column=0)

# Apprentices by Company
tk.Label(frame, text="Enter Company Code:", bg=frame_color, fg=text_color).grid(row=7, column=0)
company_code_entry = tk.Entry(frame)
company_code_entry.grid(row=8, column=0)
tk.Button(frame, text="Get Apprentices by Company", command=get_apprentices_by_company, bg=button_color).grid(row=9, column=0)

# Students by Diploma
tk.Label(frame, text="Enter Diploma ID:", bg=frame_color, fg=text_color).grid(row=10, column=0)
diploma_id_entry = tk.Entry(frame)
diploma_id_entry.grid(row=11, column=0)
tk.Button(frame, text="Get Students by Diploma", command=get_students_by_diploma, bg=button_color).grid(row=12, column=0)

# Filter Label
filter_label = tk.Label(frame, text="Filter Database:", bg=frame_color)
filter_label.grid(row=1, column=1)  # Columnspan to cover three columns

# Filter Elements
tk.Label(frame, text="Ville:", bg=frame_color, fg=text_color).grid(row=2, column=1)
ville_entry = tk.Entry(frame)
ville_entry.grid(row=3, column=1)

tk.Label(frame, text="Age:", bg=frame_color, fg=text_color).grid(row=4, column=1)
Age_entry = tk.Entry(frame)
Age_entry.grid(row=5, column=1)

tk.Label(frame, text="Sex:", bg=frame_color, fg=text_color).grid(row=6, column=1)
Sex_entry = tk.Entry(frame)
Sex_entry.grid(row=7, column=1)

tk.Label(frame, text="Nationality:", bg=frame_color, fg=text_color).grid(row=8, column=1)
Nationality_entry = tk.Entry(frame)
Nationality_entry.grid(row=9, column=1)

tk.Button(frame, text="Apply Filters", command=filter, bg=button_color).grid(row=10, column=1, columnspan=4)  # Columnspan to cover all columns

root.mainloop()