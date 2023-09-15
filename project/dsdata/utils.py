import requests


def currents_lookup(latitude, longitude):
    url = ("http://meteo:5000/get_currents_data"
           f"?latitude={latitude}&longitude={longitude}")
    response = requests.get(url, timeout=0.2)
    if response.status_code == 200:
        data = response.json()
        return data

    raise Exception("Could not retreive data from "
                    "the currents microservice")