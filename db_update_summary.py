# Finally, to update a report or table with the extracted information, you can use a database like SQLite or MySQL.
# Here's an example of how to insert data into a SQLite database using Python:


import sqlite3

def insert_data_into_database(summary):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO records (summary) VALUES (?)", (summary,))
    conn.commit()
    conn.close()
