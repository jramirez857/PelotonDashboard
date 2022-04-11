import csv
import datetime
import random
from typing import Union

import numpy as np
import pandas as pd
from faker import Faker

Faker.seed(42)
fake = Faker(locale="en_US")

df = pd.read_csv("scraped_workouts.csv")
gby = df.groupby(["Fitness Discipline", "Type", "Length (minutes)", "Title"])


def generate_positive_number(mean: float, sigma: float, round_to: int = 2) -> float:
    """
    Generates a random float value with a normal distribution. If the
    number is not positive, it will be generated again.

    Args:
        mean (Union[float,int]): The mean of the normal distribution.
        sigma (Union[float, int]): The standard deviation of the normal distribution.
        round_to (Union[float, int]): The number of decimal places to round the number to. Defaults to 2.

    Returns:
        float: A positive number of round_to decimal places.
    """
    x = round(np.random.normal(mean, sigma), round_to)
    return x if x > 0 else generate_positive_number(mean, sigma, round_to)


def generate_value(
    mean: float, sigma: float, discipline: str, column: str, round_to: int = 2
) -> Union[float, None]:
    """
    Generates a random value with fixed mean and sigma for a given column.
    Returns None if the column key does not make sense for the type of discipline.
    Otherwise, returns the value with the given round_to decimal places.

    Args:
        mean (float): The mean of the normal distribution.
        sigma (float): The standard deviation of the normal distribution.
        discipline (str): The fitness discipline of the current row.
        round_to (int, optional): The number of digits to round the generated number to. Defaults to 2.
        column (_type_, optional): The column header to get random value for. Defaults to None.

    Returns:
        Union[float, None]: _description_
    """
    if discipline != "Cycling" and column in {
        "watts",
        "resistance",
        "cadence",
        "speed",
        "distance",
        "calories",
        "heart_rate",
    }:
        return None
    if discipline == "Running" and column == "heart_rate":
        return None
    if discipline == "Meditation" or discipline == "Running" and column == "output":
        return None
    if discipline == "Cycling" and column == "resistance":
        return round(random.random() * 100, round_to)
    switcher = {
        "output": generate_positive_number(mean, sigma, round_to),
        "resistance": None,
        "watts": generate_positive_number(100, 30),
        "cadence": generate_positive_number(80, 13, 0),
        "speed": generate_positive_number(18, 3.40, 0),
        "distance": generate_positive_number(8, 5.02),
        "calories": generate_positive_number(200, 180, 0),
        "heart_rate": generate_positive_number(140, 20),
    }
    return switcher.get(column)


def generate_workout_metadata(row):
    """
    Generates a workout metadata dictionary.

    Args:
        row (DataFrame): A row from the scraped_workouts.csv file.

    Returns:
        dict: A workout metadata dictionary.
    """
    instructor_name = row["Instructor Name"].values[0]
    length = row["Length (minutes)"].values[0]
    fitness_discipline = row["Fitness Discipline"].values[0]
    workout_type = row["Type"].values[0]
    title = row["Title"].values[0]
    return [instructor_name, length, fitness_discipline, workout_type, title]


def write_headers(writer: csv.writer):
    """
    Writes the headers for the csv file.

    Args:
        writer (csv.writer): Headers for the csv file.
    """
    writer.writerow(
        [
            "Workout Timestamp",
            "Live/On-Demand",
            "Instructor Name",
            "Length (minutes)",
            "Fitness Discipline",
            "Type",
            "Title",
            "Class Timestamp",
            "Total Output",
            "Avg. Watts",
            "Avg. Resistance",
            "Avg. Cadence (RPM)",
            "Avg. Speed (mph)",
            "Distance (mi)",
            "Calories Burned",
            "Avg. Heartrate",
            "Avg. Incline",
            "Avg. Pace (min/mi)",
        ]
    )


def generate_workout_metrics(fitness_discipline):
    """
    Returns a dict of key value pairs for the workout metrics for a given fitness discipline.

    Args:
        fitness_discipline (str): The fitness discipline of the current row.

    Returns:
        dict: A dict of key value pairs for the workout metrics.
    """
    total_output = generate_value(150.5, 10.80, fitness_discipline, "output", 2)
    avg_watts = generate_value(120, 35, fitness_discipline, "watts", 2)
    avg_resistance = generate_value(None, None, fitness_discipline, "resistance", 2)
    avg_cadence = generate_value(80, 15, fitness_discipline, "cadence", 0)
    avg_speed = generate_value(15.59, 2.10, fitness_discipline, "speed", 2)
    distance = generate_value(6.79, 5.89, fitness_discipline, "distance", 2)
    calories = generate_value(196.97, 178.52, fitness_discipline, "calories", 0)
    heart_rate = generate_value(149, 22.89, fitness_discipline, "heart_rate", 2)
    return [total_output, avg_watts, avg_resistance, avg_cadence, avg_speed, distance, calories, heart_rate]


def generate_csv() -> None:
    """
    Uses sample data from the scraped_workouts.csv file to generate a csv file with Peloton workouts.
    """
    with open("workouts.csv", "w", newline="") as f:
        writer = csv.writer(f)
        write_headers(writer)
        for _ in range(random.randint(100, 1000)):
            sample_row = df.sample()
            workout_timestamp = fake.date_time_between_dates(
                datetime_start=datetime.datetime(2021, 1, 1), datetime_end="now"
            )
            workout_live_on_demand = "Live" if fake.boolean() else "On Demand"
            workout_metadata = generate_workout_metadata(sample_row)
            class_timestamp = fake.date_time_between_dates(
                datetime_start=datetime.datetime(2021, 1, 1), datetime_end="now"
            )
            workout_metrics = generate_workout_metrics(workout_metadata[2])
            row = [workout_timestamp,workout_live_on_demand] + workout_metadata + [class_timestamp] + workout_metrics
            row.extend([None, None])
            writer.writerow(row)


if __name__ == "__main__":
    generate_csv()
