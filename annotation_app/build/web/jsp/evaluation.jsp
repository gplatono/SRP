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
