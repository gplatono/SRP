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
import java.util.ArrayList;
import java.util.Random;
import javax.persistence.Convert;

/**
 *
 * @author gplatono
 */
public class TestGenerator {
    public TestGenerator(String sceneDirectory) {
        
    }
    
    public static Testcase generate() {
        Testcase testcase = new Testcase();        
        ArrayList<File> subdirs = new ArrayList<File>();
        for (File file : (new File("/scenes")).listFiles()) {
            if(file.isDirectory()) {
                subdirs.add(file);
            }
        }
        Random rand = new Random();
        int index = rand.nextInt(subdirs.size());
        testcase.setScenePath(subdirs.get(index).getPath());
        testcase.setImagePath(index + File.separator + "scene.png");
        testcase.setSceneObjects(index + File.separator + "object_list");
        ArrayList<String> objects = new ArrayList<String>();
        FileInputStream in = new FileInputStream(new File(index + File.separator + "object_list"));
        
	//Construct BufferedReader from InputStreamReader
	BufferedReader reader = new BufferedReader(new InputStreamReader(in));
 
	String line = null;
	while ((line = reader.readLine()) != null) {
		System.out.println(line);
	}
 
	br.close();
        String[] object
        testcase.setTestQuery(testQuery);
        return testcase;
    }
    
    private void cceneSelector() {
        
    }
}
