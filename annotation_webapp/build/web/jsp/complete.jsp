<%-- 
    Document   : index
    Created on : Oct 12, 2016, 11:37:57 PM
    Author     : Георгий Платонов
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link rel="stylesheet" type="text/css" href="css/main.css">
        <script type="text/javascript" src="js/scripts.js"></script>
        <script type="text/javascript" src="js/jquery-3.1.1.min.js"></script>
        <script>
            $(document).ready(function(){	//executed after the page has loaded
                checkURL();                     //check if the URL has a reference to a page and load it
                $('ul li a').click(function (e){	//traverse through all our navigation links..
                    checkURL(this.hash);	//.. and assign them a new onclick event, using their own hash as a parameter (#page1 for example)
                });
                setInterval("checkURL()",250);	//check for a change in the URL every 250 ms to detect if the history buttons have been used
            });           
        </script>
        <title>SRP Annotator tool</title>
    </head>
    <body class="body">
        <div class="container">
            <header>
                Scene Annotation Tool v0.1
            </header>
            <nav>
                <ul class="menu">
                    <li><a href="Navigator?page=index_1">Home</a></li>
                    <!--<li><a href="#annotations">Annotations</a></li>-->
                    <li><a href="Navigator?page=eval">Evaluation</a></li>
                    <li><a href="Navigator?page=exam_2">Examples</a></li>                      
                      <li><a href="Navigator?page=logout">Logout</a></li> 
                </ul>
            </nav>
            <section class="content">
                <div style="width: 80%;height: auto;margin: 0 auto;padding: 10px;position: relative;">
                <p>You answered all the questions, there are no more tests left. Thank you for participating!</p>
               
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
