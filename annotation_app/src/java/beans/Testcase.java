/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package beans;

/**
 *
 * @author gplatono
 */
public class Testcase {
    public Testcase() {
        
    }
    
    private int queryType;
    private int sceneID;
    private String scenePath;
    private String imagePath;
    private String testQuery;
    private String[] sceneObjects;    

    public int getQueryType() {
        return queryType;
    }

    public void setQueryType(int queryType) {
        this.queryType = queryType;
    }
    
    public int getSceneID() {
        return sceneID;
    }

    public void setSceneID(int sceneID) {
        this.sceneID = sceneID;
    }
    
    public String getScenePath() {
        return scenePath;
    }

    public void setScenePath(String scenePath) {
        this.scenePath = scenePath;
    }

    public String getImagePath() {
        return imagePath;
    }

    public void setImagePath(String imagePath) {
        this.imagePath = imagePath;
    }

    public String getTestQuery() {
        return testQuery;
    }

    public void setTestQuery(String testQuery) {
        this.testQuery = testQuery;
    }

    public String[] getSceneObjects() {
        return sceneObjects;
    }

    public void setSceneObjects(String[] sceneObjects) {
        this.sceneObjects = sceneObjects;
    }
    
    
}
