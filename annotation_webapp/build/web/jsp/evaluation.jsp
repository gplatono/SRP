<%-- 
    Document   : evaluation
    Created on : Oct 27, 2016, 6:12:47 AM
    Author     : Георгий Платонов
--%>

<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
   <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link rel="stylesheet" type="text/css" href="css/main.css">
        <title>JSP Page</title>
    </head>
    <body class="body">
        <div style='background-color: #FFFFFF;'>
            <c:out value="${request.getAttribute('result')}" />
            <div style="width: 80%; float: left; overflow: hidden;">
                <img class="scene" src="<%=request.getAttribute("imagePath")%>"/>
            </div>            
            <div style="overflow: hidden; padding: 10px; font-size: 15px;">                
                <c:out value="${testcase.testQuery}" escapeXml="False"/>
                    <c:choose>
                        <c:when test="${testcase.queryType == 0}">                            
                            <form action="Navigator" onsubmit="location.href=this.action+'#evaluation'; return false;">
                            <div style="height: 50px; width: 100%;">
                                <div style="overflow: hidden; float: left; width: 50%; border: 2px; padding: 5px;">    
                                    <input type="submit" style="width: 110px; height: 30px;" name="submit_response" value="Yes"/>
                                </div>
                                <div style="overflow: hidden; border: 2px; padding: 5px;">    
                                    <input type="submit" style="width: 110px; height: 30px;" name="submit_response" value="No"/>  
                                </div>
                            </div>
                            </form>
                        </c:when>
                        <c:otherwise>                            
                            <form action="Navigator" onsubmit="location.href=this.action+'#evaluation'; return false;">
                            <div style="width: 100%; border: 2px; padding: 5px; margin: 0 auto;">
                                <textarea name="description" style="resize: none; width: 95%;" rows="20"></textarea>
                                <br>                        
                                <input type="submit" name="submit_response" value="Submit Description" />
                                <br><br>
                                Objects present in the scene:
                                <br><br>
                                <b>
                                <c:forEach var="objectName" items="${testcase.sceneObjects}">                                    
                                    <c:out value="${objectName}"/>
                                    <br>
                                </c:forEach>
                                </b>
                            </div>
                            </form>
                        </c:otherwise>                
                    </c:choose>
            </div> 
        </div>
    </body>
</html>
