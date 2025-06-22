import pandas as pd
import datetime

from typing import Tuple

class TemperatureBook():
    def __init__(
        self,
        fp_data: str,
    ) -> None:
        self.data = pd.read_csv(fp_data)

        def celsius_to_fahrenheit(celsius: float) -> int:
            """Converts celsius to fahrenheit."""
            fahrenheit = (celsius * 9/5) + 32
            return int(round(fahrenheit))

        self.data["temperature_fahrenheit"] = self.data["temperature"].apply(celsius_to_fahrenheit)
        self.data["temperature"] = self.data.apply(lambda row: f"{row['temperature']} ({row['temperature_fahrenheit']}f)", axis=1)
        self.data = self.data.drop(columns=["temperature_fahrenheit"])

        self.data["time_of_request"] = pd.to_datetime(self.data["time_of_request"])
        self.data["time_of_measurement"] = pd.to_datetime(self.data["time_of_measurement"])

    def query(
        self,
        timestamp: datetime.datetime,
        criteria: str = "request",
    ) -> Tuple[datetime.datetime, datetime.datetime, float]:
        """
        Queries the temperature book for the nearest temperature reading at or before a given timestamp.

        Args:
            timestamp (datetime.datetime): The timestamp to query for.

        Returns:
            Tuple[datetime.datetime, datetime.datetime, float]: A tuple containing the time of request,
            time of measurement, and temperature of the nearest reading.
            Returns "No valid data" if no data is available before the given timestamp.
        """

        if criteria == "measurement":
            df = self.data[self.data["time_of_measurement"] <= timestamp].sort_values("time_of_measurement")
        elif criteria == "request":
            df = self.data[self.data["time_of_request"] <= timestamp].sort_values("time_of_request")
        else:
            raise ValueError(f"Invalid criteria: {criteria}. Must be 'measurement' or 'request'.")

        if len(df) == 0:
            return None

        nearest_time = df.iloc[-1]

        return (
            nearest_time["time_of_request"],
            nearest_time["time_of_measurement"],
            nearest_time["temperature"]
        )

