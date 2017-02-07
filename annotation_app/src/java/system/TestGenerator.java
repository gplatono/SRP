/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package system;

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
    
    public static Testcase generate(String datasetPath) {
        Testcase testcase = new Testcase();
        PrintWriter writer = null;
        
        try{
        writer = new PrintWriter(datasetPath + "/Log", "UTF-8");
        }
        catch(Exception ex) {
        }
        
        try {                       
        ArrayList<File> subdirs = new ArrayList<File>();
        for (File file : (new File(datasetPath)).listFiles()) {
            if(file.isDirectory()) {
                subdirs.add(file);
            }
        }
        
        Random rand = new Random();
        int index = rand.nextInt(subdirs.size());
        String scenePath = subdirs.get(index).getPath();
        
        testcase.setScenePath(subdirs.get(index).getPath());
        testcase.setImagePath("scenes" + scenePath.split("scenes")[1] +File.separator + "scene.png");
        
        int queryType = rand.nextInt(2);
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
        
        String testQuery = null;
        if(queryType == 0) { 
            int relatumIndex = rand.nextInt(objectNames.size());
            int referentIndex = rand.nextInt(objectNames.size());
            int relationIndex = rand.nextInt(relations.length);        
            while (relatumIndex == referentIndex) {
                referentIndex = rand.nextInt(objectNames.size());
            }
            testQuery = "Is the " + objectNames.get(relatumIndex) + " " + relations[relationIndex] + " the " + objectNames.get(referentIndex) + "?";
        }
        else {
            int relatumIndex = rand.nextInt(objectNames.size());
            testQuery = "Describe the location of the " + objectNames.get(relatumIndex) + ":";
        }        
        
        testcase.setSceneObjects(objectNames.toArray(new String[objectNames.size()]));        
        testcase.setTestQuery(testQuery);
        }
        catch(Exception ex) {     
            writer.println(ex.getMessage());
        }
        return testcase;
    }
    
    private void sceneSelector() {
        
    }
}
