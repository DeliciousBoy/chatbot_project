import time

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

product_list = "ProductListing_productItemWrapper__1AXaV"

def scroll_down(driver, max_scroll_attempts=5, scroll_increment=500 ,sleep_time=2, scale_factor=0.5):
    # Decrease a window scale
    driver.execute_script(f"document.body.style.transform='scale({scale_factor})'; document.body.style.transformOrigin='0 0';")

    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_attempt = 0
    
    previous_product_count = len(driver.find_elements(By.CLASS_NAME, product_list))
    
    while scroll_attempt < max_scroll_attempts:
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        for scroll_position in range(0, last_height, scroll_increment):
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            time.sleep(sleep_time)
            
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, product_list))
            )
        except TimeoutException:
            # logger.warning("Timeout waiting for products to load")
            scroll_attempt += 1
            continue
        
        time.sleep(sleep_time)  
        
        current_product_count = len(driver.find_elements(By.CLASS_NAME, product_list))
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height  == last_height and current_product_count == previous_product_count:
            break
        
        last_height = new_height
        previous_product_count = current_product_count
        scroll_attempt = 0
    
        