Contains the user interface logic for interacting with the air alarm prediction system via a web browser:

  -**'index.html'** : It provides a form where users can select a region and prediction mode (new or past), and view the hourly forecast as colored indicators:
    Red dot = air alarm predicted
    Green dot = no alarm predicted
  The template is intended to be rendered by a Flask backend and uses dynamic region and forecast data.

  -**'update_html.ipynb'** :  used for editing or dynamically updating index.html.
