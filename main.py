import json
import os

import ee
import webapp2
import jinja2

import config

import time

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

        time.sleep(5)
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
        <input type="submit" id="cancel_button"></input>
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
				    //alert( "error" );
				  })
            

                $( "#cancel_button" ).click(function() {
                    jqxhr.abort()
                    console.log( "Handler for .click() called. Ignoring AJAX call" );
                });
 

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

class GetMapId(webapp2.RequestHandler):
    def post(self):
        """ Returns a mapid and a token"""
        # Authenticate with Earth Engine
        ee.Initialize(config.EE_CREDENTIALS)

        # set response header to JSON
        self.response.headers['Content-Type'] = 'application/json'  

        image = self.request.get('image')
        minimum = self.request.get('minimum')
        maximum = self.request.get('maximum')


        mapid = ee.Image(str(image)).getMapId({'min': int(minimum), 'max': int(maximum)})
        #mapid = ee.Image('srtm90_v4').getMapId({'min': 0, 'max': 1000})
        # form object to get converted to JSON
        object_for_JSON = {'mapid': mapid['mapid'],
                            'token': mapid['token']
                        }
        response = json.dumps(object_for_JSON)
        self.response.write(response)

class GetPixelData(webapp2.RequestHandler):
    def post(self):
        """ Returns a mapid and a token"""
        # Authenticate with Earth Engine
        ee.Initialize(config.EE_CREDENTIALS)

        # set response header to JSON
        self.response.headers['Content-Type'] = 'text/html'  

        image = self.request.get('image')
        minimum = self.request.get('minimum')
        maximum = self.request.get('maximum')
        latitude = self.request.get('latitude')
        longitude = self.request.get('longitude')

        print "lat", latitude
        print "lon", longitude

        pointGeometry = ee.Geometry.Point(float(longitude), float(latitude))

        #pixel_info = float(ee.Image(image).getRegion(pointGeometry,1).getInfo()[1][4])

        image = ee.Image(str(image))
        pixel_data = image.reduceRegion(ee.Reducer.first(),pointGeometry,1).getInfo()
        self.response.write(pixel_data)


class EEAJAXExamplePage(webapp2.RequestHandler):
    def get(self):
        # set response header to JSON
        self.response.headers['Content-Type'] = 'text/html'  

        response = """

        <!doctype html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Demo</title>
            <style type="text/css">
                html, body, #map-canvas { height: 500px; margin: 0; padding: 0;}
            </style>
            <script type="text/javascript"
              src="https://maps.googleapis.com/maps/api/js?">
            </script>
        </head>
        <body>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
            <script>
         
            $( document ).ready(function() {
                // When the button is clicked
                $("#form_button").click(function(event){

                    // Prevent the form from submitting
                    event.preventDefault();
                    //alert("clicked the button");

                    // Get the form variables
                    var image = $("#image").val();
                    var maximum = $("#maximum").val();
                    var minimum = $("#minimum").val();

                    // Make the AJAX request
                    var jqxhr = $.ajax({
                        url: "/GetMapId",
                        method: "POST",
                        data: "image=" + image +"&minimum=" + minimum + "&maximum=" + maximum,
                        //data: {image:"John", last_name:"Doe"},
                        //success:function(data) { alert(data); },
                    })
                    .done(function(data) {
                        var mapId = data.mapid;
                        var token = data.token;

                        // Set mapid and token from AJAX request
                        $("#token").val(token);
                        $("#mapId").val(mapId);

                        //console.log(data);
                        //alert( "success" );
                        //alert("button" + mapid, token);





        var eeMapOptions = {
            getTileUrl: function(tile, zoom) {
              var baseUrl = 'https://earthengine.googleapis.com/map';
              var url = [baseUrl, mapId, zoom, tile.x, tile.y].join('/');
              url += '?token=' + token;
              return url;
            },
            tileSize: new google.maps.Size(256, 256)
          };

          // Create the map type.
          var mapType = new google.maps.ImageMapType(eeMapOptions);

          var myLatLng = new google.maps.LatLng(-34.397, 150.644);
          var mapOptions = {
            center: myLatLng,
            zoom: 8,
            maxZoom: 10,
            streetViewControl: false
          };

          // Create the base Google Map.
          var map = new google.maps.Map(
              document.getElementById('map'), mapOptions);

          // Add the EE layer to the map.
          map.overlayMapTypes.push(mapType);


          google.maps.event.addListener(map, 'click', function(event) {
              //map.setZoom(8);
              //map.setCenter(marker.getPosition());
              //alert(event.latLng);
              var latitude = event.latLng.lat();
              var longitude = event.latLng.lng();
              //alert(latitude);


                // Make the AJAX request when clicking on Google Map
                    var jqxhr = $.ajax({
                        url: "/GetPixelData",
                        method: "POST",
                        data: "image=" + image +"&minimum=" + minimum + "&maximum=" + maximum + "&latitude=" + latitude + "&longitude=" + longitude,
                        //success:function(data) { alert(data); },
                    })
                    .done(function(data) {
                        //var mapId = data.mapid;
                        //var token = data.token;

                        // Set mapid and token from AJAX request
                        //$("#token").val(token);
                        //$("#mapId").val(mapId);

                        //console.log(data);
                        //alert( data );
                        //alert("button" + mapid, token);
                        $("#pixel_data").text(data);

                        })
                    .fail(function(){
                        alert('fails');
                    })


          });



                    }) // End Success AJAX from Button Call
                    .fail(function() {
                        alert( "error" );
                    }) // End Error from AJAX button Call


                }); //End form button click

            }); // End document ready
         
            </script>
            <form>
                image<input type="text" name="image" id="image" value="srtm90_v4"></input>
                minimim<input type="text" name="minimim" id="minimum" value="0"></input>
                maximum<input type="text" name="maximum" id="maximum" value="1000"></input>
                token<input type="text" name="token" id="token" value="token will update here" readonly></input>
                mapId<input type="text" name="mapId" id="mapId" value="mapId will update here" readonly></input>
                <input type="submit" id="form_button"></input>
            </form>

            <!-- The element into which we render the Google Map. -->
            <div id="map" style="width: 640px; height: 480px;"></div>
            <div>Pixel data updates below on map click:</div>
            <div id="pixel_data"></div>
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
    ('/GoogleMapPage', GoogleMapPage),
    ('/GetMapId', GetMapId),
    ('/GetPixelData', GetPixelData),
    ('/EEAJAXExamplePage', EEAJAXExamplePage),
], debug=True)