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
                    <p>When you click on the "Evaluation" button you will be presented a scene, like in the Fig.1 and one of the following two tasks:</p>                
                    <center><img src="img/example.jpg" class="center" width="90%"><p>Figure 1.</p></center>
                
                    <p>I) Instructions for location specification task:</p>

                    <p>You will be presented a scene with multiple objects, labeled with names, and asked to describe the location of a specific target object with a simple phrase.</p>

                    <p>Considering the scene above, here are the kinds of answers we are looking for:</p>
            





                    <ol>
                        <p>
                        <li>Q1: Where is black block 1 in the presented scene?</li>
                        <br>
                        Ans1: to the left of a green block.
                        </p>

                        <p><li>Q2: Where is blue block 4 in the presented scene?</li>
                        <br>
                        Ans2: on a green block.
                        </p>
                        
                        <p><li>Q2: Where is red block 8 in the presented scene?</li>
                        <br>
                        Ans2: in front of another red block.
                        </p>

                        
                    </ol>
                    <p>Note the following points:</p>

                    <ul>
                        <li>As shown in the sample questions and answers, the question may use object numbers to identify the target object, but your answer must not use numbers. For example, Ans1 is NOT allowed to be something like "to the left of green cube 11". However, you can use object types (as in the answers above), and colors, as in Ans1 and Ans2.</li>

                        <li>You can use articles ("the", "a", "an") and words “other” and "another" when referring to the objects, as seen in the answers above. Do not use comparatives or superlatives, such as "rightmost", "nearest", "further to the left", etc. Rely on just the simple prepositional relations below.</li>

                        <li>Your description should uniquely pick out the target object. In other words, make sure no other object satisfies the same description. For example, you cannot describe the block 7 as being behind another red block, as both, block 7 and block 9, satisfy this description.

                            However, if in that scene red block 7 is the ONLY RED BLOCK BEHIND THE BLOCK 8, then the answer is fine -- even if there is also, say, a BLACK BLOCK BEHIND BLOCK 8. So your description can take into account the properties of the target object, as specified in the question (i.e., the type, and color, if given -- but not its number).</li>

                        <li>Avoid complicated descriptions (“Almost behind”, “5 feet above”, etc.); rather, use just one of the relations listed below. Also, if several prepositions are appropriate, pick the one that you feel is the most natural -- how you would describe the location of the target object to someone who is aware of the type (and color, if relevant) of the object, but not *which* object with these properties you have in mind. (Assume that no object numbers are actually visible.)</li>

                        <li>Here are the permissible relations; use EXACTLY ONE in your location specification (if you think that's possible):</li>

                        <ul>    
                            <li>above</li>
                            <li>below</li>
                            <li>to the right</li>
                            <li>to the left</li>
                            <li>in front of</li>
                            <li>behind</li>
                            <li>near</li>
                            <li>at</li>
                            <li>in</li>
                            <li>over</li>
                            <li>under</li>
                            <li>between</li>
                            <li>on</li>
                            <li>touching</li>
                        </ul>

                        <li>Always put your answer on a new line; if you think there two or more equally natural answers, put them on separate lines.</li>
                    </ul>


                    <p>Kinds of scenes that will be presented to you:</p>

                    <p>Each scene contains a relatively small number of objects (<20). The objects are labeled with their names that appear near each object. For each scene, not all the objects will participate in the annotation task. Rather, certain objects will be chosen, to maintain even distribution of questions between different prepositions and to ensure that each object can be identified using only one preposition. Regarding the choice of the objects it can be done either manually, by examining the scene, or by running the model and looking at its predictions and then picking the objects correspondingly.</p>


                    <p>II) Formulation of the truth-judgement task:</p>

                    <p>You will be presented a scene with two or more objects, labeled with names, and asked whether a particular prepositional expression applies to certain objects in that scene. The format of the question will be simply “Is X IN_RELATION_TO Y in the presented scene?” Each object can designated using a combination of color, type and a number, e.g., “Block 4”, “Red Book 2”, “Laptop 1”, etc. Examples:</p>
                    <ul>
                        <li>“Is Block 5 near Block 4?”</li>
                        <li>“Is Red Chair 1 in front of Brown Table 1?”</li>
                        <li>“Is Red Book 3 between Green Book 1 and Laptop 1?”</li>
                    </ul>


                    <p>Scene specifications:</p>

                    <p>Two types of scenes will be present. The first type will only contain two (three for between) objects, which are arguments of the preposition we will be testing. The second type will contain the same argument objects but in a richer environment, i.e., additional objects will be present. That will give us a chance to see how the context affects the usage of prepositions. The distribution of scenes over the set of prepositions is uniform. Also, additional scenes with smaller or bigger perceived frame will be present to test how the frame size affects judgment. The balance between positive and negative cases will be maintained by running our model on the set and taking the same amount of cases when the model predicts “yes” and when it predicts “no”. <b>You can assume that the all the knowledge about the object identities and properties, e.g., color, is available to the system, so you can rely on this in your annotations.</b></p>
                    
                    <b><p>Your progress will be saved. You can sign out and sign back in to resume your annotations at any time.</p></b>                    
                    
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
