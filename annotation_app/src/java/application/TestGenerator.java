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
        "over",
        "on"};
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
        
        
        
        /*ArrayList<File> subdirs = new ArrayList<File>();
        for (File file : (new File(datasetPath)).listFiles()) {
            if(file.isDirectory()) {
                subdirs.add(file);
            }
        }*/
        
        Random rand = new Random();
        testcase = testcases.get(rand.nextInt(testcases.size()));
        testInstance.setTestcase(testcase);
        testInstance.setScenePath("scenes" + File.separator + scenePaths.get(testInstance.getTestcase().getSceneID() - 1));
        testInstance.setImagePath(testInstance.getScenePath() + "scene.jpg");
        //int index = rand.nextInt(subdirs.size());
        //String scenePath = subdirs.get(index).getPath();
        
        //testcase.setScenePath(subdirs.get(index).getPath());
        //testcase.setImagePath("scenes" + scenePath.split("scenes")[1] + File.separator + "scene.jpg");
        
        /*int queryType = rand.nextInt(2);
        testcase.setQueryType(queryType);        
        
        ArrayList<String> objectNames = new ArrayList<String>();
        try {
            FileInputStream in = new FileInputStream(new File(scenePath + File.separator + "data"));
            BufferedReader reader = new BufferedReader(new InputStreamReader(in));

            String objectName = reader.readLine();
            while (objectName != null) {
                    objectNames.add(objectName);
                    objectName = reader.readLine();
            }
            reader.close();
        }
        catch (IOException ex) {
            writer.println(ex.getMessage());
        }
        */
        String testQuery = null;
        if(testInstance.getTestcase().getQueryType() == 1) { 
            //int relatumIndex = rand.nextInt(objectNames.size());
            //int referentIndex = rand.nextInt(objectNames.size());
            //int relationIndex = rand.nextInt(relations.length);        
            //while (relatumIndex == referentIndex) {
             //   referentIndex = rand.nextInt(objectNames.size());
            //}
            //testQuery = "Is the " + objectNames.get(relatumIndex) + " " + relations[relationIndex] + " the " + objectNames.get(referentIndex) + "?";
            testQuery = "Is " + testInstance.getTestcase().getRelatum() + " " + 
                    testInstance.getTestcase().getRelation() + " " + testInstance.getTestcase().getReferent1()+ "?";
        }
        else {
            //int relatumIndex = rand.nextInt(objectNames.size());
            //testQuery = "Describe the location of the " + objectNames.get(relatumIndex) + " relative to other objects, present in the scene. Use the following relations: Above, Below, Behind, In Front Of, To The Left, To The Right, On, At, Near, Over. Comparatives and superlatives are allowed.";
            testQuery = "Describe the location of " + testInstance.getTestcase().getRelatum() + " relative to other objects, present in the scene. Use the following relations: Above, Below, Behind, In Front Of, To The Left, To The Right, On, At, Near, Over.";
        }        
        
        //testcase.setSceneObjects(objectNames.toArray(new String[objectNames.size()]));        
        //testcase.setTestQuery(testQuery);
        testInstance.setQuery(testQuery);
        }
        catch(Exception ex) {     
            writer.println(ex.getMessage());
        }
        return testInstance;
    }
    
    private void sceneSelector() {
        
    }
}
