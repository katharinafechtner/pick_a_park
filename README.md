# Pick a park - CS50x Final Project
## Video Demo:  [YouTube video](https://youtu.be/eF5O-l2-Rk0)

## Description:
This website allows the user to analyze a map area of his or her choice to find green areas. The original idea is to provide a way of finding potentially nice recreational areas in a city to train, meet friends, relax, etc.
What the website does in short: The user enters the index page where an embedded searchable dynamic map is displayed. The user can then focus on a map frame and analyze this area via button-click to mark potential green spaces. In addition, the color distribution of the chosen map frame is analyzed with kmeans clustering. The result is a pie chart displayed on the website.
  
## General setup
Visual studio code
- Windows OS
- Flask framework
- Languages: python (v3.8), HTML, CSS, Javascript
  
## Files
- Python scripts:
  - app.py
  - screenshot.py
  - colorfilter.py
  - kmeans.py
  
- /static
  - /imgs
    - sample.jpg
    - sample2.jpg
    - sample3.jpg
    - sandclock.png
  - /screenshots
  - body.css
  - map.css
  
- /templates
  - layout.html
  - index.html
  - analysis.html

### app.py
Setup/configuration for flask application

Global variables:
- API key - user must create ./config folder and config file of this format:
  ```
  [KEYS]
  api_key = enter_your_key_without_quotes_here
  ```
- Url base (access to google map API)

Includes 2 different routes
- index page
  - clears folder with images from earlier sessions 
  - queries Google's Embed Map API
  - renders html template for index page with query details
- analysis page
  - includes function calls that are activated upon click
    - screenshot.py
    - colorfilter.py
    - kmeans.py

#### app.py - Design choices and possible improvements
There were some probems with caching so I defined this:
```
@app.after_request
...
```
Chrome still continued caching pictures somehow. Clearing the screenshot directory before each analysis did the trick but I am not sure why.
```
files = glob.glob(directory + "/*")
  for f in files:
    os.remove(f)
```

### screenshot.py
This file is called via buttonclick from the index page by the user, takes a screenshot (pyautogui) of the chosen map frame and saves it to the screenshot directory. It requires a pathname as input so that the image can later be processed.
#### screenshot.py - Design choices and possible improvements
The screenshot is taken based on the image "relator_for_screenshot.jpg" saved in the /static directory.
This is a very hacky solution.
I had to set the confidence intervall lower to make it recognize the pixels, but it still does not work in every case (for example when I work on a different screen).
Ideally, I would both query the embedded map and the static map from the google API service, so that I can automatically save an image without text, search field, etc. with the relevant metadata (size, zoom, etc.). This would require me to aquire quota $$$ though.
That way, it would also be possible to adjust the blob detector in "colorfilter.py" to select the relevant blob areas based on the chosen zoom of the current map.
Now, it will only relate the filter to the pixels, rather than squared meters/feet of park.

### colorfilter.py
This file is called via buttonclick from the index page by the user and performs a color analysis of the screenshot image which is then saved to the screenshot directory.
#### colorfilter.py - Design choices and possible improvements
The color filter lower and upper limits are set manually and work decently well for the default colors google uses for their default map.
Ideally, the analysis would use satellite pictures, compare this somehow to parks that are likely already identified by google maps, and give some kind of confidence index to how likely it atually is a park (and not just a green roof or similar).
Another feature I would have liked to implement with more time and quota $$$ was to query the places displayed within the map ("parks" or similar) and display a list of possible matches within the map on the website.

### kmeans.py
This file is called via buttonclick from the index page by the user and performs a kmeans clustering analysis of the screenshot image which is then saved to the screenshot directory.
#### kmeans.py - Design choices and possible improvements
This function has no real purpose in this context, but was originally considered to use on the map with a grid, to calculate percentages of colors and deduct some kind of index for how green an area is. This can then be translated into liveability of an area.

