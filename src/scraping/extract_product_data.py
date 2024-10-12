from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from loguru import logger

from src.scraping.config_loader import ProductElements

def safe_find_element(driver: WebDriver, by: By, value: str) -> str:
    try:
        return driver.find_element(by, value).text
    except NoSuchElementException:
        logger.warning(f'Element not found: {value}')
        return 'N/A'


def extract_product_data(driver: WebDriver, elements: ProductElements) -> ProductElements:
    """
    Extract product data from a webpage.

    Parameters:
        driver: The selenium WebDriver instance.
        elements: An instance of ProductElements dataclass containing XPATH and CLSS_NAME seletors.

    Return:
        A tuple containing the product's name, id, size, weight, price, and unit   
    """
    name = safe_find_element(driver, By.CLASS_NAME, elements.name)
    id = safe_find_element(driver, By.CLASS_NAME, elements.id)
    price = safe_find_element(driver, By.CLASS_NAME, elements.price)
    unit = safe_find_element(driver, By.CLASS_NAME, elements.unit)
    size = safe_find_element(driver, By.XPATH, elements.size)
    weight = safe_find_element(driver, By.XPATH, elements.weight)
    
    return ProductElements(
        name=name, 
        id=id, 
        price=price, 
        unit=unit,
        size=size, 
        weight=weight, 
    )



