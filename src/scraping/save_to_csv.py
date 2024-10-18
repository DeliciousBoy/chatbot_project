import shutil
from  pathlib import Path
from datetime import datetime

import pandas as pd


from src.scraping.config_loader import ProductElements

def save_product_data_to_csv(product_data_list: list[ProductElements], output_dir: str, category_name: str) -> None:
    """
    Save the scraped product data to a CSV file.
    Parameters:
        - product_data_list: A list of ProductElements dataclass instances containing the scraped product data.
        - output_dir: The path where the CSV file will be saved.
    """
    # Create a timestamped filename to avoid overwriting previous files
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    output_dir_path = Path(output_dir)
    
    # Ensure output directory exists
    output_dir_path.mkdir(parents=True, exist_ok=True)

    output_path = output_dir_path / f"{category_name}_product_data_{timestamp}.csv"
    
    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(product_data_list)
    
    # Save the DataFrame to a CSV file
    df.to_csv(output_path, index=False, encoding='utf-8-sig')                                                                                                                                                      
    