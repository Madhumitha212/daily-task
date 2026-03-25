from .run_queries import run_redshift_query
from faker import Faker
import random

fake = Faker()

for i in range(200, 220):
    weather_id = i
    city_id = random.randint(1, 3)
    time_id = random.randint(100, 119)
    temperature = round(random.uniform(20,40),2)

    insert_weather_data = """
                            INSERT INTO weather_fact(weather_id, city_id, time_id,temperature)
                            VALUES ({}, {}, {}, {})
                            """.format(weather_id, city_id, time_id, temperature)

    run_redshift_query(insert_weather_data)


for i in range(100, 120):
     dt = fake.date_time_this_year()

     time_id = i
     timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
     day = dt.day
     month = dt.month
     year = dt.year

     insert_time_table = f"""
                            INSERT INTO time_dim(time_id, timestamp, day, month, year)
                            VALUES ({time_id}, '{timestamp}', {day}, {month}, {year})
                            """

     run_redshift_query(insert_time_table)

for i in range(1, 21):
    city_id = i
    city_name = fake.city()
    country = "India"

    insert_city =f"""
                  INSERT INTO city_dim(city_id, city_name, country)
                  VALUES ({city_id}, '{city_name}', '{country}')
                  """
    run_redshift_query(insert_city)


