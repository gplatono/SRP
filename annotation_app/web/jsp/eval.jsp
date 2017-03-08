<%-- 
    Document   : index
    Created on : Oct 12, 2016, 11:37:57 PM
    Author     : Георгий Платонов
--%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link rel="stylesheet" type="text/css" href="css/main.css">
        <script type="text/javascript" src="js/scripts.js"></script>
        <script type="text/javascript" src="js/jquery-3.1.1.min.js"></script>
        <!--<script>
            $(document).ready(function(){	//executed after the page has loaded
                checkURL();                     //check if the URL has a reference to a page and load it
                $('ul li a').click(function (e){	//traverse through all our navigation links..
                    checkURL(this.hash);	//.. and assign them a new onclick event, using their own hash as a parameter (#page1 for example)
                });
                setInterval("checkURL()",250);	//check for a change in the URL every 250 ms to detect if the history buttons have been used
            });            
        </script>-->
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
                    <li><a href="Navigator?page=exam_1">Examples</a></li>                   
                </ul>
            </nav>
            <section class="content">                
                <%if(request.getAttribute("result") != null) { %>
                <p style="font-size: 15px;">
                <%=request.getAttribute("result")%>
                 </p>
            <%}%>
               
            <div style='background-color: #FFFFFF;'>
            <div style="width: 80%; float: left; overflow: hidden;">
                <img class="scene" src="${testInstance.imagePath}"/>
            </div>            
            <div style="overflow: hidden; padding: 10px; font-size: 15px;">                
                <c:out value="${testInstance.query}" escapeXml="False"/>
                    <c:choose>
                        <c:when test="${testInstance.testcase.queryType == 1}">                            
                            <form action="Navigator?page=eval">
                            <div style="height: 50px; width: 100%;">
                                <div style="overflow: hidden; float: left; width: 40%; border: 2px; padding: 5px;">    
                                    <input type="submit" style="width: 100%; height: 30px;" name="submit_response" value="Yes"/>
                                </div>
                                <div style="overflow: hidden; width: 40%; border: 2px; padding: 5px;">    
                                    <input type="submit" style="width: 100%; height: 30px;" name="submit_response" value="No"/>  
                                </div>
                            </div>
                            </form>
                        </c:when>
                        <c:otherwise>                            
                            <form action="Navigator?page=eval">
                            <div style="width: 100%; border: 2px; padding: 5px; margin: 0 auto;">
                                <textarea name="description" style="resize: none; width: 98%;" rows="20"></textarea>
                                <br>   
                                <input style="float: right; width: 50%;" type="submit" name="submit_response" value="Submit"/>
                                <br><br>
                                <!--Objects present in the scene:-->
                                <br><br>
                                <b>
                                <%--<c:forEach var="objectName" items="${testcase.sceneObjects}">                                    
                                    <c:out value="${objectName}"/>
                                    <br>
                                </c:forEach>--%>
                                </b>
                            </div>
                            </form>
                        </c:otherwise>                
                    </c:choose>
            </div> 
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
