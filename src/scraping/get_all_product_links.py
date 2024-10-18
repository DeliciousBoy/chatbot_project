from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from src.scraping.config_loader import ScraperSelector

def get_all_product_links(driver: WebDriver, selector: ScraperSelector) -> list[str]:
    """
    Extract all product links from the main page.

    Parameters:
        - driver  The WebDriver instance use to control the browser.
        - selector  The ScraperSelector object containing the necessary CLASS_NAME and XPATH selectors.
    
    Return:
        - A list of product URLs found on the page.
    """

    try:   
        grid_element = driver.find_element(By.CLASS_NAME, selector.container_class)
        product_elements: list[WebElement] = grid_element.find_elements(By.CLASS_NAME, selector.item_class)
        links = [product_element.find_element(By.XPATH, selector.link_path).get_attribute('href')
                for product_element in product_elements]
        return links

    except (NoSuchElementException, TimeoutException) as e:
        # logger.error(f'An error occurred while trying to find elements: {e}')
        return []
    

