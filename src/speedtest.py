from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import logging
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_internet_speed(driver):
    try:
        driver.get("https://www.speedtest.net")
        go_button = driver.find_element(By.CSS_SELECTOR, ".start-button a")
        go_button.click()

        WebDriverWait(driver, 120).until(
            lambda d: d.find_element(By.CSS_SELECTOR, ".upload-speed").get_attribute("data-upload-status-value") != "NaN"
        )

        download_speed = driver.find_element(By.CSS_SELECTOR, ".download-speed").text
        upload_speed = driver.find_element(By.CSS_SELECTOR, ".upload-speed").text
        ping = driver.find_element(By.CSS_SELECTOR, ".ping-speed").text
    except Exception as e:
        logger.error(f"Exception when checking internet speed: {e}")
        download_speed = "N/A"
        upload_speed = "N/A"
        ping = "N/A"
    return {"download_speed": download_speed, "upload_speed": upload_speed, "ping": ping}