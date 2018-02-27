<%-- 
    Document   : login
    Created on : Oct 17, 2016, 1:51:06 PM
    Author     : Георгий Платонов
--%>

<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link rel="stylesheet" type="text/css" href="css/main.css">   
        <!--<script src="js/scripts.js"></script>
        <script type="text/javascript" src="js/jquery-3.1.1.min.js"></script>
        <title>Login</title>
        <script type="text/javascript">
            $(document).ready(function(){	//executed after the page has loaded
                window.alert("TEST!");});
        </script>-->
    </head>
    <body class="body">
        <div class="container">
        <header></header>
        <section class="content">            
            <center><h1>Registration</h1></center> 
            <%if(request.getAttribute("signup_result") != null) { %>
                <p style="font-size: 15px; text-align:center; color: #FF0000;">
                <%=request.getAttribute("signup_result")%>
                 </p>
                 <br>
                 <br>
            <%}%>
            <div class="login">               
            <form method="POST" action="Navigator">
                <input type="hidden" name="page" value="signup">
                <table border="0">
                    <!--<thead1>
                        <tr>
                            <th></th>
                            <th></th>
                        </tr>
                    </thead>-->
                    <tbody>
                        <tr>
                            <td>Username:</td>
                            <td>
                                <input type="text" style="width: 200px;" name="username">
                            </td>
                        </tr>
                        <tr>
                            <td>Password:</td>
                            <td>
                                <input type="password" style="width: 200px;" name="password">
                            </td>
                        </tr>
                        <tr>
                            <td>Confirm Password:</td>
                            <td>
                                <input type="password" style="width: 200px;" name="confirm_password">
                            </td>
                        </tr>
                        <tr>
                            <td></td>
                            <td style="text-align: right;">
                                <input type="submit" name="submit" value="Register">
                            </td>
                        </tr>
                    </tbody>
                </table>
            </form>            
            </div>            
        </section>
        <footer>
            <div class="outer">
            Georgiy Platonov
            <br> <a href="mailto:gplatono@cs.rochester.edu">gplatono@cs.rochester.edu</a>
            <br> University of Rochester
            <br> 2016-2017
            </div>
        </footer>        
        </div>        
    </body>
</html>
