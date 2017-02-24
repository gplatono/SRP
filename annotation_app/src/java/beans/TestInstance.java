/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package beans;

import java.io.Serializable;

/**
 *
 * @author georgiy
 */
public class TestInstance implements Serializable {
    
    private Testcase testcase;
    private String scenePath;
    private String imagePath;
    private String query;
    private int userID;
    private String response;
    
    public TestInstance() {
        
    }

    public Testcase getTestcase() {
        return testcase;
    }

    public void setTestcase(Testcase testcase) {
        this.testcase = testcase;
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

    public String getQuery() {
        return query;
    }

    public void setQuery(String query) {
        this.query = query;
    }

    public int getUserID() {
        return userID;
    }

    public void setUserID(int userID) {
        this.userID = userID;
    }

    public String getResponse() {
        return response;
    }

    public void setResponse(String response) {
        this.response = response;
    }   
}
