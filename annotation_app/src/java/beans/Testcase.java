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
    
    private int id;
    private int queryType;
    private int sceneID;
    private String relation;
    private String relatum;
    private String referent1;
    private String referent2;
    //private String scenePath;
    //private String imagePath;
    //private String testQuery;
    //private String[] sceneObjects;    

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getRelation() {
        return relation;
    }

    public void setRelation(String relation) {
        this.relation = relation;
    }

    public String getRelatum() {
        return relatum;
    }

    public void setRelatum(String relatum) {
        this.relatum = relatum;
    }

    public String getReferent1() {
        return referent1;
    }

    public void setReferent1(String referent1) {
        this.referent1 = referent1;
    }

    public String getReferent2() {
        return referent2;
    }

    public void setReferent2(String referent2) {
        this.referent2 = referent2;
    }

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
}
