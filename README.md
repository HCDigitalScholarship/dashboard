# dashboard
### Research dashboard for Indigeneity/Urban Ecology courses

The research dashboard is built with [Plotly Dash](https://dash.plot.ly/), which is a handy Python framework for building data visualizations.
It also utilizes [django-plotly-dash](https://pypi.org/project/django-plotly-dash/) to embed the Plotly Dash app(s) into the Django framework, 
In order to implement other features in the future, read our [cookbook entry](https://github.com/HCDigitalScholarship/ds-cookbook/blob/master/django-plotly-dash/django-plotly-dash.md) to see how to adapt a dashboard app to Django.

**Notes:** The package `django-plotly-dash` requires Django>=2.0, Python>=3.5, Dash<=0.38.0 (they have not developed the package for greater versions as of May 2019).

### Skeleton of this project
```
dashboard/Django_Dash
|--- Django_Dash/ ## regular Django project directory which contains setting.py and wsgi.py
|
|--- Django_Dash_app/
|   |
|   |--- dashplotly/ ## the directory for Plotly Dash app(s)
|   |    |
|   |    |--- csv/ ## saving dataset
|   |    |
|   |    |--- dashboard_app.py ## the main program
|   |    |
|   |    |--- uniqueYearCalculator.py
|   | 
|   |--- migrations/
|   | 
|   |--- other files for regular Django apps
|
|--- static/css/
|
|--- templates/
|
|--- manage.py ## run the project as regular Django apps
|
|--- requirement.txt

```
### Runserver locally
Technically, this project is still a Django app. To run it, go to `dashboard/Django_Dash/` directory and do:
```
python manage.py runserver
```

### Update data source
1. Download the spreadsheet as CSV format and save it in `dashboard/Django_Dash/Django_Dash_app/dashplotly/csv/` directory
2. Clean up the data  
    2-1. Make sure the first row of the spreadsheet is the one of headers  
    2-2. Delete the columns you do not want to show in the app (e.g. the columns marking the progress of editing data)
3. Go to `dashboard/Django_Dash/Django_Dash_app/dashplotly/dashboard_app.py` and update the name of the newest spreadsheet in the following code ( 
which is the first line of the program after importing libraries is done)
   ```
   df = pd.read_csv('Django_Dash_app/dashplotly/csv/<name-of-your-spreadsheet>.csv') 
   ```
4. Run the server and check if anything goes off. Adjust either the program or the spreadsheet accordingly. 
