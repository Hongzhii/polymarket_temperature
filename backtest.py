import os

from services.MarketBook import MarketBook
from services.TemperatureBook import TemperatureBook
from utils.gamma_utils import get_market_metadata
from utils.utils import get_asset_id_mapping, unix_to_utc
from utils.keystroke_utils import get_key_input


def print_instructions():
    """Prints the available commands to the user."""
    print("===Instructions===")
    print("q\tQuit application")
    print("Left arrow\tSeek earlier by 1 tick")
    print("Right arrow\tSeek later by 1 ime tick")
    print("k\tSeek earlier by 10 ticks")
    print("l\tSeek later by 10 ticks")
    print()


def select_target_market(asset_id_mapping: dict) -> str:
    """Prompts the user to select a target market from the available options.

    Args:
        asset_id_mapping (dict): A dictionary mapping asset IDs to market names.

    Returns:
        str: The asset ID of the selected target market.
    """
    while True:
        print("Please select market to observe:")
        for i, k in enumerate(asset_id_mapping):
            print(f"{i + 1}. {asset_id_mapping[k]}")

        try:
            choice = int(input())
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if 1 <= choice <= len(asset_id_mapping):
            return list(asset_id_mapping)[choice - 1]
        else:
            print("Invalid choice. Please select a number from the list.")


def run_market_backtest(
    marketBook: MarketBook,
    temperatureBook: TemperatureBook = None,
):
    """Runs the backtest loop for a given market.

    Args:
        marketBook (MarketBook): The MarketBook object for the target market.
        temperatureBook (TemperatureBook, optional): The TemperatureBook object. Defaults to None.
    """
    index = 0
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print_instructions()

        if temperatureBook:
            timestamp = unix_to_utc(marketBook[index + 1]["timestamp"])
            temp_data = temperatureBook.query(timestamp)
            print("===Temperature data===")

            if temp_data:
                request, measure, temp = temp_data
                print(f"Time of request: {request}")
                print(f"Nearest measure time: {measure}")
                print(f"Temperature: {temp}")
            else:
                print("No temperature data available for this timestamp.")
            
            print()

        marketBook.display_book(index + 1)  # First state is always None
        user_input = get_key_input()

        if user_input == "q":
            break
        elif user_input == "left":
            if index > 0:
                index -= 1
            else:
                print("Reached the beginning of book history")
        elif user_input == "right":
            if index < len(marketBook) - 1:
                index += 1
            else:
                print("Reached the end of book history")
        elif user_input == "j":
            if index > 0:
                index = max(index - 10, 0)
            else:
                print("Reached the beginning of book history")
        elif user_input == "l":
            if index < len(marketBook) - 1:
                index = min(index + 10, len(marketBook) - 2)
            else:
                print("Reached the end of book history")


def run(
    fp_market_data: str,
    fp_temperature_data: str,
    slug: str,
):
    """Main function to orchestrate the backtest process."""
    market_metadata = get_market_metadata(slug)
    asset_id_mapping = get_asset_id_mapping(market_metadata)

    target_market = select_target_market(asset_id_mapping)

    os.system("cls" if os.name == "nt" else "clear")

    marketBook = MarketBook(
        asset_id=target_market,
        book_name=asset_id_mapping[target_market],
        fp_data=fp_market_data,
    )

    temperatureBook = TemperatureBook(fp_temperature_data)

    run_market_backtest(marketBook, temperatureBook)


if __name__ == "__main__":
    slug = "highest-temperature-in-london-on-june-22"
    fp_market_data = f"data/market_data/{slug}.json"
    fp_temperature_data = (
        "data/temperature_data/EGLC_2025-06-22.csv"
    )

    run(
        fp_market_data,
        fp_temperature_data,
        slug,
    )