import threading
import time

from python.database_init import microsoft_sql_connection


def transaction1():
    conn = microsoft_sql_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT StockQuantity from Products WHERE ProductID = 4 ")
    initial_stock = cursor.fetchone()[0]
    print(f"Transaction reads {initial_stock} first.")

    time.sleep(5)  # Allow Transaction 2 to try updating the data

    cursor.execute("SELECT StockQuantity from Products WHERE ProductID = 4 ")
    final_stock = cursor.fetchone()[0]
    print(f"Transaction reads {final_stock} the second time.")

    conn.commit()
    conn.close()

def transaction2():
    time.sleep(2)  # Ensure Transaction 1 runs first
    conn = microsoft_sql_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE Products SET StockQuantity = StockQuantity + 10 WHERE ProductID = 4 ")
    print(f"Transaction 2 updates the stock and commits.")
    conn.commit()
    conn.close()

t1 = threading.Thread(target=transaction1)
t2 = threading.Thread(target=transaction2)

t1.start()
t2.start()
