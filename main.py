import sqlite3

def explore_database():
    conn = sqlite3.connect('player_data.db')
    cursor = conn.cursor()

    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Tables in the database:")
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        
        # Get schema
        cursor.execute(f"PRAGMA table_info({table_name});")
        schema = cursor.fetchall()
        print(f"Schema for {table_name}:")
        for column in schema:
            print(column)

        # Check if table has data
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"Table {table_name} contains {count} rows.")
        else:
            print(f"Table {table_name} is empty.")
    
    conn.close()

if __name__ == "__main__":
    explore_database()
