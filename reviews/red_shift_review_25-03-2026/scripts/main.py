from fastapi import FastAPI
from scripts.run_queries import run_redshift_query

app = FastAPI()

@app.get("/avg-temp")
def get_avg_temp():
    avg_temp = """
        SELECT c.city_name, round(AVG(w.temperature),2) AS avg_temp
        FROM weather_fact w
        JOIN city_dim c ON w.city_id = c.city_id
        GROUP BY c.city_name;
    """

    result = run_redshift_query(avg_temp)

    records = []
    for row in result['Records']:
        values = [list(col.values())[0] for col in row]
        records.append({"city_name": values[0], "avg_temp": values[1]})

    return records