import os

from config import REGIONS
from data_fetching.main import DataFetcher
from data_processing.main import DataProcessor

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    for region_name, region_config in REGIONS.items():
        data = DataFetcher(region_name, region_config)
        data.fetch_data()
        region = DataProcessor(region_name, region_config)
        region.draw()
