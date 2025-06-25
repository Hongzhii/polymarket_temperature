import json
import datetime

from typing import Mapping, List, Optional

def get_asset_id_mapping(market_metadata):
    data_dict = dict()

    for market in market_metadata:
        question, clob_tid, outcomes = market
        
        data_dict[clob_tid[0]] = question + " " + outcomes[0]
        data_dict[clob_tid[1]] = question + " " + outcomes[1]

    return data_dict

def load_raw_data(
    fp: str,
    timestamp: Optional[datetime.datetime] = None,
) -> List[Mapping]:
    """
    Loads raw data from a JSON file.

    The function reads the file, replaces any occurrences of "][" with ",",
    and then parses the JSON data.

    If a timestamp is provided, the function filters the data to include 
    only entries with timestamps greater than or equal to the provided 
    timestamp.
        
    Args:
        fp (str): The file path to the JSON file.
        timestamp (datetime.datetime, optional): The datetime object to
            filter the data from. Defaults to None.
    Returns:
        List[Mapping]: A list of dictionaries representing the loaded data.
    """

    with open(fp) as f:
        raw_text = f.read()

    raw_text = raw_text.replace("[]", "")
    raw_text = raw_text.replace("][", ",")
    data = json.loads(raw_text)

    if timestamp:
        for i, entry in enumerate(data):
            if unix_to_utc(entry["timestamp"]) > timestamp:
                break
        data = data[i:]

    return data

def unix_to_utc(timestamp: str) -> datetime.datetime:
    """Converts a Unix timestamp (in milliseconds) to a UTC datetime object.

        Args:
            timestamp (str): A Unix timestamp in milliseconds.

        Returns:
            datetime.datetime: A datetime object representing the timestamp in UTC.
        """
    if len(timestamp) == 13:
        timestamp = timestamp[:-3]

    return datetime.datetime.fromtimestamp(
        int(timestamp),
        datetime.UTC,
    )
