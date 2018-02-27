/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package beans;

import java.io.Serializable;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

/**
 *
 * @author gplatono
 */
@Entity
public class Scene implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private int id;
    
    private String path;
    private String name;
    private String taskType;

    public Scene() {
    }

    public Scene(int id, String path) {
        this.id = id;
        this.path = path;
    }    

    public Scene(String path, String name, String taskType) {
        this.id = id;
        this.path = path;
        this.name = name;
        this.taskType = taskType;
    }   

    public Scene(int id, String path, String name, String taskType) {
        this.id = id;
        this.path = path;
        this.name = name;
        this.taskType = taskType;
    }
    
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getTaskType() {
        return taskType;
    }

    public void setTaskType(String taskType) {
        this.taskType = taskType;
    }
    


    @Override
    public boolean equals(Object object) {
        // TODO: Warning - this method won't work in the case the id fields are not set
        if (!(object instanceof Scene)) {
            return false;
        }
        Scene other = (Scene) object;
        if (this.id != other.id) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "beans.Scene[ id=" + id + " ]";
    }
    
}
