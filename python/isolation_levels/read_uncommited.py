import time

from python.database_init import microsoft_sql_connection


def read_uncommitted():
    conn = microsoft_sql_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT Price from Products WHERE ProductID = 4")
    price = cursor.fetchone()[0]
    print(f"Original price: {price}")

    cursor.execute("UPDATE Products SET Price = ? WHERE ProductID = ?", (price + 90, 4))

    print(f"Updated price: {price + 90}")
    time.sleep(5)
    cursor.execute("ROLLBACK")
    print("Rolled back changes")
    cursor.close()

if __name__ == "__main__":
    read_uncommitted()