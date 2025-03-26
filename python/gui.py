import tkinter as tk
from tkinter import ttk, messagebox
from CRUD.artisan import *
from CRUD.product import *

# Create the main window
root = tk.Tk()
root.title("Artisan Marketplace")
root.geometry("1250x400")

# Create a Notebook (Tabs)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Create frames for different sections
frame_artisans = ttk.Frame(notebook)
frame_products = ttk.Frame(notebook)

notebook.add(frame_artisans, text="Artisans")
notebook.add(frame_products, text="Products")

### ARTISAN FORM ###
def submit_artisan():
    name = artisan_name_var.get()
    location = artisan_location_var.get()
    speciality = artisan_speciality_var.get()

    if name and location and speciality:
        add_artisan(name, location, speciality)
        messagebox.showinfo("Success", "Artisan added successfully!")
        artisan_name_var.set("")
        artisan_location_var.set("")
        artisan_speciality_var.set("")
        refresh_artisan_table()
    else:
        messagebox.showwarning("Warning", "All fields are required!")

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

ttk.Button(artisan_form_frame, text="Add Artisan", command=submit_artisan).grid(row=3, columnspan=2, pady=10)

### ARTISAN TABLE ###
artisan_tree = ttk.Treeview(frame_artisans, columns=("ID", "Name", "Location", "Speciality"), show="headings")
artisan_tree.heading("ID", text="ID")
artisan_tree.heading("Name", text="Name")
artisan_tree.heading("Location", text="Location")
artisan_tree.heading("Speciality", text="Speciality")
artisan_tree.pack(fill="both", expand=True, padx=10, pady=10)

def refresh_artisan_table():
    for row in artisan_tree.get_children():
        artisan_tree.delete(row)
    for artisan in get_artisans():
        artisan_tree.insert("", "end", values=artisan)

refresh_artisan_table()

### PRODUCT FORM ###
def submit_product():
    artisan_id = product_artisan_var.get()
    name = product_name_var.get()
    description = product_description_var.get()
    price = product_price_var.get()
    stock = product_stock_var.get()

    if artisan_id and name and price and stock:
        add_product(artisan_id, name, description, float(price), int(stock))
        messagebox.showinfo("Success", "Product added successfully!")
        product_name_var.set("")
        product_description_var.set("")
        product_price_var.set("")
        product_stock_var.set("")
        refresh_product_table()
    else:
        messagebox.showwarning("Warning", "All fields are required!")

def delete_selected_product():
    selected_item = product_tree.selection()
    if selected_item:
        product_id = product_tree.item(selected_item, "values")[0]
        delete_product(product_id)
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

ttk.Button(product_form_frame, text="Add Product", command=submit_product).grid(row=5, columnspan=2, pady=10)
ttk.Button(product_form_frame, text="Delete Product", command=delete_selected_product).grid(row=5, column=3, columnspan=2, pady=10)

### PRODUCT TABLE ###
product_tree = ttk.Treeview(frame_products, columns=("ID", "ArtisanID", "Name", "Description", "Price", "Stock"), show="headings")
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
    for product in get_products():
        product_tree.insert("", "end", values=product)

refresh_product_table()


# Run the main loop (placed at the very end)
root.mainloop()
