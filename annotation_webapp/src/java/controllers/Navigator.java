/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package controllers;

import application.JDBCHelper;
import beans.Testcase;
import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import application.TestGenerator;
import beans.Scene;
import beans.TestInstance;
import beans.User;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import application.UserSecurityManager;

/**
 *
 * @author Георгий Платонов
 */
public class Navigator extends HttpServlet {

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
        
        String page = request.getParameter("page");
        if (page == null)
            if(request.getSession().getAttribute("user") != null)
                page = "index_1";
            else page = "login";
                  
            try {
                if(request.getSession().getAttribute("SecurityManager") == null)
                    request.getSession().setAttribute("SecurityManager", new UserSecurityManager());
                UserSecurityManager manager = (UserSecurityManager)request.getSession().getAttribute("SecurityManager");
                //String url = request.getServletPath();
                if(page.equals("login")) {
                    String username = request.getParameter("username");
                    String password = request.getParameter("password");
                    if(username != null) {
                        User user = manager.login(username, password);
                        if (user != null)
                            request.getSession().setAttribute("user", user);
                        page = "index_1";
                    }                    
                }
                
                
                if(request.getSession().getAttribute("user") != null || request.getParameter("page").equals("signup")) {
                
                if(page.equals("signup")){
                    String username = request.getParameter("username");
                    String password = request.getParameter("password");
                    String confirm = request.getParameter("confirm_password");                     
                    if (username != null && password != null && confirm != null && password.equals(confirm)) {
                        String result = manager.SignUp(username, password);
                        if(result.equals("OK"))
                            page = "login";
                        else if (result.equals("USERNAME_EXISTS")) {
                            page = "signup";
                            request.setAttribute("signup_result", "The username you entered is already taken");
                        }
                    }
                }
                
                if(page.equals("DUMP")) {
                    new JDBCHelper().dump_responses("dump");                
                }
                
                if(page.equals("send_response")) {
                    if(request.getParameter("skip") == null) {
                    TestInstance testInstance = (TestInstance)request.getSession().getAttribute("testInstance");                                    
                    
                    if(testInstance != null) {

                        if(request.getParameter("description") != null)
                            testInstance.setResponse(request.getParameter("description"));
                        else
                            testInstance.setResponse(request.getParameter("submit_response").toUpperCase());
                        request.getSession().setAttribute("result", "Thank you. Your last response - \'" + testInstance.getResponse() + "\' - has been saved...");                
                        JDBCHelper.saveResponse(testInstance);
                        request.getSession().removeAttribute("testInstance");                    
                    }
                    else {
                        request.getSession().removeAttribute("result");
                    }
                    response.sendRedirect(request.getContextPath() +"/Navigator?page=eval&result=" + "Thank you. Your last response - \'" + testInstance.getResponse() + "\' - has been saved...");
                    }
                    else
                        response.sendRedirect(request.getContextPath() +"/Navigator?page=eval");
                    return;                    
                }
                else {
                    request.getSession().removeAttribute("result");
                }
                if(page.equals("eval")) {                    
                    TestInstance testInstance = TestGenerator.generate((User)request.getSession().getAttribute("user"));
                    request.getSession().setAttribute("testInstance", testInstance);
                    if (testInstance == null) 
                        page = "complete";
                }
                if(page.equals("SCNUPLD"))
                    page = "scn_upload";
                if(page.equals("logout")) {
                    request.getSession().setAttribute("user", null);
                    page = "login";
                }
                }
                else page = "login";                
                request.getRequestDispatcher("/jsp/" + page + ".jsp").forward(request, response);
            }
            catch(Exception ex) {                
                response.getWriter().println(ex.getMessage());
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
