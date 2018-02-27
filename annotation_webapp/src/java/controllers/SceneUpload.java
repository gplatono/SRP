/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package controllers;

import application.JDBCHelper;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.nio.file.Paths;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;
import java.util.stream.Collectors;
import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.annotation.MultipartConfig;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.Part;
import javax.servlet.jsp.PageContext;
import org.apache.commons.fileupload.*;
import org.apache.commons.fileupload.disk.*;
import org.apache.commons.fileupload.servlet.*;
import beans.Scene;
import java.net.URL;
import java.util.ArrayList;


/**
 *
 * @author gplatono
 */
@WebServlet(name = "SceneUpload", urlPatterns = {"/SceneUpload"})
@MultipartConfig
public class SceneUpload extends HttpServlet {

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
        
        byte[] data;        
        Collection<Part> parts = request.getParts();
        ArrayList<Scene> scenes = new ArrayList<Scene>();        
        PrintWriter writer = response.getWriter();
        try {
            for (Part part : parts) {
                String fileName = part.getSubmittedFileName();
                if (fileName == null)
                    continue;
                URL classpath = SceneUpload.class.getClassLoader().getResource("controllers/SceneUpload.class");
                String filePath = /*classpath.getPath().split("WEB-INF")[0] + System.getProperty("user.home") + */"scenes/" + fileName;
                File file = new File("scenes/");
                file.mkdirs();
                InputStream in = part.getInputStream();
                OutputStream out = new FileOutputStream(filePath);
                data = new byte[in.available()];
                in.read(data);
                out.write(data);

                in.close();
                out.close();

                String taskType = request.getParameter("taskType");
                if (!taskType.equals("DESCRIPT") && !taskType.equals("TRUTHJUD"))
                    continue;
                scenes.add(new Scene(filePath, fileName, taskType));
            }
            JDBCHelper.add_scenes(scenes);
            
            writer.print("OK!");
        }
        catch(Exception ex) {
            String msg = ex.getMessage();
            writer.print(msg);
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
