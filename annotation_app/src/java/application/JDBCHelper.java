/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package application;

import beans.Testcase;
import java.sql.*;
import java.util.ArrayList;

/**
 *
 * @author gplatono
 */
public class JDBCHelper {
        
    private final String JDBC_DRIVER = "org.postgresql.Driver";  
    private final String DB_URL = "jdbc:postgresql://localhost:5432/srp";
    private final String USER = "gplatono";
    private final String PASS = "";
    private static Connection dbConnection = null;
    private static int testSize;
    
    public JDBCHelper() {
        try {
            Class.forName(JDBC_DRIVER);
            dbConnection = DriverManager.getConnection(DB_URL, USER, PASS);
            Statement statement = dbConnection.createStatement();
            
        }
        catch(Exception ex) {
            String str = ex.getMessage();
            int i = 0;
        }                
    }
    
    public static ArrayList<String> getScenes() throws SQLException {        
        ArrayList<String> paths = new ArrayList<String>();
        Statement statement = dbConnection.createStatement();
        String query = "SELECT * FROM SCENES";
        ResultSet result = statement.executeQuery(query);        
        while(result.next()) {
            paths.add(result.getString("path"));
        }
        result.close();
        statement.close();
        return paths;
    }
    
    static get
    
    public static void saveResponse(Testcase testcase) {
        //Statement statement = dbConnection.createStatement();
        //String query = "INSERT INTO "
    }
}
