from typing import Optional, Tuple

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from loguru import logger

def setup_driver(headless: bool = True) -> Tuple[Optional[WebDriver], Optional[WebDriverWait]]:
    """
    Set up and configure the Chrome WebDriver.

    Parameters:
        headless (bool): If True, runs Chrom in headless mode (without a GUI).

    Returns:
        Tuple[Optional[webdriver.Chrome], Optional[WebDriverWait]]:
            - A tuple containing the Chrome WebDriver instance and WebDriverWait object if 
              setup is successful.
            - Returns (None, None) if there is an error during setup.
    """

    options = Options()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')  # Required for Docker
        options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
        options.add_argument('--disable-software-rasterizer')  # Disable software rendering
        options.add_argument('--remote-debugging-port=9222')  # For debugging in headless mode
        
    try:
        driver = webdriver.Chrome(options=options)
        # driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        # logger.info('Chrome driver setup successfully.')
        return driver, wait
    
    except WebDriverException as e:
        logger.error(f'WebDriverException encountered: {e}')
        return None, None
    
    except TimeoutException as e:
        logger.error(f'TimeoutException encountered: {e}')
        return None, None
    
    except Exception as e:
        logger.error(f'An unexpected error occurred: {e}')
        return None, None