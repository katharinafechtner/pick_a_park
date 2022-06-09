import os
import glob
import configparser
from flask import Flask, render_template, request
from screenshot import screenshot
from colorfilter import colorfilter
from kmeans import Kmeans

''' Flask application - Pick a Park
This website lets the user choose a map frame via google's dynamic embedded map API.
Upon button-click, a screenshot is taken that is then analyzed:
- colorfilter
- blob detector
- kmeans color distribution
The analysis results are marked as a map image including detected green areas
and a kmeans distribution pie chart.
The analysis results are displayed on the website and saved to a file.'''

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# url variable
#url_base = "https://maps.googleapis.com/maps/api/staticmap?"
#url_base = "https://www.google.com/maps/embed/v1/place?"
url_base = "https://www.google.com/maps/embed/v1/search?"

# Screenshot path
dirname = os.path.dirname(__file__)

# Retrieve API key from config file
cfg = configparser.ConfigParser()
cfg.read(dirname + '\\.config\\user.cfg')
api_key = cfg.get('KEYS', 'api_key')


# No caching at all for API endpoints.
@app.after_request
def add_header(response):

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


''' Route to index page '''
@app.route("/", methods=["GET", "POST"])
def index():

  if request.method == 'POST':

    directory = dirname + "\\static\\screenshots"

    files = glob.glob(directory + "/*")
    for f in files:
        os.remove(f)

    query = request.form.get("query")

    return (render_template("index.html", api_key=api_key, query=query))
    #return render_template("index.html")
  
  else:
    return (render_template("index.html", api_key=api_key, query="Boston"))
    #return render_template("index.html")


''' Route to analysis page '''
@app.route("/analysis", methods=["GET", "POST"])
def analysis():

  if request.method == 'POST':

    screenshot(dirname)
    colorfilter(dirname)
    Kmeans(dirname)

    return render_template("analysis.html")
  
  else:
    return (render_template("index.html", api_key=api_key, query="Boston"))


if __name__ == '__main__':
  #print ("Executed when invoked directly")
  app.run()
#else:
    #print ("Executed when imported")