package IsolationLevels;

import java.sql.*;

public class ReadUncommitted {
    private static final String URL = "jdbc:sqlserver://DESKTOP-ANDREI-B\\SQLEXPRESS;databaseName=Artisan-Marketplace;integratedSecurity=true;encrypt=true;trustServerCertificate=true;";

    public static void main(String[] args) throws SQLException {
        try (Connection conn = DriverManager.getConnection(URL)) {
            conn.setTransactionIsolation(Connection.TRANSACTION_READ_UNCOMMITTED);
            conn.setAutoCommit(false);

            Statement stmt = conn.createStatement();
            stmt.executeQuery("SELECT Price from Products WHERE ProductID = 4");
            ResultSet rs = stmt.getResultSet();
            rs.next();
            double price = rs.getDouble(1);
            System.out.println("Price read: " + price);
            conn.commit();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
