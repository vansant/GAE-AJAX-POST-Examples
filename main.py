import webapp2
import json

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

class AJAXFormPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        html_form = """
			<form action="/AJAXPostPage" method="Post">
				<input type="text" name="name"></input>
			</form>
		"""
        self.response.write(html_form)

class AJAXPostPage(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        name = self.request.get('name')
        self.response.write('you posted %s to this page' % name)

class AJAXFormJSONPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        html_form = """
			<form action="/AJAXPostJSONPage" method="Post">
				<input type="text" name="first_name"></input>
				<input type="text" name="last_name"></input>
				<input type="submit"></input>
			</form>
		"""
        self.response.write(html_form)

class AJAXPostJSONPage(webapp2.RequestHandler):
    def post(self):
    	# set response header to JSON
        self.response.headers['Content-Type'] = 'application/json'  

        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')

        # form object to get converted to JSON
        object_for_JSON = {"person":
        					[
        						{"firstName": first_name,
        						"lastName":last_name
        						},
        					]
        				}
        response = json.dumps(object_for_JSON)
        self.response.write(response)

class AJAXExamplePage(webapp2.RequestHandler):
    def get(self):
    	# set response header to JSON
        self.response.headers['Content-Type'] = 'text/html'  

        response = """

        <!doctype html>
		<html>
		<head>
		    <meta charset="utf-8">
		    <title>Demo</title>
		</head>
		<body>
		    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
		    <script>
		 
		    $( document ).ready(function() {
			 
			    var jqxhr = $.ajax({
				    url: "/AJAXPostJSONPage",
				    method: "POST",
				    data: "first_name=howdy&last_name=partner",
				    //data: {first_name:"John", last_name:"Doe"},
				    //success:function(data) { alert(data); },
  				})
				  .done(function(data) {
				  	console.log(data);
				    alert( "success" );
				  })
				  .fail(function() {
				    alert( "error" );
				  })

			});
		 
		    </script>
		</body>
		</html>

        """

        self.response.write(response)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/AJAXFormPage', AJAXFormPage),
    ('/AJAXPostPage', AJAXPostPage),
    ('/AJAXFormJSONPage', AJAXFormJSONPage),
    ('/AJAXPostJSONPage', AJAXPostJSONPage),
    ('/AJAXExamplePage', AJAXExamplePage),
], debug=True)