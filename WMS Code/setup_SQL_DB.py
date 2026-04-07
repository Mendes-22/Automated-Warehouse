import sqlite3

def populate_warehouse():
    # Connect to the manually created file
    connection = sqlite3.connect('warehouse.db')
    cursor = connection.cursor()
    
    # Clean the table to start fresh (prevents duplicate entries)
    cursor.execute("DELETE FROM slots")
    
    # Will create 6 columns (X) and 9 levels (Z) = 54 slots
    # Level 1 to 3: Tall boxes (Type 2)
    # Level 4 to 9: Short boxes (Type 1)
    
    for level in range(1, 10):    # Z_pos (Height)
        for column in range(1, 7): # X_pos (Horizontal)
            
            # Logic: If level <= 3, it's for Tall (2), else it's for Short (1)
            allowed_type = 2 if level <= 3 else 1
            
            # Don't need to include 'id' here because it is AUTOINCREMENT
            cursor.execute("""
                INSERT INTO slots (x_pos, z_pos, occupied, box_type) 
                VALUES (?, ?, ?, ?)
            """, (column, level, 0, allowed_type))
            
    connection.commit()
    connection.close()
    print("✅ Database 'warehouse.db' created and populated!")

if __name__ == "__main__":
    populate_warehouse()
