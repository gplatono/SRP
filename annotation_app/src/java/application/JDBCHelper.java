/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package application;

import beans.TestInstance;
import beans.Testcase;
import java.sql.*;
import java.util.ArrayList;
import java.util.Random;

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
    
    public static ArrayList<Testcase> getTestcases() throws SQLException {
        ArrayList<Testcase> testcases = new ArrayList<>();
        Statement statement = dbConnection.createStatement();
        String query = "SELECT * FROM testcases;";
        ResultSet results = statement.executeQuery(query);
        while(results.next()) {
            Testcase testcase = new Testcase();
            testcase.setId(results.getInt("ID"));
            testcase.setQueryType(results.getInt("TYPE"));
            testcase.setSceneID(results.getInt("SCENE_ID"));
            testcase.setRelation(results.getString("RELATION"));
            testcase.setRelatum(results.getString("RELATUM"));
            testcase.setReferent1(results.getString("REFERENT1"));
            testcase.setReferent2(results.getString("REFERENT2"));
            testcases.add(testcase);
        }
        results.close();
        statement.close();
        return testcases;
    }
    
    public static ArrayList<String> getScenes() throws SQLException {        
        ArrayList<String> paths = new ArrayList<String>();
        Statement statement = dbConnection.createStatement();
        String query = "SELECT * FROM SCENES";
        ResultSet results = statement.executeQuery(query);        
        while(results.next()) {
            paths.add(results.getString("path"));
        }
        results.close();
        statement.close();
        return paths;
    }
    
    public static void saveResponse(TestInstance testInstance) throws SQLException {
        Statement statement = dbConnection.createStatement();
        String query = "INSERT INTO responses VALUES (";
        query += (new Random().nextInt(1000000)) + ","; 
        query += testInstance.getTestcase().getId() + ",";
        query += testInstance.getUserID() + ",";
        query += "'" + testInstance.getResponse() + "'" + ");";
        statement.executeUpdate(query);
        statement.close();        
    }
}
