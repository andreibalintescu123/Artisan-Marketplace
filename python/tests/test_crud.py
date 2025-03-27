from python.CRUD.product import *
from python.CRUD.artisan import *

# Add an artisan
add_artisan("John Doe", "New York", "Pottery", connection=sqlite_connection())

# Add a product
add_product(1, "Ceramic Vase", "Handmade ceramic vase", 25.99, 10, connection=sqlite_connection())

# Fetch and display all artisans
print("Artisans:", get_artisans(connection=sqlite_connection()))

# Fetch and display all products
print("Products:", get_products(connection=sqlite_connection()))

# Update a product
update_product(1, "Large Ceramic Vase", "Handmade large ceramic vase", 30.99, 8, connection=sqlite_connection())

# Fetch after deletion
print("Final Products:", get_products(connection=sqlite_connection()))
