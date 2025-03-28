import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from python.CRUD.artisan import *
from python.CRUD.product import *
from python.CRUD.order import *
from python.database_init import sqlite_connection, postgres_connection, microsoft_sql_connection

# Create the main window
root = tk.Tk()
root.title("Artisan Marketplace")
root.geometry("1250x500")

# Create a Notebook (Tabs)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Create frames for different sections
frame_artisans = ttk.Frame(notebook)
frame_products = ttk.Frame(notebook)
frame_orders = ttk.Frame(notebook)

notebook.add(frame_orders, text="Orders")
notebook.add(frame_artisans, text="Artisans")
notebook.add(frame_products, text="Products")


# ARTISAN FORM
def submit_artisan():
    name = artisan_name_var.get()
    location = artisan_location_var.get()
    speciality = artisan_speciality_var.get()

    if name and location and speciality:
        add_artisan(name, location, speciality, connection=sqlite_connection())
        messagebox.showinfo("Success", "Artisan added successfully!")
        artisan_name_var.set("")
        artisan_location_var.set("")
        artisan_speciality_var.set("")
        refresh_artisan_table()
    else:
        messagebox.showwarning("Warning", "All fields are required!")


# View Artisans Function
def view_artisans():
    # Fetch all artisans
    artisans = get_artisans(connection=sqlite_connection())

    # Create a new window for detailed view
    view_window = tk.Toplevel(root)
    view_window.title("Artisans Details")
    view_window.geometry("800x500")

    # Create a text widget to display artisan details
    artisan_details = scrolledtext.ScrolledText(view_window, wrap=tk.WORD)
    artisan_details.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Format and insert artisan details
    artisan_details.insert(tk.END, "ARTISANS DETAILS\n")
    artisan_details.insert(tk.END, "=" * 50 + "\n\n")

    for artisan in artisans:
        artisan_details.insert(tk.END, f"Artisan ID: {artisan[0]}\n")
        artisan_details.insert(tk.END, f"Name: {artisan[1]}\n")
        artisan_details.insert(tk.END, f"Location: {artisan[2]}\n")
        artisan_details.insert(tk.END, f"Speciality: {artisan[3]}\n")
        artisan_details.insert(tk.END, "-" * 50 + "\n\n")

    # Make the text widget read-only
    artisan_details.config(state=tk.DISABLED)


def update_selected_artisan():
    selected_item = artisan_tree.selection()
    if selected_item:
        # Get the current values of the selected artisan
        current_values = artisan_tree.item(selected_item, "values")
        artisan_id = current_values[0]

        # Open update dialog
        update_window = tk.Toplevel(root)
        update_window.title("Update Artisan")
        update_window.geometry("300x250")

        # Variables for update
        update_name_var = tk.StringVar(value=current_values[1])
        update_location_var = tk.StringVar(value=current_values[2])
        update_speciality_var = tk.StringVar(value=current_values[3])

        # Create update form
        ttk.Label(update_window, text="Name:").pack(pady=(10, 0))
        ttk.Entry(update_window, textvariable=update_name_var, width=30).pack(pady=5)

        ttk.Label(update_window, text="Location:").pack(pady=(10, 0))
        ttk.Entry(update_window, textvariable=update_location_var, width=30).pack(pady=5)

        ttk.Label(update_window, text="Speciality:").pack(pady=(10, 0))
        ttk.Entry(update_window, textvariable=update_speciality_var, width=30).pack(pady=5)

        def save_update():
            name = update_name_var.get()
            location = update_location_var.get()
            speciality = update_speciality_var.get()

            if name and location and speciality:
                # Reopen connection for update
                update_artisan(artisan_id, name, location, speciality, connection=sqlite_connection())
                messagebox.showinfo("Success", "Artisan updated successfully!")
                update_window.destroy()
                refresh_artisan_table()
            else:
                messagebox.showwarning("Warning", "All fields are required!")

        ttk.Button(update_window, text="Save Update", command=save_update).pack(pady=10)
    else:
        messagebox.showwarning("Warning", "Please select an artisan to update!")


