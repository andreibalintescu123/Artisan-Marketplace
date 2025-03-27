import sqlite3
import pyodbc

DB_PATH = "D:/JavaProjects/Laboratories/ArtisanMarketplace/python/artisan_marketplace.db"

def microsoft_sql_connection():
    server = 'DESKTOP-ANDREI-B\\SQLEXPRESS'
    database = 'Artisan-Marketplace'
    trusted_connection = 'yes'  # Use Windows authentication
    driver = '{ODBC Driver 17 for SQL Server}'  # Try 18 or 13 if 17 doesn't work

    # Connection string
    conn_str = (
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection={trusted_connection};"
        f"TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)

def postgres_connection():
    conn_str = (
        "DRIVER={PostgreSQL Unicode(x64)};"
        "SERVER=localhost;"
        "PORT=5432;"
        "DATABASE=postgres;"
        "UID=postgres;"
        "PWD=andrei123;"
    )
    return pyodbc.connect(conn_str)

def sqlite_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_tables():
    connection = microsoft_sql_connection()
    cursor = connection.cursor()

    # Create tables
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Artisans' AND xtype='U')
    CREATE TABLE Artisans (
        ArtisanID INTEGER IDENTITY(1,1) PRIMARY KEY,
        Name NVARCHAR(255) NOT NULL,
        Location NVARCHAR(255) NOT NULL,
        Speciality NVARCHAR(255) NOT NULL
    );

    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Products' AND xtype='U')
    CREATE TABLE Products (
        ProductID INTEGER IDENTITY(1,1) PRIMARY KEY,
        ArtisanID INTEGER NOT NULL,
        Name NVARCHAR(255) NOT NULL,
        Description NVARCHAR(MAX),
        Price DECIMAL(10,2) NOT NULL,
        StockQuantity INTEGER NOT NULL,
        FOREIGN KEY (ArtisanID) REFERENCES Artisans(ArtisanID) ON DELETE CASCADE
    );

    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Orders' AND xtype='U')
    CREATE TABLE Orders (
        OrderID INTEGER IDENTITY(1,1) PRIMARY KEY,
        CustomerName NVARCHAR(255) NOT NULL,
        OrderDate DATETIME NOT NULL,
        TotalAmount DECIMAL(10,2) NOT NULL
    );

    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='OrderItems' AND xtype='U')
    CREATE TABLE OrderItems (
        OrderItemID INTEGER IDENTITY(1,1) PRIMARY KEY,
        OrderID INTEGER NOT NULL,
        ProductID INTEGER NOT NULL,
        Quantity INTEGER NOT NULL,
        Price DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID) ON DELETE CASCADE
    );
    """)

    connection.commit()
    connection.close()
    print("Microsoft SQL Server database tables created successfully.")

if __name__ == "__main__":
    create_tables()