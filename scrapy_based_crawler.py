import scrapy
import os
import json
from tqdm import tqdm
import yaml

def get_outliers(lst):
    
    groups = {}
    # Group strings by first three characters
    for string in lst:
        try:
            group_key = string.split('_')[1][:3]
        except:
            continue
        # if group_key == '1700':
        #     continue
        if group_key not in groups:
            groups[group_key] = [string]
        else:
            groups[group_key].append(string)

    # Filter groups to only include single members
    single_member_groups = [group[0] for group in groups.values() if len(group) == 1]

    return single_member_groups

def load_config():
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    return config


class DigikalaSpider(scrapy.Spider):
    name = "digi-ganj"

    def start_requests(self):
        self.headers = {
            'authority': 'api.digikala.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-GB,en;q=0.9,fa-IR;q=0.8,fa;q=0.7,en-US;q=0.6',
            # 'cookie': '_hjSessionUser_2754176=eyJpZCI6Ijg0ZDI3YzQ1LTkyNjEtNWE5Mi1hMDlhLTRiZDdkZTFhMDI3MyIsImNyZWF0ZWQiOjE2NzA5MzY4MzUzMDQsImV4aXN0aW5nIjp0cnVlfQ==; _ga_S5JJQD4MDE=GS1.1.1682753314.1.1.1682753330.0.0.0; _ga_4S04WR965Q=GS1.1.1684917928.17.1.1684918263.0.0.0; _conv_r=s%3Awww.google.com*m%3Aorganic*t%3A*c%3A; _ym_uid=1687986679620631938; _ym_d=1687986679; _conv_v=vi%3A1*sc%3A20*cs%3A1688311188*fs%3A1670936829*pv%3A41*exp%3A%7B%7D*ps%3A1688050938*seg%3A%7B10002577.1%7D; ph_phc_sZZBNR08PFM9Mf5GBbb9lBvujTlo4IBdbb15beviIpX_posthog=%7B%22distinct_id%22%3A%220189e7af-7470-7d08-acb9-ccf9c99a739e%22%2C%22%24device_id%22%3A%220189e7af-7470-7d08-acb9-ccf9c99a739e%22%2C%22%24user_state%22%3A%22anonymous%22%2C%22%24sesid%22%3A%5B1691809182838%2C%220189e7af-7476-7591-9614-7c9bb7ae65e0%22%2C1691809182838%5D%2C%22%24session_recording_enabled_server_side%22%3Afalse%2C%22%24autocapture_disabled_server_side%22%3Atrue%2C%22%24active_feature_flags%22%3A%5B%5D%2C%22%24enabled_feature_flags%22%3A%7B%7D%2C%22%24feature_flag_payloads%22%3A%7B%7D%7D; _ga_LR50FG4ELJ=GS1.1.1693721522.50.1.1693722816.60.0.0; _ga_50CEWK5GC9=GS1.1.1696253660.5.1.1696254365.0.0.0; _sp_id.3a05=f3b5dc63-b470-4b4b-a109-552fa1ea4c55.1697453470.1.1697453799..4b36da6c-3c5b-4c77-9ac1-3a2f27b1daa0..3ac3a0f1-de8a-4cdf-9bec-87a36ebc52a3.1697453469829.6; ab_test_experiments=%5B%5D; _ga_B05FSHYDGX=GS1.2.1699884558.1.0.1699884558.0.0.0; _ga=GA1.1.500616008.1670936827; _ga_YTPKDQLPZM=GS1.1.1700401941.6.1.1700402241.0.0.0; _clck=1csduoi%7C2%7Cfgv%7C0%7C1419; _clsk=wetniu%7C1700504112791%7C1%7C1%7Cw.clarity.ms%2Fcollect; _sp_ses.13cb=*; _hp2_ses_props.1726062826=%7B%22ts%22%3A1700569739962%2C%22d%22%3A%22www.digikala.com%22%2C%22h%22%3A%22%2F%22%7D; _hp2_id.1726062826=%7B%22userId%22%3A%225995641228348843%22%2C%22pageviewId%22%3A%222913432168219845%22%2C%22sessionId%22%3A%226595711302771274%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; tracker_glob_new=679Jm4F; tracker_session=8J2CzhT; TS01c77ebf=01023105916a827e3715c9abb93185cd13e816fee675051cebe8936945eeff695da830d7475649a9b14c93b851e3edbf2fe34811f8d18251b378cf9849ae2b35bc56b1e3fa0ae3065e4fbe37a90dd738ad31ec7d59; _sp_id.13cb=24953406-39ed-4be5-a098-c6e4cd7b0538.1670936829.83.1700570170.1700553830.9b232083-cd5f-4cfd-8688-337f75abef94.07e5d7a1-60e9-408b-b872-3594de7b86f2.674b1f15-f524-426d-8648-3efe944ca301.1700569740005.66; _ga_QQKVTD5TG8=GS1.1.1700569739.19.1.1700570880.0.0.0',
            'origin': 'https://www.digikala.com',
            'referer': 'https://www.digikala.com/',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'x-web-client': 'desktop',
            'x-web-optimize-response': '1',
        }

        config = load_config()
        self.valid_urls = lambda urls: get_outliers(urls)
        os.makedirs('./images', exist_ok=True)
        os.makedirs('./images/candidates', exist_ok=True)
        os.makedirs('./products-info', exist_ok=True)
        start, end = config['start'], config['end']

        for page_num in tqdm(range(start, end)):
            # params = {
            # 'has_selling_stock': '1',
            # 'sort': '7',
            # 'page': str(page_num),
            # }
            prefix = 'https://api.digikala.com/v1/categories/'
            postfix = f'/search/?seo_url=&has_selling_stock=1&page={page_num}' 
            START_URL = prefix + config['start_url'] + postfix 
            yield scrapy.Request(START_URL, callback=self.parse, headers=self.headers)

    def parse(self, response):
            products_data = response.json()
            product_ids = [item['id'] for item in products_data['data']['products']]
            for id in product_ids:
                yield scrapy.Request(f'https://api.digikala.com/v2/product/{id}/', headers=self.headers, callback=self.get_product, meta={'id':id})

    def get_product(self, response):
        product_data = response.json()
        id = response.meta.get('id')
        with open(f'./products-info/{id}.json', 'w+') as f:
            json.dump(product_data, f)


        images_url = response.json()['data']['product']['images']['list']
        urls = [url['url'][0].split('?')[0] for url in images_url]
        valid_urls = self.valid_urls(urls)
        for url in valid_urls:
            yield scrapy.Request(url, callback=self.get_image, headers=self.headers, meta={'id':id})

    def get_image(self, response):
        id = response.meta.get('id')
        if response.status == 200:
            filename = response.url.split('/')[-1]
            image_path = os.path.join('./images/candidates', str(id) + '__' + filename)

            with open(image_path, 'wb') as f:
                f.write(response.body)
                self.log('Saved file {}'.format(image_path))
        else:
            self.log('Image download failed for URL {}: HTTP status {}'.format(response.url, response.status))

import scrapy
from scrapy.crawler import CrawlerProcess

import scrapy
from scrapy.crawler import CrawlerProcess
process = CrawlerProcess(
    settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
        "CONCURRENT_REQUESTS":1
    }
)
process.crawl(DigikalaSpider)
process.start()  # the script will block here until the crawling is finished