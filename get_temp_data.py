import datetime
import time
import requests
import os
import xml.etree.ElementTree as ET

DATA_DIR = "data/temperature_data"

# Dictionary to store the last recorded temperature for each location
last_temperatures = {}

def parse_xml(text):
    root = ET.fromstring(text)

    for metar in root.findall(".//METAR"):
        observation_time = metar.find("observation_time").text
        temp_c = metar.find("temp_c").text
    

    result = {
        "time_of_measurement": observation_time,
        "temperature": temp_c,
    }

    return result

def query(iata_code):
    global last_temperatures  # Access the global dictionary
    url = "https://aviationweather.gov/api/data/metar"
    params = {
        "ids": iata_code,
        "format": "xml",
    }

    response = requests.get(url, params=params)
    now = datetime.datetime.now(datetime.UTC)

    parsed_response = parse_xml(response.text)
    temperature = parsed_response['temperature']

    # Determine the correct timezone for the location
    if iata_code == "KLGA":
        timezone = datetime.timezone(datetime.timedelta(hours=-4))  # New York local time during daylight saving
        file_time = datetime.datetime.now(timezone)
    elif iata_code == "EGLC":
        file_time = datetime.datetime.now(datetime.timezone.utc)  # London time is UTC
    else:
        raise ValueError("Unknown IATA code")

    # Create the filename with the local date
    fp = f"{iata_code}_{file_time.strftime('%Y-%m-%d')}.csv"
    fp = os.path.join(DATA_DIR, fp)

    # Check if the temperature has changed
    if iata_code in last_temperatures and last_temperatures[iata_code] == temperature:
        print(f"Temperature for {iata_code} has not changed. Skipping update.")
        return  # Skip writing if the temperature is the same

    # If the file doesn't exist, write the header
    if not os.path.exists(fp):
        with open(fp, "w") as f:
            f.write(
                "time_of_request," + 
                "time_of_measurement," +
                "temperature\n"
            )

    # Append the new data to the file
    with open(fp, "a") as f:
        f.write(
            f"{now}," +
            f"{parsed_response['time_of_measurement']}," +
            f"{parsed_response['temperature']}\n"
        )

    # Update the last recorded temperature
    last_temperatures[iata_code] = temperature

    print(parsed_response)


def main():
    NYC_ID = "KLGA"
    LON_ID = "EGLC"

    os.makedirs(DATA_DIR, exist_ok=True)

    while True:
        query(NYC_ID)
        query(LON_ID)
        time.sleep(30)

while True:
    try:
        main()
    except Exception as e:
        print(e)
    time.sleep(60)