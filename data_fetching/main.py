import csv
import json
import os
import random
import time
from typing import Dict

import requests

from .config import CIAN_API_URL, CIAN_REQUEST_LAG, REFERER, USER_AGENT


def generate_payload(region_code: int, page_number: int) -> Dict:
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


def json_parser(objects: object, file_name: str, adress_code: int) -> None:
    """Process a JSON responce and write a file with raw data"""
    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for object in objects:
            writer.writerow([object['cianId'],
                             object['adfoxParams']['puid8'],
                             float(object['totalArea']),
                             object['geo']['coordinates']['lat'],
                             object['geo']['coordinates']['lng'],
                             object['geo']['address'][adress_code]['id'],
                             object['geo']['address'][adress_code]['fullName'],
                             int(object['adfoxParams']['puid8'] /
                                 float(object['totalArea']))
                             ])


def data_fetching(region_name: str, region_config: Dict) -> None:
    """Data request by pages, process a responce"""
    csv_file_path = f'data/{region_name}.csv'
    if os.path.exists(csv_file_path) == False:
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

    url = CIAN_API_URL
    headers = {'user-agent': USER_AGENT,
               'referer': REFERER}

    pages_list = range(region_config['first page'],
                       region_config['last page'] + 1)

    for page_number in pages_list:
        post_request = requests.post(url,
                                     json=generate_payload(
                                         region_config['region code'],
                                         page_number),
                                     headers=headers)
        data = json.loads(post_request.text)
        objects = data['data']['offersSerialized']

        json_parser(objects, csv_file_path, region_config['adress code'])
        time.sleep(random.randint(*CIAN_REQUEST_LAG))
