import os
import re
import random
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from .driver import get_driver
from .proxy import get_proxy_list
from .search import search_company
from .speedtest import check_internet_speed
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_ip_address(driver):
    try:
        driver.get("https://api.ipify.org")  
        ip_address = driver.find_element("tag name", "body").text
        logger.info(f"Current IP address: {ip_address}")
    except Exception as e:
        logger.error(f"Error while getting IP address: {e}")
        ip_address = "N/A"
    return ip_address


def test_proxy(proxy, company_name):
    driver = get_driver(proxy, True)
    ip_address = get_ip_address(driver)
    speed_result = check_internet_speed(driver)
    first_url, search_time = search_company(driver, company_name)
    driver.quit()

    logger.info(f"Proxy: {proxy} - IP: {ip_address}")
    logger.info(f"Download: {speed_result['download_speed']} Mbps - Upload: {speed_result['upload_speed']} Mbps - Ping: {speed_result['ping']} ms")
    logger.info(f"Found URL: {first_url} - Search Time: {search_time:.6f} seconds")

    return {
        "proxy": proxy,
        "ip": ip_address,
        "speed_result": speed_result,
        "company_name": company_name,
        "first_url": first_url,
        "search_time": search_time
    }

def test_all_proxies():
    companies = [
        "Vinamilk", "Vietcombank", "FPT", "Techcombank", "Masan", "Vingroup",
        "PetroVietnam", "Vietnam Airlines", "BIDV", "VietinBank", "Hoa Phat",
        "Vinacafe", "Saigon Beer", "Novaland", "Sun Group", "THACO",
        "Tiki", "Shopee", "Lazada", "Zalora", "Momo", "Grab", "Zalo", "Go-Viet",
        "Sendo", "VinFast", "VinSmart", "Vinpearl", "VinHomes", "VinMart",
        "Bitexco", "Viettel", "Mobifone", "VNPT", "VinaPhone", "FLC Group",
        "Kido", "Dabaco", "Thien Long Group", "Vinasoy", "Sabeco", "Habeco",
        "VietJet Air", "Bamboo Airways", "Jetstar Pacific", "Saigontourist",
        "Ben Thanh Group", "Saigon Co.op", "Big C", "Lotte Mart", "AEON",
        "Circle K", "FamilyMart", "Bach Hoa Xanh", "VinMart+", "Co.op Food",
        "The Gioi Di Dong", "Dien May Xanh", "FPT Shop", "Viettel Store",
        "Mediamart", "Nguyen Kim", "Phuc Long", "Highlands Coffee", "Starbucks",
        "The Coffee House", "Trung Nguyen Coffee", "KFC", "Lotteria",
        "Burger King", "McDonald's", "Pizza Hut", "Domino's Pizza", "Jollibee",
        "CGV", "Lotte Cinema", "Beta Cineplex", "Galaxy Cinema", "BHD Star",
        "Vincom", "Crescent Mall", "Parkson", "Takashimaya", "Diamond Plaza",
        "Saigon Centre", "Bitexco Financial Tower", "Landmark 81", "Keangnam",
        "Vincom Center", "Royal City", "Times City", "Aeon Mall"
    ]

    results = []

    with open("results.json", "a") as file:
        # First test without proxy
        company_name = random.choice(companies)
        logger.info("Testing without proxy...")
        result = test_proxy(None, company_name)
        results.append(result)
        file.write(json.dumps(result, indent=4) + "\n")

        proxy_list = get_proxy_list()
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for i, proxy in enumerate(proxy_list):
                port = proxy.get("proxy_port")
                protocol, ip = re.match(r"(http|https)://([^/:]+)", os.getenv('PROXY_SERVER', '')).groups()
                proxy_string = f"{protocol}://{ip}:{port}"
                company_name = random.choice(companies)
                logger.info(f"Submitting proxy #{i+1}: {proxy_string} for testing...")
                futures.append(executor.submit(test_proxy, proxy_string, company_name))

            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                file.write(json.dumps(result, indent=4) + "\n")

    return results