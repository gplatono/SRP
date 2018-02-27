<%-- 
    Document   : success
    Created on : Oct 19, 2016, 4:10:03 AM
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
        <div class="container">
            <header>
                Scene Annotation Tool v0.1
            </header>
            <nav>
                <ul id="menu">
                    <li><a href="Navigator?addr=index">Home</a></li>
                    <li><a href="Navigator?addr=annotations">Annotations</a></li>
                    <li><a href="Navigator?addr=evaluation">Evaluations</a></li>
                    <li><a href="Navigator?addr=examples">Examples</a></li>                   
                </ul>
            </nav>

            <section class="content">
                Your response was successfully saved.
                <form action="Navigator">
                    <input type="submit" name="continue" value="true" />
                </form>
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
