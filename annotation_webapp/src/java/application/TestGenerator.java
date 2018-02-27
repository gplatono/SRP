/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package application;

import beans.Scene;
import beans.TestInstance;
import beans.Testcase;
import beans.User;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.URLDecoder;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;
import javax.persistence.Convert;

/**
 *
 * @author gplatono
 */
public class TestGenerator {
    
    private static String[] relations = {
        "above, ", 
        "below, ", 
        "to the right of,",
        "to the left of,",
        "in front of,",
        "behind,",
        "near,",
        "at,",
        "in,",
        "over,",
        "under,",
        "between,",
        "on,",
        "touching."};    
    
    public TestGenerator(String sceneDirectory) {
        
    }
    
    public static TestInstance generate(User user) throws Exception {
        TestInstance testInstance = new TestInstance();        
        //ArrayList<Testcase> testcases = JDBCHelper.getEnabledTestcases();
        ArrayList<Testcase> testcasesDescr = JDBCHelper.getUnansweredForUser(user, 1); 
        ArrayList<Testcase> testcasesTruth = JDBCHelper.getUnansweredForUser(user, 0); 
        if(testcasesDescr.isEmpty() && testcasesTruth.isEmpty())
            return null;
        else if (!testcasesDescr.isEmpty()) {
            testInstance.setTestcase(testcasesDescr.get(new Random().nextInt(testcasesDescr.size())));
        }
        else {
            testInstance.setTestcase(testcasesTruth.get(new Random().nextInt(testcasesTruth.size())));
        }
            
        testInstance.setUserID(user.getId());
        //testInstance.setTestcase(testcases.get(new Random().nextInt(testcases.size())));
        Scene testScene = JDBCHelper.getSceneById(testInstance.getTestcase().getSceneID());
        testInstance.setImagePath(testScene.getPath());

        if(!testInstance.getTestcase().getRelation().equals("-")) { 
            testInstance.setQuery("Is " + testInstance.getTestcase().getRelatum() + " " + 
                    testInstance.getTestcase().getRelation() + " " + testInstance.getTestcase().getReferent1()+ "?");
        }
        else {            
            String testQuery = "Where is " + testInstance.getTestcase().getRelatum() + " in the presented scene? Please describe its location relative to other objects. Use the following relations only:<br> ";
            testQuery += "[<b>above, below, to the right of, to the left of, in front of, behind, near, at, in, over, under, between, on, touching</b>].";
            //for (String rel : relations) {
            //    testQuery += "<b>" + rel + "</b>";
            //}
            testInstance.setQuery(testQuery);
        }               

        return testInstance;
    }
}