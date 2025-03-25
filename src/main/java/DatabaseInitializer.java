import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class DatabaseInitializer {
    private static final String URL = "jdbc:postgresql://localhost:5432/postgres"; // Adjust if needed
    private static final String USER = "postgres";
    private static final String PASSWORD = "andrei123";

    public static void main(String[] args) {
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
             Statement stmt = conn.createStatement()) {

            // Create tables
            String createTablesSQL = """
                CREATE TABLE IF NOT EXISTS Artisans (
                    ArtisanID SERIAL PRIMARY KEY,
                    Name VARCHAR(255) NOT NULL,
                    Location VARCHAR(255) NOT NULL,
                    Speciality VARCHAR(255) NOT NULL
                );

                CREATE TABLE IF NOT EXISTS Products (
                    ProductID SERIAL PRIMARY KEY,
                    ArtisanID INT NOT NULL,
                    Name VARCHAR(255) NOT NULL,
                    Description TEXT,
                    Price DECIMAL(10,2) NOT NULL,
                    StockQuantity INT NOT NULL,
                    FOREIGN KEY (ArtisanID) REFERENCES Artisans(ArtisanID) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS Orders (
                    OrderID SERIAL PRIMARY KEY,
                    CustomerName VARCHAR(255) NOT NULL,
                    OrderDate TIMESTAMP NOT NULL DEFAULT NOW(),
                    TotalAmount DECIMAL(10,2) NOT NULL
                );

                CREATE TABLE IF NOT EXISTS OrderItems (
                    OrderItemID SERIAL PRIMARY KEY,
                    OrderID INT NOT NULL,
                    ProductID INT NOT NULL,
                    Quantity INT NOT NULL,
                    Price DECIMAL(10,2) NOT NULL,
                    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
                    FOREIGN KEY (ProductID) REFERENCES Products(ProductID) ON DELETE CASCADE
                );
            """;

            stmt.executeUpdate(createTablesSQL);
            System.out.println("PostgreSQL database initialized successfully.");

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
