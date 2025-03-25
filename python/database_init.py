import sqlite3

def initialize_sqlite():
    connection = sqlite3.connect("artisans_platform.db")  # Creates the database file if not exists
    cursor = connection.cursor()

    # Create tables
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Artisans (
            ArtisanID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Location TEXT NOT NULL,
            Speciality TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Products (
            ProductID INTEGER PRIMARY KEY,
            ArtisanID INTEGER NOT NULL,
            Name TEXT NOT NULL,
            Description TEXT,
            Price REAL NOT NULL,
            StockQuantity INTEGER NOT NULL,
            FOREIGN KEY (ArtisanID) REFERENCES Artisans(ArtisanID) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS Orders (
            OrderID INTEGER PRIMARY KEY,
            CustomerName TEXT NOT NULL,
            OrderDate TEXT NOT NULL,
            TotalAmount REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS OrderItems (
            OrderItemID INTEGER PRIMARY KEY,
            OrderID INTEGER NOT NULL,
            ProductID INTEGER NOT NULL,
            Quantity INTEGER NOT NULL,
            Price REAL NOT NULL,
            FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID) ON DELETE CASCADE
        );
    """)

    connection.commit()
    connection.close()
    print("SQLite database initialized successfully.")


if __name__ == "__main__":
    initialize_sqlite()
