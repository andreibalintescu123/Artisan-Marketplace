package IsolationLevels;

import java.sql.*;

public class RepeatableRead {
    private static final String URL = "jdbc:sqlserver://DESKTOP-ANDREI-B\\SQLEXPRESS;databaseName=Artisan-Marketplace;integratedSecurity=true;encrypt=true;trustServerCertificate=true;";

    public static void main(String[] args) throws SQLException {
        try (Connection conn = DriverManager.getConnection(URL)) {
            conn.setTransactionIsolation(Connection.TRANSACTION_REPEATABLE_READ);
            conn.setAutoCommit(false);

            Statement stmt = conn.createStatement();
            stmt.executeQuery("SELECT COUNT(*) FROM Products WHERE ArtisanID = 1");
            ResultSet rs = stmt.getResultSet();
            rs.next();
            int count = rs.getInt(1);

            Thread.sleep(10000);

            System.out.println("Count read first time: " + count);
            stmt.executeQuery("SELECT COUNT(*) FROM Products WHERE ArtisanID = 1");
            rs = stmt.getResultSet();
            rs.next();
            int count2 = rs.getInt(1);
            System.out.println("Count read second time: " + count2);
            conn.commit();
        } catch (SQLException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }
}
