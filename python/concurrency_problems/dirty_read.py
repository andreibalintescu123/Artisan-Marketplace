import threading
import time

from python.database_init import microsoft_sql_connection


def transaction1():
    conn = microsoft_sql_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE Products SET StockQuantity = 100 WHERE ProductID = 2")
    print("Transaction 1 updated stock but has NOT committed.")

    time.sleep(5)  # Allow Transaction 2 to try reading uncommitted data
    cursor.execute("ROLLBACK")
    print("Transaction 1 rolled back the update.")

    conn.close()

def transaction2():
    time.sleep(2)  # Ensure Transaction 1 runs first
    conn = microsoft_sql_connection()
    cursor = conn.cursor()

    cursor.execute("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
    cursor.execute("SELECT StockQuantity FROM Products WHERE ProductID = 2")
    stock = cursor.fetchone()[0]

    print(f"Transaction 2 reads stock: {stock}")

    conn.commit()
    conn.close()

t1 = threading.Thread(target=transaction1)
t2 = threading.Thread(target=transaction2)

t1.start()
t2.start()
