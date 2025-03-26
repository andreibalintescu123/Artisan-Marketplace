from python.database_init import create_connection


def add_product(artisan_id, name, description, price, stock_quantity):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Products (ArtisanID, Name, Description, Price, StockQuantity) VALUES (?, ?, ?, ?, "
                       "?)",
                       (artisan_id, name, description, price, stock_quantity))
        conn.commit()
    except Exception as e:
        print(f"Error adding product: {e}")
        conn.rollback()
    finally:
        conn.close()


def get_products():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
    except Exception as e:
        print(f"Error getting products: {e}")
        products = []
    finally:
        conn.close()
    return products


def update_product(product_id, name, description, price, stock_quantity):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Products SET Name=?, Description=?, Price=?, StockQuantity=? WHERE ProductID=?",
                       (name, description, price, stock_quantity, product_id))
        conn.commit()
    except Exception as e:
        print(f"Error updating product: {e}")
        conn.rollback()
    finally:
        conn.close()


def delete_product(product_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Products WHERE ProductID=?", (product_id,))
        conn.commit()
    except Exception as e:
        print(f"Error deleting product: {e}")
        conn.rollback()
    finally:
        conn.close()
