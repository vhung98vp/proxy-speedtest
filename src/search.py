import time
from selenium.webdriver.common.by import By
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_company(driver, company_name):
    site_url = "masothue.com"
    search_query = f"{company_name} {site_url}"
    try:
        driver.get(f"https://www.google.com/search?q={search_query}&hl=vi")
    except Exception as e:
        logger.error(f"Can't search google, error: {e}")

    start_time = time.time()

    def get_first_url():
        try:
            match_url = driver.find_element(By.XPATH, "//a[contains(@href, '%s')]" % f"https://{site_url}")
            return match_url.get_attribute("href")
        except Exception as e:
            logger.error(f"Exception when get first url while searching google: {e}")
            return ""
    
    first_url = get_first_url()
    
    search_time = time.time() - start_time
    if not first_url:
        try:
            recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
            if recaptcha_iframe:
                logger.error("Recaptcha detected...")
                time.sleep(30)
                first_url = get_first_url()
                search_time = time.time() - start_time - 30
        except Exception as e:        
            logger.error(f"Exception when get first url while searching google: {e}")
    
    return first_url, search_time