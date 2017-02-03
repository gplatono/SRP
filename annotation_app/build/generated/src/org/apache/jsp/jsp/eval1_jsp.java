package org.apache.jsp.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;

public final class eval1_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent {

  private static final JspFactory _jspxFactory = JspFactory.getDefaultFactory();

  private static java.util.List<String> _jspx_dependants;

  private org.glassfish.jsp.api.ResourceInjector _jspx_resourceInjector;

  public java.util.List<String> getDependants() {
    return _jspx_dependants;
  }

  public void _jspService(HttpServletRequest request, HttpServletResponse response)
        throws java.io.IOException, ServletException {

    PageContext pageContext = null;
    HttpSession session = null;
    ServletContext application = null;
    ServletConfig config = null;
    JspWriter out = null;
    Object page = this;
    JspWriter _jspx_out = null;
    PageContext _jspx_page_context = null;

    try {
      response.setContentType("text/html;charset=UTF-8");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;
      _jspx_resourceInjector = (org.glassfish.jsp.api.ResourceInjector) application.getAttribute("com.sun.appserv.jsp.resource.injector");

      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("<!DOCTYPE html>\n");
      out.write("<html>\n");
      out.write("    <head>\n");
      out.write("        <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\n");
      out.write("        <link rel=\"stylesheet\" type=\"text/css\" href=\"css/main.css\">        \n");
      out.write("        <title>SRP Annotator tool</title>\n");
      out.write("    </head>\n");
      out.write("    <body class=\"body\">\n");
      out.write("        <div class=\"container\">\n");
      out.write("            <header>\n");
      out.write("                Scene Annotation Tool v0.1\n");
      out.write("            </header>\n");
      out.write("            <nav>\n");
      out.write("                <ul class=\"menu\">\n");
      out.write("                    <li><a href=\"/Navigator?page=description\">Home</a></li>\n");
      out.write("                    <li><a href=\"/Navigator?page=annotations\">Annotations</a></li>\n");
      out.write("                    <li><a href=\"/Navigator?page=eval1\">Evaluations</a></li>\n");
      out.write("                    <li><a href=\"/Navigator?page=examples\">Examples</a></li>                    \n");
      out.write("                </ul>\n");
      out.write("                \n");
      out.write("            </nav>\n");
      out.write("            <section id=\"Content\" class=\"content\" style=\"vertical-align: middle;\">\n");
      out.write("             <br>\n");
      out.write("        <img class=\"scene\" src=\"scenes/screen.jpg\" />\n");
      out.write("        <br>\n");
      out.write("        On the given picture, is the <b>red cube on top of the purple cube</b>?\n");
      out.write("        <br>\n");
      out.write("        <form action=\"SubmissionHandler\">\n");
      out.write("            <div style=\"height: 50px; width: 100%;\">\n");
      out.write("                <div style=\"float: left; width: 50px; border: 2px; padding: 5px;\">    \n");
      out.write("                    <input type=\"submit\" style=\"width: 50px;\" name=\"yes\" value=\"Yes\"/>\n");
      out.write("                </div>\n");
      out.write("                <div style=\"float: left; width: 50px; border: 2px; padding: 5px;\">    \n");
      out.write("                    <input type=\"submit\" style=\"width: 50px;\" name=\"no\" value=\"No\"/>  \n");
      out.write("                </div>\n");
      out.write("            </div>\n");
      out.write("        </form>             \n");
      out.write("            </section>        \n");
      out.write("            <footer>\n");
      out.write("                <div class=\"outer\">\n");
      out.write("                Georgiy Platonov\n");
      out.write("                <br> <a href=\"mailto:gplatono@cs.rochester.edu\">gplatono@cs.rochester.edu</a>\n");
      out.write("                <br> University of Rochester\n");
      out.write("                <br> 2016\n");
      out.write("                </div>\n");
      out.write("            </footer>        \n");
      out.write("        </div>\n");
      out.write("    </body>\n");
      out.write("</html>\n");
    } catch (Throwable t) {
      if (!(t instanceof SkipPageException)){
        out = _jspx_out;
        if (out != null && out.getBufferSize() != 0)
          out.clearBuffer();
        if (_jspx_page_context != null) _jspx_page_context.handlePageException(t);
        else throw new ServletException(t);
      }
    } finally {
      _jspxFactory.releasePageContext(_jspx_page_context);
    }
  }
}
