from loguru import logger
from selenium.webdriver.remote.webdriver import WebDriver

from src.scraping.config_loader import ProductElements
from src.scraping.extract_product_data import extract_product_data


def scrape_product_data(driver: WebDriver, product_links: list[str], elements: ProductElements) -> list[str]:
    """
    Scrape product data from a list of product links.

    Parameters:
        - driver: The selenium WebDriver instance.
        - product_links : A list of URLs pointing to the product pages.
        - elements: An instance of ProductElements dataclass containing XPATH and CLASS_NAME selectors.

    Return:
        A list of product data
    """

    product_data_list = []

    for link in product_links:
        driver.get(link)
        product_data = extract_product_data(driver=driver, elements=elements)
        product_data_list.append(product_data)
    return product_data_list