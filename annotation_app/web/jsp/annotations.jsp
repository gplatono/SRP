<%-- 
    Document   : annotations
    Created on : Oct 19, 2016, 4:07:52 AM
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
                <img class="scene" src="scenes/1.png" />
                <br>
                <form action="SubmissionHandler">
                    <!--Enter the referent object name: <br>
                    <input width=100% type="text" rows="1" /> <br>
                    Select the relation: <br>
                    <select>
                        <option value="sp_above">Above</option>
                        <option value="sp_below">Below</option>
                        <option value="sp_left">To the left of </option>
                        <option value="sp_right">To the right of</option>
                        <option value="sp_infrontof">In front of</option>
                        <option value="sp_behind">Behind</option>
                        <option value="sp_near">Near</option>
                        <option value="sp_at">At</option>
                        <option value="sp_over">Over</option>
                        <option value="sp_under">Under</option>
                        <option value="sp_in">In</option>
                        <option value="sp_on">On</option>
                        <option value="sp_around">Around</option>                        
                    </select>           
                    <br>
                    Enter the names of all the objects for which the selected relation holds, with respect to the selected referent (separate the names by commas or spaces): 
                    <br>  
                    <input width=100% type="text" rows="3" />
                    <br>
                    <br>-->
                    <div style="text-align: right; width: 70%; border: 2px; padding: 5px; margin: 0 auto;">
                    <textarea style="width: 100%;" name="description" rows="10"></textarea>
                    <br>                        
                        <input type="submit" name="submit_desc" value="Submit Description" />
                    </div>
                </form>
    </body>
</html>
