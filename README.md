# PelotonDashboard
This project is a dashboard for Peloton workouts created as part of a [tutorial](https://josetheengineer.dev/how-to-build-a-dashboard-for-your-peloton-workout-data-using-dash) on my blog.


## Generate Fake Data
In order to generate anonymized data to follow along with the tutorial, I have created a fake data generator that can be used to generate a fake csv to use along with the dashboard. The fake data generator is located in the `csv_generator.py` file and uses predefined normal distribution parameters to generate fake workout metrics. After running the generator, the fake data is located in the `workouts.csv` file in the root directory.

```
source venv/bin/activate && pip install -r requirements.txt
python csv_generator.py
```