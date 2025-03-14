import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
import logging
import random
import time
from .simulate_browsing import simulate_browsing


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEBGL_VENDORS = ['Nvidia GeForce GTX 970', 'Nvidia GeForce GTX 980', 'Nvidia GeForce GTX 980 Ti', 'Nvidia GeForce GTX Titan X', 'AMD Radeon R9 290', 'AMD Radeon R9 290X',
                    'AMD Radeon R9 390', 'AMD Radeon R9 390X', 'AMD Radeon R9 Fury', 'AMD Radeon R9 Fury X', 'AMD Radeon RX 480', 'AMD Radeon RX 580',
                    'AMD Radeon RX 590', 'AMD Radeon RX Vega 64', 'AMD Radeon RX Vega 56', 'AMD Radeon VII', 'AMD Radeon RX 5700', 'AMD Radeon RX 5700 XT',
                    'AMD Radeon RX 5600 XT', 'AMD Radeon RX 5500 XT', 'Nvidia GeForce RTX 2070', 'Nvidia GeForce RTX 2070 Super', 'Nvidia GeForce RTX 2080', 'Nvidia GeForce RTX 2080 Super',
                    'Nvidia GeForce RTX 2080 Ti', 'Nvidia GeForce RTX 3070', 'Nvidia GeForce RTX 3080', 'Nvidia GeForce RTX 3090', 'AMD Radeon RX 6800', 'AMD Radeon RX 6800 XT', 'AMD Radeon RX 6900 XT']
screen_sizes = ['1920,1080', '1366,768', '1440,900', '1600,900',
                '1280,720', '1024,768', '1536,864', '1280,800', '1093,614', '1280,1024']
extensions_dir = os.path.join(os.getcwd(), 'extensions')
extension_files = [f for f in os.listdir(extensions_dir) if f.endswith('.crx')]


def get_driver(proxy=None, open_gui=False):
    user_agent = UserAgent(platforms='desktop').random

    options = Options()
    
    options.add_experimental_option("prefs", {  # For PDF Download
        # "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,  # Avoid opening PDF in browser
        # "profile.managed_default_content_settings.images": 2
    })
    
    if not open_gui:
        options.add_argument("--headless")  # Headless makes the chromedriver not have a GUI
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')

    for _ in range(100):
        width = random.randint(1024, 1920)
        height = random.randint(768, 1080)
        screen_sizes.append(f'{width},{height}')    
    screen_heights = list(range(70, 120))
    screen_widths = list(range(70, 120))

    options.add_argument(f'user-agent={user_agent}')
    options.add_argument(f'--fp-webgl-vendor={random.choice(WEBGL_VENDORS)}')
    options.add_argument(f'--fp-screenheight={random.choice(screen_heights)}')
    options.add_argument(f'--fp-screenwidth={random.choice(screen_widths)}')
    options.add_argument(f"--window-size={random.choice(screen_sizes)}")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--sonet-fingerprinting-client-rects-noise')
    options.add_argument('--sonet-fingerprinting-canvas-image-data-noise')
    options.add_argument('--sonet-fingerprinting-audio-context-data-noise')
    
    # Add additional parameters
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-breakpad")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--disable-component-update")
    # options.add_argument("--disable-default-apps")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-extensions")
    # options.add_argument("--disable-features=Translate,BackForwardCache,AutofillSaveCard,InterestFeedContentSuggestions")
    options.add_argument("--disable-hang-monitor")
    options.add_argument("--disable-ipc-flooding-protection")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-first-run")
    options.add_argument("--no-service-autorun")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-crash-reporter")
    options.add_argument("--no-zygote")
    options.add_argument("--disable-infobars")
    # options.add_argument("--single-process")
    options.add_argument("--remote-debugging-pipe")
    options.add_argument("--enable-automation") 
    options.add_argument("--enable-unsafe-swiftshader") 

    selected_extensions = random.sample(extension_files, random.randint(2, 4))
    if 'uBlockOrigin.crx' in extension_files and 'uBlockOrigin.crx' not in selected_extensions:
        selected_extensions.append('uBlockOrigin.crx')
    for extension_path in selected_extensions:
        options.add_extension(os.path.join(extensions_dir, extension_path))
        logger.info(f"Extension installed: {extension_path}")


    # # Custom chromedriver path on windows
    if open_gui:
        service = Service(executable_path='./driver/chromedriver.exe')
        driver = webdriver.Chrome(options=options, service=service)
    else:
        driver = webdriver.Chrome(options=options)

    # Bypassing automation detection
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    try:
        driver.get("https://api.ipify.org")  
        ip_address = driver.find_element("tag name", "body").text
        logger.info(f"Current IP address: {ip_address}")
    except Exception as e:
        logger.error(f"Error while getting IP address: {e}")

    # Load site and add history
    simulate_browsing(driver, random.randint(5, 8))
    # simulate_browsing(driver, random.randint(2, 4), True)

    for handle in driver.window_handles[2:]:
        driver.switch_to.window(handle)
        time.sleep(1)
        driver.close()
    driver.switch_to.window(driver.window_handles[1])
    
    logger.info(f"Chromedriver session {driver.session_id} has been created with UA {user_agent} and proxy {proxy}")
    return driver