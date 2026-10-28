import sqlite3
from datetime import datetime

# Initialize the database and create tables if they don't exist
def init_db():
    # Connect to SQLite database (creates 'tracker.db' in the project directory)
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    
    # Create a table to store product name, price, and timestamp
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            price REAL,
            date_recorded TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Insert a new price record into the database
def add_price_record(product_name, price):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    
    # Get current timestamp
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Insert record into the price_history table
    cursor.execute('''
        INSERT INTO price_history (product_name, price, date_recorded)
        VALUES (?, ?, ?)
    ''', (product_name, price, current_date))
    
    conn.commit()
    conn.close()
    print("Data successfully saved to the database!")

# Test database setup locally
if __name__ == "__main__":
    init_db()
    add_price_record("A Light in the Attic", 51.77)