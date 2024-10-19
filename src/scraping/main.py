from src.scraping.setup_driver import setup_driver
from src.scraping.config_loader import load_config
from src.scraping.scroll_down import scroll_down
from src.scraping.get_all_product_links import get_all_product_links
from src.scraping.config_loader import load_config
from src.scraping.product_scraper import scrape_product_data
from src.scraping.save_to_csv import save_product_data_to_csv
from src.config import RAW_DATA_DIR
from src.utils.logging_config import logger

def main() -> None:  
   driver, wait = setup_driver()
   try:
      
      all_categories_config = load_config(config_path='config.yaml')
      
      for category_name, (selector, category_config) in all_categories_config.items():   
         driver.get(category_config.web_url)
         scroll_down(driver)
         product_links = get_all_product_links(driver=driver, selector=selector)
         product_data_list = scrape_product_data(driver=driver, product_links=product_links, 
                                                elements=category_config.product_elements)
         save_product_data_to_csv(product_data_list, output_dir=RAW_DATA_DIR, 
                                 category_name=category_name)
         logger.success(f"Scraping completed for category: {category_name:<20}| "
                        f"Total products scraped: {len(product_data_list):<10}")
   finally:
      
      with open("/app/data/raw/scraping_done.flag", "w") as f:
         f.write("Scraping Completed\n")
         
      driver.quit()
      
if __name__ == "__main__":
    main()