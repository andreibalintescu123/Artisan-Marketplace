import threading
import time

from python.database_init import microsoft_sql_connection


def transaction1():
    conn = microsoft_sql_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT StockQuantity from Products WHERE ProductID = 1")
    current_stock = cursor.fetchone()[0]
    print(f"Transaction 1 reads current stock {current_stock}.")

    time.sleep(5)  # Allow Transaction 2 to try reading uncommitted data
    new_stock = current_stock + 20
    cursor.execute(f"UPDATE Products SET StockQuantity = {new_stock} WHERE ProductID = 1")
    conn.commit()
    print(f"Transaction 1 updates new stock to {new_stock}.")

    conn.close()

def transaction2():
    time.sleep(2)  # Ensure Transaction 1 runs first
    conn = microsoft_sql_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE Products SET StockQuantity = 0 WHERE ProductID = 1")

    print(f"Transaction 2 updates stock to 0 and commits.")

    conn.commit()
    conn.close()

t1 = threading.Thread(target=transaction1)
t2 = threading.Thread(target=transaction2)

t1.start()
t2.start()
