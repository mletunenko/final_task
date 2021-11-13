import csv
import json
import os
import random
import time
from typing import Dict, List

import requests

from .config import CIAN_API_URL, CIAN_REQUEST_LAG, REFERER, USER_AGENT


class DataFetcher:
    def __init__(self, region_name: str, region_config: Dict) -> None:
        self.region_name = region_name
        self.region_config = region_config

    @staticmethod
    def _check_csv_file_exist(csv_file_path: str) -> None:
        """Check if csv-file exist, and create it if not"""
        if not os.path.exists(csv_file_path):
            with open(csv_file_path, 'a') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['cian_id',
                                 'price',
                                 'square',
                                 'coord_lat',
                                 'coord_lng',
                                 'district_id',
                                 'district_name',
                                 'price_per_meter'])

    @staticmethod
    def _json_parser(rows: list, file_name: str, adress_code: int) -> None:
        """Process a JSON response and write a file with raw data"""
        with open(file_name, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in rows:
                writer.writerow([row['cianId'],
                                 row['adfoxParams']['puid8'],
                                 float(row['totalArea']),
                                 row['geo']['coordinates']['lat'],
                                 row['geo']['coordinates']['lng'],
                                 row['geo']['address'][adress_code]['id'],
                                 row['geo']['address'][adress_code][
                                     'fullName'],
                                 int(row['adfoxParams']['puid8'] /
                                     float(row['totalArea']))
                                 ])

    @staticmethod
    def _generate_payload(region_code: int, page_number: int) -> Dict:
        """Create a payload for POST request"""
        result = {
            'jsonQuery': {
                'region': {
                    'type': 'terms',
                    'value': [
                        region_code
                    ]
                },
                '_type': 'flatsale',
                'engine_version': {
                    'type': 'term',
                    'value': 2
                },
                'page': {
                    'type': 'term',
                    'value': page_number
                }
            }
        }
        return result

    def _get_pages_list(self) -> List:
        """Create a list of pages for requests"""
        return range(self.region_config['first page'],
                     self.region_config['last page'] + 1)

    def fetch_data(self) -> None:
        """Fetch data from requests and write it to csv-file"""
        csv_file_path = f'data/{self.region_name}.csv'
        DataFetcher._check_csv_file_exist(csv_file_path)
        url = CIAN_API_URL
        headers = {'user-agent': USER_AGENT,
                   'referer': REFERER}
        pages_list = self._get_pages_list()
        for page_number in pages_list:
            post_request = requests.post(url,
                                         json=DataFetcher._generate_payload(
                                             self.region_config['region code'],
                                             page_number),
                                         headers=headers)
            rows = json.loads(post_request.text)['data']['offersSerialized']
            DataFetcher._json_parser(rows, csv_file_path,
                                     self.region_config['adress code'])
            time.sleep(random.randint(*CIAN_REQUEST_LAG))
