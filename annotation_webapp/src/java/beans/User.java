/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package beans;

import java.io.Serializable;

/**
 *
 * @author gplatono
 */
public class User implements Serializable {
    
    private String username;
    private String password;
    private int id;
    private int role;

    /**
     * Get the value of role
     *
     * @return the value of role
     */
    public int getRole() {
        return role;
    }

    /**
     * Set the value of role
     *
     * @param role new value of role
     */
    public void setRole(int role) {
        this.role = role;
    }


    /**
     * Get the value of user_id
     *
     * @return the value of user_id
     */
    public int getId() {
        return id;
    }

    /**
     * Set the value of user_id
     *
     * @param user_id new value of user_id
     */
    public void setId(int id) {
        this.id = id;
    }


    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public User(int id, String username, String password, int role) {
        this.id = id;
        this.role = role;
        this.username = username;
        this.password = password;
    }   
    
    public User(String username, String password, int role) {        
        this.username = username;
        this.password = password;
        this.role = role;
    }   
}
