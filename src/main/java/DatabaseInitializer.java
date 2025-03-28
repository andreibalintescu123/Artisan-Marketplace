import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;


public class DatabaseInitializer {
    // Remove the extra quotes and fix the backslashes
    private static final String URL = "jdbc:sqlserver://DESKTOP-ANDREI-B\\SQLEXPRESS;databaseName=Artisan-Marketplace;integratedSecurity=true;encrypt=true;trustServerCertificate=true;";

    public static void main(String[] args) {
        try (Connection conn = DriverManager.getConnection(URL);
             Statement stmt = conn.createStatement()) {

            // SQL Server compatible syntax
            String createTablesSQL = """
                        CREATE TABLE IF NOT EXISTS Artisans (
                            ArtisanID INT IDENTITY(1,1) PRIMARY KEY,
                            Name NVARCHAR(255) NOT NULL,
                            Location NVARCHAR(255) NOT NULL,
                            Speciality NVARCHAR(255) NOT NULL
                        );    
                        CREATE TABLE IF NOT EXISTS Products(
                            ProductID INT IDENTITY(1,1) PRIMARY KEY,
                            ArtisanID INT NOT NULL,
                            Name NVARCHAR(255) NOT NULL,
                            Description NVARCHAR(255),
                            Price DECIMAL(10,2) NOT NULL,
                            StockQuantity INT NOT NULL,
                            FOREIGN KEY (ArtisanID) REFERENCES Artisans(ArtisanID) ON DELETE CASCADE
                        );
                    
                        CREATE TABLE IF NOT EXISTS Orders (
                            OrderID INT IDENTITY(1,1) PRIMARY KEY,
                            CustomerName NVARCHAR(255) NOT NULL,
                            OrderDate DATETIME NOT NULL DEFAULT DATETIME(),
                            TotalAmount DECIMAL(10,2) NOT NULL
                        );
                    
                        CREATE TABLE IF NOT EXISTS OrderItems (
                            OrderItemID INT IDENTITY(1,1) PRIMARY KEY,
                            OrderID INT NOT NULL,
                            ProductID INT NOT NULL,
                            Quantity INT NOT NULL,
                            Price DECIMAL(10,2) NOT NULL,
                            FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
                            FOREIGN KEY (ProductID) REFERENCES Products(ProductID) ON DELETE CASCADE
                        );
                    """;

            stmt.executeUpdate(createTablesSQL);
            System.out.println("Tables created successfully in Artisan-Marketplace database.");

        } catch (SQLException e) {
            System.err.println("Error initializing database:");
            e.printStackTrace();
        }
    }
}