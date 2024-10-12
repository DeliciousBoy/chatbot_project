import pandas as pd
from src.scraping.config_loader import ProductElements

def save_product_data_to_csv(product_data_list: list[ProductElements], output_path: str) -> None:
    """
    Save the scraped product data to a CSV file.

    Parameters:
        - product_data_list: A list of ProductElements dataclass instances containing the scraped product data.
        - output_path: The path where the CSV file will be saved.
    """
    # Convert the list of ProductElements into a list of dictionaries
    data = [
        {
            'Name': product.name,
            'ID': product.id,
            'Price': product.price,
            'Unit': product.unit,
            'Size': product.size,
            'Weight': product.weight
        }
        for product in product_data_list
    ]
    
    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(data)
    
    # Save the DataFrame to a CSV file
    df.to_csv(output_path, index=False, encoding='utf-8-sig')                                                                                                                                                      