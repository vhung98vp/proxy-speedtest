import os
import re
import time
import requests
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_proxy_list():
    load_dotenv()
    proxy_server = os.getenv('PROXY_SERVER', '')
    match = re.match(r"(http|https)://([^/:]+)", proxy_server)
    if match:
        try:
            logger.info(f"Getting proxy list from {proxy_server}...")
            response = requests.get(f"{proxy_server}/proxy_list")
            time.sleep(2)
            if response.status_code == 200:
                proxy_list = response.json()
                logger.info(f"Retrieved {len(proxy_list)} proxies")
                return proxy_list
        except Exception as e:
            logger.error("Error, Fail to get proxy: ", e)
    return []