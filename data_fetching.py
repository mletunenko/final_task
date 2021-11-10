import json
import random
import time
from typing import Dict
import requests
import csv
import os


def payload(region_code: int, page_number: int) -> Dict:
    result = {
        "jsonQuery": {
            "region": {
                "type": "terms",
                "value": [
                    region_code
                ]
            },
            "_type": "flatsale",
            "engine_version": {
                "type": "term",
                "value": 2
            },
            "page": {
                "type": "term",
                "value": page_number
            }
        }
    }
    return result


def json_parser(objects: object, file_name: str, adress_code: int) -> None:
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
    csv_file_path = f"data/{region_name}.csv"
    os.makedirs('data', exist_ok=True)
    if os.path.exists(csv_file_path) == False:
        with open(csv_file_path, "a") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['cian_id',
                             'price',
                             'square',
                             'coord_lat',
                             'coord_lng',
                             'district_id',
                             'district_name',
                             'price_per_meter'])

    url = 'https://api.cian.ru/search-offers/v2/search-offers-desktop/'
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                             '95.0.4638.54 Safari/537.36',
               # 'cookie': '_CIAN_GK=b675ee7e-5330-474c-a4e1-1f65c87fea45; adb=1; login_mro_popup=meow; _gcl_au=1.1.1754581063.1635929063; _ga=GA1.2.108157695.1635929063; uxfb_usertype=searcher; uxs_uid=3f211330-3c82-11ec-adb8-4d2e1dedd9a5; tmr_lvid=f325692433ee831a79bfd68422e15eaa; tmr_lvidTS=1635929064486; afUserId=169c07ed-7c0d-4396-9121-cfc8e42e339b-p; first_visit_time=1635929537524; utm_source=google; utm_medium=cpc; lastSource=google; google_paid=1; cookie_agreement_accepted=true; _ym_uid=1635943855133879491; _ym_d=1635943855; serp_stalker_banner=1; session_region_name=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; forever_region_id=1; forever_region_name=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; is_push_declined=true; utm_campaign=b2c_spb_brand_cian_all_mix_search; fingerprint=42451a31a570cb8c4d77632370b2fd1c; _gid=GA1.2.516716455.1636450212; _gac_UA-30374201-1=1.1636450212.CjwKCAiA1aiMBhAUEiwACw25MZWLAvoxf_k7GtDv6jF_4rx5mv31KnTQ3MabaITKyY4mpdHzOUionBoCKBkQAvD_BwE; utm_term=%2B%D1%86%D0%B8%D0%B0%D0%BD%20%2B%D0%BF%D0%B8%D1%82%D0%B5%D1%80; gclid=CjwKCAiA1aiMBhAUEiwACw25MUKlVKTdl-DKURoGMhl9Z_tyqodOgdRBdQEdC-vpEK-WvofHnHUZZBoCKKcQAvD_BwE; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; serp_registration_trigger_popup=1; sopr_session=f67d2098bdde4119; _fbp=fb.1.1636537339273.1046024066; AF_SYNC=1636537339997; session_region_id=4743; session_main_town_region_id=4743; __cf_bm=o9qbRQfQC3V8rbJngLh9Rl6xAZWxuuyZcF5.DS64Goc-1636538335-0-Ac6nWVgyTQLpLkpJsTLX/DfLq3XAqlecdqvNq2hmlxgDFhv3I/p/jU/ThUtfG3D17NOJIb2zIJXS5Q3qtWLdc2Y=; anti_bot="2|1:0|10:1636538539|8:anti_bot|40:eyJyZW1vdGVfaXAiOiAiNS4xOC4yMDguMjMyIn0=|47b75e5d62e7ba9e6330e00a77c1801d757ad3cca9399567567028d26d6ccc8d"; _dc_gtm_UA-30374201-1=1; cto_bundle=EXuFNl9LdzcyRUg3MDBJcW1xNUNGTzlTbkJDZFdxY29ZWnVpamtIeGxjWGZRalVqVERqOG1CTGZadUFqckdjcEdxZHc1SlVoeldkM2pkUnZwZzRwOG8wUG1tZU13eURubnR6dUxuTmE4dVphS040eng4NElJMm5BUkhOSFBPQlUlMkJyZWRnM1AlMkY3RmVXNG1JWXlGOE5UWlJpamFiMnh1eEdSVXd3UmQwenE3Rk9NNVdKcTVaNCUyRjViMmRVc3ZSWHFXWkMlMkJGVA; tmr_reqNum=231',
               'referer': 'https://ekb.cian.ru/'}

    pages_list = range(region_config['first page'],
                       region_config['last page'] + 1)

    for page_number in pages_list:
        post_request = requests.post(url,
                                     json=payload(region_config['region code'],
                                                  page_number),
                                     headers=headers)
        data = json.loads(post_request.text)
        objects = data['data']['offersSerialized']

        json_parser(objects, csv_file_path, region_config['adress code'])
        time.sleep(random.randint(1, 4))
