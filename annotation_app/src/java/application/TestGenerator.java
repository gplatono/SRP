/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package application;

import beans.TestInstance;
import beans.Testcase;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.URLDecoder;
import java.util.ArrayList;
import java.util.Random;
import javax.persistence.Convert;

/**
 *
 * @author gplatono
 */
public class TestGenerator {
    
    private static String[] relations = {
        "above", 
        "below", 
        "to the right",
        "to the left",
        "in front of",
        "behind",
        "near",
        "at",
        "in",
        "over",
        "under",
        "between",
        "on",
        "touching"};
    public TestGenerator(String sceneDirectory) {
        
    }
    
    public static TestInstance generate(String appPath) {
        Testcase testcase = new Testcase();
        TestInstance testInstance = new TestInstance();
        PrintWriter writer = null;
        String datasetPath = appPath + "scenes/";        
        
        try{
        writer = new PrintWriter(appPath + "Log", "UTF-8");
        }
        catch(Exception ex) {
        }
        
        try {   
            JDBCHelper helper = new JDBCHelper();
        ArrayList<String> scenePaths = JDBCHelper.getScenes();
        ArrayList<Testcase> testcases = JDBCHelper.getTestcases();
        
        Random rand = new Random();
        testcase = testcases.get(rand.nextInt(testcases.size()));
        testInstance.setTestcase(testcase);
        testInstance.setScenePath("scenes" + File.separator + scenePaths.get(testInstance.getTestcase().getSceneID() - 1));
        testInstance.setImagePath(testInstance.getScenePath() + "scene.jpg");
        
        String testQuery = null;
        if(testInstance.getTestcase().getQueryType() == 1) { 
            testQuery = "Is " + testInstance.getTestcase().getRelatum() + " " + 
                    testInstance.getTestcase().getRelation() + " " + testInstance.getTestcase().getReferent1()+ "?";
        }
        else {
            testQuery = "Where is " + testInstance.getTestcase().getRelatum() + " in the presented scene? Please describe its location relative to other objects. Use the following relations only:<br> ";
            for (String rel : relations) {
                testQuery += "<b>" + rel + "</b><br>";
            }
        }        
        
        testInstance.setQuery(testQuery);
        }
        catch(Exception ex) {     
            writer.println(ex.getMessage());
        }
        return testInstance;
    }
    
}
