<%-- 
    Document   : login
    Created on : Oct 17, 2016, 1:51:06 PM
    Author     : Георгий Платонов
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link rel="stylesheet" type="text/css" href="css/main.css">        
        <title>Login</title>
    </head>
    <body class="body">
        <div class="container">
        <header></header>
        <section class="content">            
            <center><h1>Login</h1></center>
            
            <div class="login">
            <form method="POST" action="LoginManager">
                <table border="0">
                    <!--<thead1>
                        <tr>
                            <th></th>
                            <th></th>
                        </tr>
                    </thead>-->
                    <tbody>
                        <tr>
                            <td>Login:</td>
                            <td>
                                <input type="text" style="width: 200px;" name="login_val">
                            </td>
                        </tr>
                        <tr>
                            <td>Password:</td>
                            <td>
                                <input type="password" style="width: 200px;" name="pass_val">
                            </td>
                        </tr>
                        <tr>
                            <td></td>
                            <td style="text-align: right;">
                                <input type="submit" name="submit" value="Sign in">
                            </td>
                        </tr>
                    </tbody>
                </table></form>            
            </div>            
        </section>
        <footer>
            <div class="outer">
            Georgiy Platonov
            <br> <a href="mailto:gplatono@cs.rochester.edu">gplatono@cs.rochester.edu</a>
            <br> University of Rochester
            <br> 2016
            </div>
        </footer>        
        </div>        
    </body>
</html>
