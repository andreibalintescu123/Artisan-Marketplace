from python.database_init import sqlite_connection


def add_product(artisan_id, name, description, price, stock_quantity, connection):
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO Products (ArtisanID, Name, Description, Price, StockQuantity) VALUES (?, ?, ?, ?, "
                       "?)",
                       (artisan_id, name, description, price, stock_quantity))
        connection.commit()
    except Exception as e:
        print(f"Error adding product: {e}")
        connection.rollback()
    finally:
        connection.close()


def get_products(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
    except Exception as e:
        print(f"Error getting products: {e}")
        products = []
    finally:
        connection.close()
    return products


def update_product(product_id, name, description, price, stock_quantity, connection):
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE Products SET Name=?, Description=?, Price=?, StockQuantity=? WHERE ProductID=?",
                       (name, description, price, stock_quantity, product_id))
        connection.commit()
    except Exception as e:
        print(f"Error updating product: {e}")
        connection.rollback()
    finally:
        connection.close()


def delete_product(product_id, connection):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Products WHERE ProductID=?", (product_id,))
        connection.commit()
    except Exception as e:
        print(f"Error deleting product: {e}")
        connection.rollback()
    finally:
        connection.close()
