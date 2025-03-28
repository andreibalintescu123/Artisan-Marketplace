import sqlite3
from datetime import datetime


def add_order(customer_name, connection):
    """
    Add a new order with the current date and initial total amount of 0.
    
    Args:
        customer_name (str): Name of the customer placing the order
        connection (sqlite3.Connection): Database connection
    
    Returns:
        int or None: Order ID if successful, None otherwise
    """
    cursor = connection.cursor()
    current_date = datetime.now().strftime('%Y-%m-%d')

    try:
        cursor.execute("""
            INSERT INTO Orders (CustomerName, OrderDate, TotalAmount) 
            VALUES (?, ?, 0)
        """, (customer_name, current_date))

        order_id = cursor.lastrowid
        connection.commit()
        return order_id
    except Exception as e:
        print(f"Error adding order: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()


def add_order_item(order_id, product_id, quantity, connection):
    """
    Add an item to an order and update product stock.
    
    Args:
        order_id (int): ID of the order
        product_id (int): ID of the product being ordered
        quantity (int): Quantity of the product
        connection (sqlite3.Connection): Database connection
    
    Returns:
        bool: True if successful, False otherwise
    """
    cursor = connection.cursor()

    try:
        # Get product price
        cursor.execute("SELECT Price, StockQuantity FROM Products WHERE ProductID = ?", (product_id,))
        product = cursor.fetchone()

        if not product:
            print(f"Product {product_id} not found")
            return False

        product_price, current_stock = product

        # Check if enough stock
        if current_stock < quantity:
            print(f"Insufficient stock for product {product_id}")
            return False

        # Insert order item
        cursor.execute("""
            INSERT INTO OrderItems (OrderID, ProductID, Quantity, Price) 
            VALUES (?, ?, ?, ?)
        """, (order_id, product_id, quantity, product_price))

        # Update product stock
        new_stock = current_stock - quantity
        cursor.execute("""
            UPDATE Products 
            SET StockQuantity = ? 
            WHERE ProductID = ?
        """, (new_stock, product_id))

        connection.commit()
        return True
    except Exception as e:
        print(f"Error adding order item: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()


def calculate_order_total(order_id, connection):
    """
    Calculate and update the total amount for an order.
    
    Args:
        order_id (int): ID of the order
        connection (sqlite3.Connection): Database connection
    
    Returns:
        float: Total order amount
    """
    cursor = connection.cursor()

    try:
        # Calculate total by multiplying quantity and price for each order item
        cursor.execute("""
            SELECT SUM(Quantity * Price) as TotalAmount 
            FROM OrderItems 
            WHERE OrderID = ?
        """, (order_id,))

        total_amount = cursor.fetchone()[0] or 0

        # Update order total
        cursor.execute("""
            UPDATE Orders 
            SET TotalAmount = ? 
            WHERE OrderID = ?
        """, (total_amount, order_id))

        connection.commit()
        return total_amount
    except Exception as e:
        print(f"Error calculating order total: {e}")
        connection.rollback()
        return 0
    finally:
        cursor.close()


def get_order_details(order_id, connection):
    """
    Retrieve complete details of an order.
    
    Args:
        order_id (int): ID of the order
        connection (sqlite3.Connection): Database connection
    
    Returns:
        dict: Order details including items
    """
    cursor = connection.cursor()

    try:
        # Get order header
        cursor.execute("""
            SELECT OrderID, CustomerName, OrderDate, TotalAmount 
            FROM Orders 
            WHERE OrderID = ?
        """, (order_id,))
        order = cursor.fetchone()

        if not order:
            return None

        # Get order items with product details
        cursor.execute("""
            SELECT 
                oi.ProductID, 
                p.Name as ProductName, 
                oi.Quantity, 
                oi.Price,
                (oi.Quantity * oi.Price) as SubTotal
            FROM OrderItems oi
            JOIN Products p ON oi.ProductID = p.ProductID
            WHERE oi.OrderID = ?
        """, (order_id,))
        order_items = cursor.fetchall()

        return {
            'order_id': order[0],
            'customer_name': order[1],
            'order_date': order[2],
            'total_amount': order[3],
            'items': order_items
        }
    except Exception as e:
        print(f"Error retrieving order details: {e}")
        return None
    finally:
        cursor.close()


def place_order(customer_name, order_items, connection):
    """
    Complete order placement process.
    
    Args:
        customer_name (str): Name of the customer
        order_items (list): List of tuples (product_id, quantity)
        connection (sqlite3.Connection): Database connection
    
    Returns:
        int or None: Order ID if successful, None otherwise
    """
    try:
        # Create order
        order_id = add_order(customer_name, connection)

        if not order_id:
            return None

        # Add order items
        for product_id, quantity in order_items:
            if not add_order_item(order_id, product_id, quantity, connection):
                # Rollback if any item fails
                delete_order(order_id, connection)
                return None

        # Calculate and update total
        total_amount = calculate_order_total(order_id, connection)

        return order_id
    except Exception as e:
        print(f"Error placing order: {e}")
        return None


def delete_order(order_id, connection):
    """
    Delete an order and restore product stocks.
    
    Args:
        order_id (int): ID of the order to delete
        connection (sqlite3.Connection): Database connection
    
    Returns:
        bool: True if successful, False otherwise
    """
    cursor = connection.cursor()

    try:
        # Retrieve order items to restore stock
        cursor.execute("""
            SELECT ProductID, Quantity 
            FROM OrderItems 
            WHERE OrderID = ?
        """, (order_id,))
        order_items = cursor.fetchall()

        # Restore product stocks
        for product_id, quantity in order_items:
            cursor.execute("""
                UPDATE Products 
                SET StockQuantity = StockQuantity + ? 
                WHERE ProductID = ?
            """, (quantity, product_id))

        # Delete order items
        cursor.execute("DELETE FROM OrderItems WHERE OrderID = ?", (order_id,))

        # Delete order
        cursor.execute("DELETE FROM Orders WHERE OrderID = ?", (order_id,))

        connection.commit()
        return True
    except Exception as e:
        print(f"Error deleting order: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()


# Function to retrieve all orders
def get_orders(connection):
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT OrderID, CustomerName, OrderDate, TotalAmount FROM Orders ORDER BY OrderDate DESC")
        orders = cursor.fetchall()
    except Exception as e:
        print(f"Error getting orders: {e}")
        orders = []  # Return an empty list in case of error
    finally:
        connection.close()
    return orders
