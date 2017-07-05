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
import beans.TestInstance;
import java.net.URL;

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
        response.setContentType("text/html;charset=UTF-8");
        //try (PrintWriter out = response.getWriter()) {
            /* TODO output your page here. You may use following sample code. */
            //out.println(request.getParameter("page"));
            /*out.println("<html>");
            out.println("<head>");
            out.println("<title>Servlet Navigator</title>");            
            out.println("</head>");
            out.println("<body>");
            out.println("<h1>Servlet Navigator at " + request.getContextPath() + "</h1>");
            out.println("</body>");
            out.println("</html>");*/
            //return;
        //}
        //if(request.getParameter("login_val") != null)
        //if(request.getParameter("login_val") != null && request.getParameter("login_val").equals("admin") &&
            //request.getParameter("pass_val") != null && request.getParameter("pass_val").equals("admin"))
            //request.getRequestDispatcher("jsp/index.jsp").forward(request, response);            
            String address = request.getParameter("page");
            
            
            if(address.equals("DUMP")) {
                try {
                new JDBCHelper().dump_responses("dump");
                }
                catch(Exception ex) {
                    response.getWriter().println(ex.getMessage());
                }
                return;
            }
            if (address == null)
                address = "index";
            if(request.getParameter("submit_response") != null) {
                //PrintWriter out = response.getWriter();
                //out.println("ok");                
                TestInstance testInstance = (TestInstance)request.getSession().getAttribute("testInstance");
                if(request.getParameter("description") != null)
                    testInstance.setResponse(request.getParameter("description"));
                else
                    testInstance.setResponse(request.getParameter("submit_response"));
                request.setAttribute("result", "Thank you. Your last response - \'" + testInstance.getResponse() + "\' - has been saved...");                
                try {
                JDBCHelper.saveResponse(testInstance);
                }
                catch (Exception ex) {
                   
                }
                
                address = "eval";
                //return;
            }
            else {
                request.setAttribute("result", null);
            }
            if(address.equals("eval")) {
                URL classpath = Navigator.class.getClassLoader().getResource("controllers/Navigator.class");
                String appPath = classpath.getPath().split("WEB-INF")[0];                
                //String datasetPath = System.getProperty("user.home") + File.separator + "scenes";
                TestInstance testInstance = TestGenerator.generate(appPath);
                testInstance.setUserID(1);
                request.getSession().setAttribute("testInstance", testInstance);
                //request.setAttribute("imagePath", request.getContextPath() + testcase.getImagePath());//"scenes/" + (testcase.getSceneID() + 1) + "/" + "scene.png");                
                //return;
            }            
            if(address.equals("SCNUPLD"))
                address = "scn_upload";
            request.getRequestDispatcher("/jsp/" + address + ".jsp").forward(request, response);
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
