package beans;

import beans.Testcase;
import javax.annotation.Generated;
import javax.persistence.metamodel.SingularAttribute;
import javax.persistence.metamodel.StaticMetamodel;

@Generated(value="EclipseLink-2.5.2.v20140319-rNA", date="2017-10-13T14:40:04")
@StaticMetamodel(TestInstance.class)
public class TestInstance_ { 

    public static volatile SingularAttribute<TestInstance, String> scenePath;
    public static volatile SingularAttribute<TestInstance, String> imagePath;
    public static volatile SingularAttribute<TestInstance, String> response;
    public static volatile SingularAttribute<TestInstance, String> query;
    public static volatile SingularAttribute<TestInstance, Integer> userID;
    public static volatile SingularAttribute<TestInstance, Testcase> testcase;

}