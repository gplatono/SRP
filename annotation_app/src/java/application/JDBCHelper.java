/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package application;

import beans.Testcase;
import java.sql.*;

/**
 *
 * @author gplatono
 */
public class JDBCHelper {
        
    private final String JDBC_DRIVER = "org.postgresql.Driver";  
    private final String DB_URL = "jdbc:postgresql://localhost:5432/srp";
    private final String USER = "gplatono";
    private final String PASS = "";
    private Connection dbConnection = null;
    public JDBCHelper() {
        try {
            Class.forName(JDBC_DRIVER);
            dbConnection = DriverManager.getConnection(DB_URL, USER, PASS);
        }
        catch(Exception ex) {
            
        }                
    }
    
    public static void saveResponse(Testcase testcase) {
        Statement statement = dbConnection.createStatement();
        String query = "INSERT INTO "
    }
}
