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
                    <li><a href="Navigator?page=exam_1">Examples</a></li>                    
                </ul>
            </nav>
            <section class="content">
                <div style="width: 80%;height: auto;margin: 0 auto;padding: 10px;position: relative;">
                <p>When you click on the "Evaluation" button you will be presented a scene, like this:</p>
                
                <center>
                <img src="img/example.jpg" class="center" width="90%">
                <p>Figure 1.</p>
                </center>
                <!--<p>You will be given an object, say "Cube 8" and asked to describe its location in term of its relation to other objects present in the scene.</p>
                <p>Please follow the following guidelines when writing the description</p>-->
                
                <p>
                    You will be asked to answer "where" questions about the locations
                    of objects in a scene, using natural ways of specifying those locations
                    in relation to other objects, using spatial relations 
                    "above", 
                    "below", 
                    "to the right",
                    "to the left",
                    "in front of",
                    "behind",
                    "near",
                    "at",
                    "in",
                    "over",
                    "under"
                    "between"
                    "on", and
                    "touching".
                    Try to provide a description that will uniquely identify the given object (so that no other object satisfies the same description), while keeping your answer simple and natural.
                </p>
                
                <p>Considering the scene above, here are the kinds of answers we are looking for:</p>

                <ol>
                    <p>
                    <li>Where is Block 1?</li>
                    Answer: to the left of a green block <i>(Note that block 1 is uniquely identified in this way, regardless of which green block you pick)</i>
                    </p>
                    
                    <p><li>Where is Block 5?</li>
                    Answer: on a black block
                    </p>
                    
                    <p>
                    <li>Where is Block 8?</li>
                    Answer: in front of another red block
                    </p>                    
                    
                    <p>
                    <li>Where is Block 7?</li>
                    Answer: between a green block and a red block
                    </p>
                    
                    Also, equally valid response would be:
                    
                    <p>
                    <li>Where is Block 7?</li>
                    Answer: to the left of another red
  block
                    </p>                                        
                </ol>
                
                <p>
                    <b>
                        Be careful when describing the object in question. It is undesirable to describe Block 10 as being "under the blue block", since there are other blocks that satisfy the same criterion.
                    </b>
                </p>

                <p>
                    Note: You are allowed to refer to the TYPE (e.g., table, block, etc.)
                    of other objects and their COLOR (red, black, blue, etc.) Do not refer to other objects by their label. Those labels are given only so that you can understand which object we are asking about.
                </p>

                <p>
                    You can refer to any of the objects in the scene that have labels (using their type, and if necessary, color)
                </p>

                <p>
                    You can use articles "the", "a", "an", or "another" in referring to other objects, whichever is most natural. Do not refer to
      multiple objects (such as "between the blue blocks".) Do not use comparatives or superlatives, such as "rightmost",
      "nearest", "further to the left", etc., just simple prepositional relations.
                </p>
                
                <p>Here is another example: </p>                
                
                <center>
                <img src="img/example2.jpg" class="center" width="90%">
                </center>
                <ol>
                    <p>
                    <li>Where is Banana 1?</li>
                    Answer: near the laptop
                    </p>
                    
                    <p><li>Where is the Rose?</li>
                    Answer: in the vase
                    </p>
                    
                    <p>
                    <li>Where is Banana 2?</li>
                    Answer: behind the other bananas
                    </p>                   
                </ol>
                
                <p>
                    <b>
                        Here, again, be careful not to identify Banana 1 as 
                        being "to the right of laptop", 
                        which might come to mind first, 
                        since all the bananas in the scene satisfy that description.
                        
                        <br>
                        
                        Also, you are allowed to refer to the parts of the "environment" of the scene:
                        the plane, in the case of blocks world and the walls, floor and ceiling in the room world.
                    </b>
                </p>
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
