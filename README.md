# PelotonDashboard
This project is a dashboard for Peloton workouts created as part of a [tutorial](https://josetheengineer.dev/how-to-build-a-dashboard-for-your-peloton-workout-data-using-dash) on my blog.

## Generating fake csv

In order to generate fake data to follow along with the tutorial, I have created the csv_generator.py script.

This script uses sample workouts from scraped_workouts.csv to generate fake workout metrics and metadata which provides a somewhat anonymized csv.

To run this script, you will need to install the dependencies from the requirements.txt file. This script will output a csv file named workouts.csv in the directory it is run from.

```
source venv/bin/activate && pip install -r requirements.txt
python csv_generator.py
```
