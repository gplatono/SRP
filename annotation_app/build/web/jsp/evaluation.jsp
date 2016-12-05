<%-- 
    Document   : evaluation
    Created on : Oct 27, 2016, 6:12:47 AM
    Author     : Георгий Платонов
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
   <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link rel="stylesheet" type="text/css" href="css/main.css">
        <title>JSP Page</title>
    </head>
    <body class="body">
        <br>
        <img class="scene" src="scenes/screen.jpg" />
        <br>
        On the given picture, is the <b>red cube on top of the purple cube</b>?
        <br>
        <form action="SubmissionHandler">
            <div style="height: 50px; width: 100%;">
                <div style="float: left; width: 50px; border: 2px; padding: 5px;">    
                    <input type="submit" style="width: 50px;" name="yes" value="Yes"/>
                </div>
                <div style="float: left; width: 50px; border: 2px; padding: 5px;">    
                    <input type="submit" style="width: 50px;" name="no" value="No"/>  
                </div>
            </div>
        </form>           
    </body>
</html>
