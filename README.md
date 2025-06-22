# Polymarket Temperature Backtesting

This project provides a backtesting environment for analyzing Polymarket's temperature prediction markets against real-world temperature data.

## Overview

The project consists of several modules:

-   `get_market_data.py`: Fetches market data from Polymarket using websockets.
-   `get_temp_data.py`: Retrieves temperature data from aviationweather.gov.
-   `backtest.py`: Implements the backtesting logic, allowing users to step through market data and compare it to temperature readings.
-   `services/`: Contains classes for managing market and temperature data.
-   `utils/`: Includes utility functions for data processing and API interactions.
-   `data/`: Stores the fetched market and temperature data.

## Data Sources

-   **Polymarket:** Market data is obtained via websocket from Polymarket's CLOB.
-   **Aviation Weather:** Temperature data is sourced from aviationweather.gov's METAR API.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd polymarket_temperature
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    *Note:* There is no `requirements.txt` file in the workspace. You may need to manually install the required packages, such as `requests` and `websockets`.

## Usage

1.  **Fetch Market and Temperature Data:**

    Run the following scripts to collect market and temperature data:

    ```bash
    python get_market_data.py
    python get_temp_data.py
    ```

    These scripts will store the data in the `data/market_data` and `data/temperature_data` directories, respectively.

2.  **Run the Backtest:**

    Execute the `backtest.py` script to start the backtesting environment:

    ```bash
    python backtest.py
    ```

    The script will prompt you to select a market to observe. Use the arrow keys to navigate through the market data and compare it to the corresponding temperature readings.

### Backtesting Controls

| Key          | Action                      |
| :----------- | :-------------------------- |
| `q`          | Quit the application        |
| `Left arrow` | Seek earlier by 1 tick      |
| `Right arrow`| Seek later by 1 tick        |
| `k`          | Seek earlier by 10 ticks     |
| `l`          | Seek later by 10 ticks     |

## Modules

### `utils`

*   [`utils.get_asset_id_mapping`](utils/utils.py): Maps market metadata to asset IDs.
*   [`utils.load_raw_data`](utils/utils.py): Loads raw data from a JSON file.
*   [`utils.unix_to_utc`](utils/utils.py): Converts Unix timestamps to UTC datetime objects.
*   [`websocket_utils.monitor_market`](utils/websocket_utils.py): Monitors a market using websockets.
*   [`gamma_utils.get_market_metadata`](utils/gamma_utils.py): Retrieves market metadata from the Polymarket Gamma API.
*   [`keystroke_utils.get_key_input`](utils/keystroke_utils.py): Captures user keystrokes for backtesting control.

### `services`

*   [`MarketBook.MarketBook`](services/MarketBook.py): Manages and processes market data, including constructing and updating order books.
*   [`TemperatureBook.TemperatureBook`](services/TemperatureBook.py): Reads and queries temperature data from CSV files.

## Contributing

Contributions are welcome! Please submit a pull request with your changes.

## License

[MIT License](LICENSE)
