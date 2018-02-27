<%-- 
    Document   : scn_upload
    Created on : Jul 3, 2017, 3:18:05 PM
    Author     : gplatono
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>JSP Page</title>
    </head>
    <body>
        <form action="SceneUpload" method="POST" enctype="multipart/form-data">
            <input type = "file" name = "file" size = "50" multiple="true" />
            <br />
            
            <input type = "radio" name = "taskType" value="DESCRIPT" /> Description task           
            <br />
            
            <input type = "radio" name = "taskType" value="TRUTHJUD" /> Truth-judgment task
            <br />
            
            <input type = "submit" value = "Upload" />
        </form>
    </body>
</html>
