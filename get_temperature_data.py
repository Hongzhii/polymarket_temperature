import datetime
import time
import requests
import os
import xml.etree.ElementTree as ET

DATA_DIR = "data/temperature_data"

# Dictionary to store the last recorded temperature for each location
last_temperatures = {}
last_measurement_times = {}

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
    global last_measurement_times  # Access the global dictionary
    url = "https://aviationweather.gov/api/data/metar"
    params = {
        "ids": iata_code,
        "format": "xml",
    }

    response = requests.get(url, params=params)
    now = datetime.datetime.now(datetime.UTC)

    parsed_response = parse_xml(response.text)
    time_of_measurement = parsed_response['time_of_measurement']

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

    # Check if the measurement time has changed
    # Convert time_of_measurement to datetime object for comparison
    time_of_measurement_dt = datetime.datetime.fromisoformat(time_of_measurement.replace('Z', '+00:00'))
    
    # Convert last measurement time to datetime object if it exists
    if iata_code in last_measurement_times:
        last_measurement_dt = datetime.datetime.fromisoformat(last_measurement_times[iata_code].replace('Z', '+00:00'))
        updated = last_measurement_dt < time_of_measurement_dt
    else:
        updated = True  # First measurement for this location

    if not updated:
        print(f"Time of measurement for {iata_code} has not changed. Skipping update.")
        return  # Skip writing if the measurement time is the same

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
    last_measurement_times[iata_code] = time_of_measurement

    print(parsed_response)


def main():
    NYC_ID = "KLGA"
    LON_ID = "EGLC"

    os.makedirs(DATA_DIR, exist_ok=True)

    while True:
        query(NYC_ID)
        query(LON_ID)
        time.sleep(5)

while True:
    try:
        main()
    except Exception as e:
        print(e)
    time.sleep(10)