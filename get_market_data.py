import asyncio
import os

from utils.websocket_utils import monitor_market
from utils.gamma_utils import get_market_metadata
from utils.utils import get_asset_id_mapping

LON = "highest-temperature-in-london-on-june-24"
NYC = "highest-temperature-in-nyc-on-june-24"
DATA_DIR = "data/market_data"

def get_asset_ids(slug):
    metadata = get_market_metadata(slug)
    asset_id_mapping = get_asset_id_mapping(metadata)

    return asset_id_mapping

async def main():
    nyc_mappings = get_asset_ids(NYC)
    lon_mappings = get_asset_ids(LON)
    os.makedirs(DATA_DIR, exist_ok=True)

    task1 = asyncio.create_task(
        monitor_market(
            list(lon_mappings.keys()),
            os.path.join(DATA_DIR, LON),
        )
    )
    task2 = asyncio.create_task(
        monitor_market(
            list(nyc_mappings.keys()),
            os.path.join(DATA_DIR, NYC),
        )
    )

    result1 = await task1
    result2 = await task2

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print(e)