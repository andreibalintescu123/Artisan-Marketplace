from python.database_init import create_connection


# Function to add a new order
def add_order(customer_name):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO Orders (CustomerName, TotalAmount) VALUES (?, ?)", (customer_name, 0))
        order_id = cursor.lastrowid  # Get the ID of the newly inserted order
        conn.commit()
    except Exception as e:
        print(f"Error adding order: {e}")
        conn.rollback()
        return None  # Indicate failure
    finally:
        conn.close()
    return order_id  # Return the order ID for further processing


# Function to add items to an order
def add_order_item(order_id, product_id, quantity, price):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO OrderItems (OrderID, ProductID, Quantity, Price) VALUES (?, ?, ?, ?)",
                       (order_id, product_id, quantity, price))
        conn.commit()
    except Exception as e:
        print(f"Error adding order item: {e}")
        conn.rollback()
        return False  # Indicate failure
    finally:
        conn.close()
    return True  # Indicate success


# Function to update product stock after placing an order
def update_product_stock(product_id, new_stock):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE Products SET StockQuantity = ? WHERE ProductID = ?", (new_stock, product_id))
        conn.commit()
    except Exception as e:
        print(f"Error updating product stock: {e}")
        conn.rollback()
        return False  # Indicate failure
    finally:
        conn.close()
    return True  # Indicate success


# Function to update the total amount of an order
def update_order_total(order_id, total_amount):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE Orders SET TotalAmount = ? WHERE OrderID = ?", (total_amount, order_id))
        conn.commit()
    except Exception as e:
        print(f"Error updating order total: {e}")
        conn.rollback()
        return False  # Indicate failure
    finally:
        conn.close()
    return True  # Indicate success


# Function to retrieve all orders
def get_orders():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT OrderID, CustomerName, OrderDate, TotalAmount FROM Orders ORDER BY OrderDate DESC")
        orders = cursor.fetchall()
    except Exception as e:
        print(f"Error getting orders: {e}")
        orders = []  # Return an empty list in case of error
    finally:
        conn.close()
    return orders


# Function to retrieve all items in an order
def get_order_items(order_id):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT OrderItemID, OrderID, ProductID, Quantity, Price FROM OrderItems WHERE OrderID = ?",
                       (order_id,))
        order_items = cursor.fetchall()
    except Exception as e:
        print(f"Error getting order items: {e}")
        order_items = []  # Return an empty list in case of error
    finally:
        conn.close()
    return order_items


# Function to delete an order (and its associated items)
def delete_order(order_id):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Delete all associated order items first
        cursor.execute("DELETE FROM OrderItems WHERE OrderID = ?", (order_id,))

        # Delete the order itself
        cursor.execute("DELETE FROM Orders WHERE OrderID = ?", (order_id,))

        conn.commit()
    except Exception as e:
        print(f"Error deleting order: {e}")
        conn.rollback()
        return False  # Indicate failure
    finally:
        conn.close()
    return True  # Indicate success