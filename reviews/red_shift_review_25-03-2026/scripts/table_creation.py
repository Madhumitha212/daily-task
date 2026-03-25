from .run_queries import *

def create_tables():
    weather_fact = f"""
    CREATE TABLE weather_fact (
        weather_id INT PRIMARY KEY,
        city_id INT,
        time_id INT,
        temperature FLOAT
    )
    DISTKEY(city_id)
    SORTKEY(time_id);
    """

    city_table = f"""
    CREATE TABLE city_dim (
        city_id INT PRIMARY KEY,
        city_name VARCHAR(100),
        country VARCHAR(50)
    );
    """

    time_table = f"""
    CREATE TABLE time_dim(
        time_id INT PRIMARY KEY,
        timestamp TIMESTAMP,
        day INT,
        month INT,
        year INT
    )
    """

    print("Creating weather fact table...")
    run_redshift_query(weather_fact)
    print("Creating city table...")
    run_redshift_query(city_table)
    print("Creating time table")
    run_redshift_query(time_table)

if __name__ == "__main__":
    create_tables()
