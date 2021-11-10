from config import regions
from data_fetching import data_fetching
from data_processing import data_preparation, create_heat_map, \
    create_graph_average_price, create_graph_average_square
import os

if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)

    for region_name, region_config in regions.items():
        data_fetching(region_name, region_config)

        df = data_preparation(region_name, region_config)

        create_heat_map(df, region_name, region_config)

        create_graph_average_price(df, region_name)

        create_graph_average_square(df, region_name)
