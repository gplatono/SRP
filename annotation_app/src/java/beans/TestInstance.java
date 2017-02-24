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
}
