import threading
import time

from python.database_init import microsoft_sql_connection


def transaction1():
    conn = microsoft_sql_connection()
    cursor = conn.cursor()

    cursor.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")
    cursor.execute("SELECT COUNT(*) FROM Products WHERE ArtisanID = 1")
    count_before = cursor.fetchone()[0]
    print(f"Transaction 1 sees {count_before} products initially.")

    time.sleep(10)  # Wait for Transaction 2 to insert a new row

    cursor.execute("SELECT COUNT(*) FROM Products WHERE ArtisanID = 1")
    count_after = cursor.fetchone()[0]
    print(f"Transaction 1 sees {count_after} products after Transaction 2 commits.")

    conn.close()

def transaction2():
    time.sleep(2)
    conn = microsoft_sql_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Products (ArtisanID, Name, Description, Price, StockQuantity) VALUES (1, 'Vaza prototip', 'Test', 28, 10)")
    cursor.commit()
    print("Transaction 2 inserts a new product and commits.")

    conn.close()

t1 = threading.Thread(target=transaction1)
t2 = threading.Thread(target=transaction2)

t1.start()
t2.start()