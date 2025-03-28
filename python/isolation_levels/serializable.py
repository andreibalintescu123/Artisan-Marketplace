import time

from python.database_init import microsoft_sql_connection


def repeatable_read():
    time.sleep(3)
    conn = microsoft_sql_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Products (ArtisanID, Name, Description, Price, StockQuantity) VALUES (1, 'Vaza de argila', 'Test 3', 84, 10)")
    cursor.commit()
    print("Inserted a new product entry for Artisan 1. ")

    conn.close()

if __name__ == '__main__':
    repeatable_read()