def delete_selected_artisan():
    selected_item = artisan_tree.selection()
    if selected_item:
        artisan_id = artisan_tree.item(selected_item, "values")[0]
        delete_artisan(artisan_id, connection=sqlite_connection())
        messagebox.showinfo("Success", "Artisan deleted successfully!")
        refresh_artisan_table()
    else:
        messagebox.showwarning("Warning", "Please select an artisan to delete!")


artisan_form_frame = ttk.Frame(frame_artisans)
artisan_form_frame.pack(pady=10, padx=10, fill="x")

artisan_name_var = tk.StringVar()
artisan_location_var = tk.StringVar()
artisan_speciality_var = tk.StringVar()

ttk.Label(artisan_form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
ttk.Entry(artisan_form_frame, textvariable=artisan_name_var, width=30).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(artisan_form_frame, text="Location:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
ttk.Entry(artisan_form_frame, textvariable=artisan_location_var, width=30).grid(row=1, column=1, padx=5, pady=5)

ttk.Label(artisan_form_frame, text="Speciality:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
ttk.Entry(artisan_form_frame, textvariable=artisan_speciality_var, width=30).grid(row=2, column=1, padx=5, pady=5)

# Buttons for Artisan operations
ttk.Button(artisan_form_frame, text="Add Artisan", command=submit_artisan).grid(row=3, column=0, pady=10)
ttk.Button(artisan_form_frame, text="Update Artisan", command=update_selected_artisan).grid(row=3, column=2, pady=10)
ttk.Button(artisan_form_frame, text="Delete Artisan", command=delete_selected_artisan).grid(row=4, column=1, pady=10)
ttk.Button(artisan_form_frame, text="View Artisans", command=view_artisans).grid(row=3, column=1, pady=10)
# ARTISAN TABLE
artisan_tree = ttk.Treeview(frame_artisans, columns=("ID", "Name", "Location", "Speciality"), show="headings")
artisan_tree.heading("ID", text="ID")
artisan_tree.heading("Name", text="Name")
artisan_tree.heading("Location", text="Location")
artisan_tree.heading("Speciality", text="Speciality")
artisan_tree.pack(fill="both", expand=True, padx=10, pady=10)


def refresh_artisan_table():
    for row in artisan_tree.get_children():
        artisan_tree.delete(row)
    for artisan in get_artisans(connection=sqlite_connection()):
        artisan_tree.insert("", "end", values=artisan)


refresh_artisan_table()


# PRODUCT FORM
def submit_product():
    artisan_id = product_artisan_var.get()
    name = product_name_var.get()
    description = product_description_var.get()
    price = product_price_var.get()
    stock = product_stock_var.get()

    if artisan_id and name and price and stock:
        add_product(artisan_id, name, description, float(price), int(stock), connection=sqlite_connection())
        messagebox.showinfo("Success", "Product added successfully!")
        product_name_var.set("")
        product_description_var.set("")
        product_price_var.set("")
        product_stock_var.set("")
        refresh_product_table()
    else:
        messagebox.showwarning("Warning", "All fields are required!")


# View Products Function
def view_products():
    # Fetch all products
    products = get_products(connection=sqlite_connection())

    # Create a new window for detailed view
    view_window = tk.Toplevel(root)
    view_window.title("Products Details")
    view_window.geometry("900x600")

    # Frame for sorting options
    sort_frame = ttk.Frame(view_window)
    sort_frame.pack(pady=10, padx=10, fill='x')

    # Sorting Label and Dropdown
    ttk.Label(sort_frame, text="Sort by Stock:").pack(side=tk.LEFT, padx=(0, 10))

    # Sorting variable and options
    sort_var = tk.StringVar(value="Default")
    sort_options = ["Default", "Low to High", "High to Low"]
    sort_dropdown = ttk.Combobox(sort_frame, textvariable=sort_var, values=sort_options, width=15, state="readonly")
    sort_dropdown.pack(side=tk.LEFT, padx=(0, 10))

    # Treeview for Products
    product_tree = ttk.Treeview(view_window, columns=(
        "Product ID", "Artisan ID", "Name", "Description", "Price", "Stock"
    ), show="headings")

    # Define headings
    product_tree.heading("Product ID", text="Product ID")
    product_tree.heading("Artisan ID", text="Artisan ID")
    product_tree.heading("Name", text="Name")
    product_tree.heading("Description", text="Description")
    product_tree.heading("Price", text="Price")
    product_tree.heading("Stock", text="Stock Quantity")

    # Set column widths
    product_tree.column("Product ID", width=80, anchor='center')
    product_tree.column("Artisan ID", width=80, anchor='center')
    product_tree.column("Name", width=150)
    product_tree.column("Description", width=200)
    product_tree.column("Price", width=100, anchor='e')
    product_tree.column("Stock", width=100, anchor='center')

    # Function to populate and sort products
    def populate_products(event=None):
        # Clear existing items
        for i in product_tree.get_children():
            product_tree.delete(i)

        # Sort products based on selected option
        sorted_products = products.copy()
        if sort_var.get() == "Low to High":
            sorted_products.sort(key=lambda x: x[5])  # Sort by stock quantity
        elif sort_var.get() == "High to Low":
            sorted_products.sort(key=lambda x: x[5], reverse=True)

        # Insert products into treeview
        for product in sorted_products:
            product_tree.insert("", "end", values=product)

    # Bind sorting dropdown to populate function
    sort_dropdown.bind("<<ComboboxSelected>>", populate_products)

    # Initial population
    populate_products()

    # Add scrollbar
    scrollbar = ttk.Scrollbar(view_window, orient=tk.VERTICAL, command=product_tree.yview)
    product_tree.configure(yscroll=scrollbar.set)

    # Pack treeview and scrollbar
    product_tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


def update_selected_product():
    selected_item = product_tree.selection()
    if selected_item:
        # Get the current values of the selected product
        current_values = product_tree.item(selected_item, "values")
        product_id = current_values[0]

        # Open update dialog
        update_window = tk.Toplevel(root)
        update_window.title("Update Product")
        update_window.geometry("300x350")

        # Variables for update
        update_artisan_var = tk.StringVar(value=current_values[1])
        update_name_var = tk.StringVar(value=current_values[2])
        update_description_var = tk.StringVar(value=current_values[3])
        update_price_var = tk.StringVar(value=current_values[4])
        update_stock_var = tk.StringVar(value=current_values[5])

        # Create update form
        ttk.Label(update_window, text="Artisan ID:").pack(pady=(10, 0))
        ttk.Entry(update_window, textvariable=update_artisan_var, width=30).pack(pady=5)

        ttk.Label(update_window, text="Name:").pack(pady=(10, 0))
        ttk.Entry(update_window, textvariable=update_name_var, width=30).pack(pady=5)

        ttk.Label(update_window, text="Description:").pack(pady=(10, 0))
        ttk.Entry(update_window, textvariable=update_description_var, width=30).pack(pady=5)

        ttk.Label(update_window, text="Price:").pack(pady=(10, 0))
        ttk.Entry(update_window, textvariable=update_price_var, width=30).pack(pady=5)

        ttk.Label(update_window, text="Stock:").pack(pady=(10, 0))
        ttk.Entry(update_window, textvariable=update_stock_var, width=30).pack(pady=5)

        def save_update():
            artisan_id = update_artisan_var.get()
            name = update_name_var.get()
            description = update_description_var.get()
            price = update_price_var.get()
            stock = update_stock_var.get()

            if artisan_id and name and price and stock:
                # Reopen connection for update
                update_product(product_id, name, description, float(price), int(stock), connection=sqlite_connection())
                messagebox.showinfo("Success", "Product updated successfully!")
                update_window.destroy()
                refresh_product_table()
            else:
                messagebox.showwarning("Warning", "All fields are required!")

        ttk.Button(update_window, text="Save Update", command=save_update).pack(pady=10)
    else:
        messagebox.showwarning("Warning", "Please select a product to update!")


def delete_selected_product():
    selected_item = product_tree.selection()
    if selected_item:
        product_id = product_tree.item(selected_item, "values")[0]
        delete_product(product_id, connection=sqlite_connection())
        messagebox.showinfo("Success", "Product deleted successfully!")
        refresh_product_table()
    else:
        messagebox.showwarning("Warning", "Please select a product to delete!")


product_form_frame = ttk.Frame(frame_products)
product_form_frame.pack(pady=10, padx=10, fill="x")

product_artisan_var = tk.StringVar()
product_name_var = tk.StringVar()
product_description_var = tk.StringVar()
product_price_var = tk.StringVar()
product_stock_var = tk.StringVar()

ttk.Label(product_form_frame, text="Artisan ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
ttk.Entry(product_form_frame, textvariable=product_artisan_var, width=30).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(product_form_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
ttk.Entry(product_form_frame, textvariable=product_name_var, width=30).grid(row=1, column=1, padx=5, pady=5)

ttk.Label(product_form_frame, text="Description:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
ttk.Entry(product_form_frame, textvariable=product_description_var, width=30).grid(row=2, column=1, padx=5, pady=5)

ttk.Label(product_form_frame, text="Price:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
ttk.Entry(product_form_frame, textvariable=product_price_var, width=30).grid(row=3, column=1, padx=5, pady=5)

ttk.Label(product_form_frame, text="Stock:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
ttk.Entry(product_form_frame, textvariable=product_stock_var, width=30).grid(row=4, column=1, padx=5, pady=5)

# Buttons for Product operations
ttk.Button(product_form_frame, text="Add Product", command=submit_product).grid(row=5, column=0, pady=10)
ttk.Button(product_form_frame, text="Update Product", command=update_selected_product).grid(row=5, column=2, pady=10)
ttk.Button(product_form_frame, text="Delete Product", command=delete_selected_product).grid(row=6, column=1, pady=10)
ttk.Button(product_form_frame, text="View Products", command=view_products).grid(row=5, column=1, pady=10)
# PRODUCT TABLE
product_tree = ttk.Treeview(frame_products, columns=("ID", "ArtisanID", "Name", "Description", "Price", "Stock"),
                            show="headings")
product_tree.heading("ID", text="ID")
product_tree.heading("ArtisanID", text="Artisan ID")
product_tree.heading("Name", text="Name")
product_tree.heading("Description", text="Description")
product_tree.heading("Price", text="Price")
product_tree.heading("Stock", text="Stock")
product_tree.pack(fill="both", expand=True, padx=10, pady=10)


def refresh_product_table():
    for row in product_tree.get_children():
        product_tree.delete(row)
    for product in get_products(connection=sqlite_connection()):
        product_tree.insert("", "end", values=product)


refresh_product_table()


def parse_order_items(order_items_input):
    """
    Parse order items from a string input.

    Args:
        order_items_input (str): String in format "ProductID:Quantity,ProductID:Quantity"

    Returns:
        list of tuples: [(product_id, quantity), ...]
    """
    # Remove any whitespace
    order_items_input = order_items_input.strip()

    # Check if input is empty
    if not order_items_input:
        raise ValueError("Order items cannot be empty")

    # Split items and parse each
    try:
        order_items = []
        for item in order_items_input.split(','):
            # Split each item and convert to integers
            product_id, quantity = map(str.strip, item.split(':'))
            order_items.append((int(product_id), int(quantity)))

        return order_items
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid order items format. Use 'ProductID:Quantity'. Error: {e}")


def submit_order():
    customer_name = order_customer_var.get().strip()
    order_items_input = order_items_var.get()

    try:
        # Parse order items using the new parsing function
        order_items = parse_order_items(order_items_input)

        if customer_name and order_items:
            # Verify products exist and have enough stock before placing order
            connection = sqlite_connection()
            cursor = connection.cursor()

            valid_order = True
            for product_id, quantity in order_items:
                cursor.execute("SELECT StockQuantity FROM Products WHERE ProductID = ?", (product_id,))
                result = cursor.fetchone()

                if not result:
                    messagebox.showerror("Error", f"Product ID {product_id} does not exist")
                    valid_order = False
                    break

                if result[0] < quantity:
                    messagebox.showerror("Error", f"Insufficient stock for Product ID {product_id}")
                    valid_order = False
                    break

            cursor.close()
            connection.close()

            if valid_order:
                order_id = place_order(customer_name, order_items, connection=sqlite_connection())

                if order_id:
                    messagebox.showinfo("Success", f"Order placed successfully! Order ID: {order_id}")
                    order_customer_var.set("")
                    order_items_var.set("")
                    refresh_order_table()
                    refresh_product_table()  # Update product stock in the table
                else:
                    messagebox.showerror("Error", "Failed to place order. Check product availability.")
        else:
            messagebox.showwarning("Warning", "Customer name and order items are required!")

    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An error occurred: {str(e)}")


# View Orders Function
def view_order_details():
    selected_item = order_tree.selection()
    if selected_item:
        order_id = order_tree.item(selected_item, "values")[0]

        # Get full order details
        order_details = get_order_details(order_id, connection=sqlite_connection())

        if order_details:
            # Create a detailed view window
            details_window = tk.Toplevel(root)
            details_window.title(f"Order {order_id} Details")
            details_window.geometry("600x400")

            # Create text widget for details
            details_text = scrolledtext.ScrolledText(details_window, wrap=tk.WORD)
            details_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            # Format and insert order details
            details_text.insert(tk.END, f"Order ID: {order_details['order_id']}\n")
            details_text.insert(tk.END, f"Customer: {order_details['customer_name']}\n")
            details_text.insert(tk.END, f"Order Date: {order_details['order_date']}\n")
            details_text.insert(tk.END, f"Total Amount: ${order_details['total_amount']:.2f}\n\n")

            details_text.insert(tk.END, "ORDER ITEMS:\n")
            details_text.insert(tk.END, "-" * 50 + "\n")

            for item in order_details['items']:
                details_text.insert(tk.END,
                                    f"Product ID: {item[0]}, "
                                    f"Product Name: {item[1]}, "
                                    f"Quantity: {item[2]}, "
                                    f"Price: ${item[3]:.2f}, "
                                    f"Subtotal: ${item[4]:.2f}\n"
                                    )

            # Make text read-only
            details_text.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Order Details", "Could not retrieve order details.")
    else:
        messagebox.showwarning("Warning", "Please select an order to view!")


# Delete Order Function
def delete_selected_order():
    selected_item = order_tree.selection()
    if selected_item:
        order_id = order_tree.item(selected_item, "values")[0]

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete Order {order_id}?")

        if confirm:
            success = delete_order(order_id, connection=sqlite_connection())

            if success:
                messagebox.showinfo("Success", f"Order {order_id} deleted successfully!")
                refresh_order_table()
            else:
                messagebox.showerror("Error", f"Failed to delete Order {order_id}")
    else:
        messagebox.showwarning("Warning", "Please select an order to delete!")


# Order Form Frame
order_form_frame = ttk.Frame(frame_orders)
order_form_frame.pack(pady=10, padx=10, fill="x")

# Order Variables
order_customer_var = tk.StringVar()
order_items_var = tk.StringVar()  # Will store product IDs and quantities

# Order Form Labels and Entries
ttk.Label(order_form_frame, text="Customer Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
ttk.Entry(order_form_frame, textvariable=order_customer_var, width=30).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(order_form_frame, text="Order Items (ProductID:Quantity):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
ttk.Entry(order_form_frame, textvariable=order_items_var, width=30).grid(row=1, column=1, padx=5, pady=5)

# Buttons for Order operations
ttk.Button(order_form_frame, text="Place Order", command=submit_order).grid(row=2, column=0, pady=10)
ttk.Button(order_form_frame, text="View Order Details", command=view_order_details).grid(row=2, column=1, pady=10)
ttk.Button(order_form_frame, text="Delete Order", command=delete_selected_order).grid(row=2, column=2, pady=10)

# Order Table
order_tree = ttk.Treeview(frame_orders, columns=("ID", "CustomerName", "OrderDate", "TotalAmount"), show="headings")
order_tree.heading("ID", text="Order ID")
order_tree.heading("CustomerName", text="Customer Name")
order_tree.heading("OrderDate", text="Order Date")
order_tree.heading("TotalAmount", text="Total Amount")
order_tree.pack(fill="both", expand=True, padx=10, pady=10)


# Refresh Order Table Function
def refresh_order_table():
    for row in order_tree.get_children():
        order_tree.delete(row)
    for order in get_orders(connection=sqlite_connection()):
        order_tree.insert("", "end", values=order)


# Initial table refresh
refresh_order_table()
# Run the main loop (placed at the very end)
root.mainloop()
