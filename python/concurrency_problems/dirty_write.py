import threading
import time

from python.database_init import microsoft_sql_connection


def transaction1():
    conn = microsoft_sql_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT Price from Products WHERE ProductID = 3")
    old_price = cursor.fetchone()[0]
    print(f"Old price: {old_price}")
    new_price = old_price - 10
    cursor.execute(f"UPDATE Products SET Price = {new_price} WHERE ProductID = 3")
    print(f"Transaction 1 updates price to {new_price} but has NOT committed.")

    time.sleep(7)  # Give time for Transaction 2 to overwrite it

    print("Transaction 1 rolled back changes.")
    cursor.execute("ROLLBACK")

    conn.close()


def transaction2():
    time.sleep(2)  # Ensure Transaction 1 runs first
    conn = microsoft_sql_connection()
    cursor = conn.cursor()

    cursor.execute("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
    cursor.execute("SELECT Price from Products WITH (NOLOCK) WHERE ProductID = 3")
    wrong_price = cursor.fetchone()[0]
    cursor.execute(f"UPDATE Products SET Price = {wrong_price + 4} WHERE ProductID = 3")
    print(f"Transaction 2 updates price to {wrong_price + 4} and committed.")
    cursor.commit()

    conn.close()


t1 = threading.Thread(target=transaction1)
t2 = threading.Thread(target=transaction2)

t1.start()
t2.start()
