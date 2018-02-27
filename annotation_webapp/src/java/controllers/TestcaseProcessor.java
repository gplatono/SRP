/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package controllers;

import application.JDBCHelper;
import beans.Scene;
import beans.Testcase;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.SQLException;
import java.util.ArrayList;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 *
 * @author gplatono
 */
@WebServlet(name = "TestcaseProcessor", urlPatterns = {"/TestcaseProcessor"})
public class TestcaseProcessor extends HttpServlet {

    /**
     * Processes requests for both HTTP <code>GET</code> and <code>POST</code>
     * methods.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    protected void processRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
            String[] raw_testcases = request.getParameter("testcases").split("###");            
            ArrayList<Testcase> testcases = new ArrayList<Testcase>();
            PrintWriter out = response.getWriter();
            
            try {
                ArrayList<Scene> scenes = JDBCHelper.getScenes();

                for (String raw_testcase : raw_testcases) {
                    String[] fields = raw_testcase.trim().split("\n");
                    fields[0] = fields[0].trim();
                    int scene_id = -1;
                    int taskType = -1;
                    for (Scene scene : scenes) {
                        if (scene.getName().equals(fields[0])) {
                            scene_id = scene.getId();
                            if(scene.getTaskType().equals("DESCRIPT"))
                                taskType = 1;
                            else taskType = 0;
                            break;
                        }
                    }
                    
                    String relation = fields[1].trim();
                    String relatum = fields[2].trim();
                    String referent1 = fields[3].trim();
                    String referent2 = null;
                    if (fields.length > 4)
                        referent2 = fields[4].trim();
                    String query = null;
                    String signature = scene_id + " " + relation + " " + relatum + " " + referent1 + " " + referent2;
                    if(taskType == 0) {
                        if (referent2 == null || referent2.equals(""))
                            query = "Is " + relatum + " " + relation + " " + referent1 + "?";
                        else
                            query = "Is " + relatum + " " + relation + " " + referent1 + " and " + referent2 + "?";
                    }
                    else
                        query = "Where is " + relatum + " in the given scene?";
                    if (scene_id != -1 && taskType != -1) {
                        testcases.add(new Testcase(taskType, scene_id, relation, relatum, referent1, referent2, true, query, signature));
                    }                    
                }
                
                JDBCHelper.add_testcases(testcases);
                out.println("OK!");
            }
            catch(Exception ex) {
                out.println(ex.getMessage());                
            }
    }

    // <editor-fold defaultstate="collapsed" desc="HttpServlet methods. Click on the + sign on the left to edit the code.">
    /**
     * Handles the HTTP <code>GET</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        processRequest(request, response);
    }

    /**
     * Handles the HTTP <code>POST</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        processRequest(request, response);
    }

    /**
     * Returns a short description of the servlet.
     *
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "Short description";
    }// </editor-fold>

}
