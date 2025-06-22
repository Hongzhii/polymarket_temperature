import requests
import ast

from typing import List, Tuple, Mapping

def search_by_slug(slug) -> Mapping:
    """
    Searches for events by slug using the Polymarket Gamma API.

    Args:
        slug (str): The slug of the event to search for.

    Returns:
        dict: The JSON response from the API, or None if the request fails.
    """
    gamma_url = "https://gamma-api.polymarket.com/events"
    params = {"slug": slug}

    try:
        response = requests.get(gamma_url, params=params).json()[0]
    except IndexError:
        raise ValueError(f"Failed to fetch {slug}")

    return response


def extract_clob_tid(data) -> List[Tuple]:
    """
    Extracts the clob token IDs from the market data.

    Args:
        data (dict): The JSON response from the API.

    Returns:
        list: A list of tuples, where each tuple contains:
            1. Question
            2. Clob token IDs
            3. Outcomes for a market
    """
    markets = data["markets"]

    result = [
        (
            market["question"],
            ast.literal_eval(market["clobTokenIds"]),
            ast.literal_eval(market["outcomes"]),
        )
        for market in markets
    ]

    return result

def get_market_metadata(slug):
    raw_data = search_by_slug(slug)
    return extract_clob_tid(raw_data)

