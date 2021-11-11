import os
from config import REGIONS
from data_fetching.main import data_fetching
from data_processing.main import (create_graph_average_price,
                                  create_graph_average_square, create_heat_map,
                                  data_preparation)

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    os.makedirs('output', exist_ok=True)

    for region_name, region_config in REGIONS.items():
        data_fetching(region_name, region_config)
        df = data_preparation(region_name, region_config)
        create_heat_map(df, region_name, region_config)
        create_graph_average_price(df, region_name)
        create_graph_average_square(df, region_name)
