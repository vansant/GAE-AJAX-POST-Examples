import json
import os

import ee
import webapp2
import jinja2

import config

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {
            "page_title": "Hello World Example",
            "body_content":"Hello, World"}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


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

class GoogleMapPage(webapp2.RequestHandler):
    def get(self):

        # Authenticate with Earth Engine
        ee.Initialize(config.EE_CREDENTIALS)

        # Get mapid
        mapid = ee.Image('srtm90_v4').getMapId({'min': 0, 'max': 1000})
        template_values = {
            "page_title": "Google Maps Example",
            "body_content":"Google Map Below",
            'mapid': mapid['mapid'],
            'token': mapid['token']
            }
        template = JINJA_ENVIRONMENT.get_template('google_map.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/AJAXFormPage', AJAXFormPage),
    ('/AJAXPostPage', AJAXPostPage),
    ('/AJAXFormJSONPage', AJAXFormJSONPage),
    ('/AJAXPostJSONPage', AJAXPostJSONPage),
    ('/AJAXExamplePage', AJAXExamplePage),
    ('/GoogleMapPage', GoogleMapPage),
], debug=True)