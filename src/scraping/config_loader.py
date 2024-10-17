from pathlib import Path
from dataclasses import dataclass
from typing import Union, Tuple, Optional

import yaml
from loguru import logger

@dataclass
class ScraperSelector:
    """ Dataclass for storing Classname and XPATH selectors for scraping."""
    container_class: str
    item_class: str
    link_path: str

@dataclass
class ProductElements:
    """ Dataclass for storing product element selectors."""
    name: str
    id: str
    price: str
    unit: str
    size: Optional[str] = None
    weight: Optional[str] = None

@dataclass
class CategoryConfig:
    """ Dataclass for storing catergory specific configuration."""
    product_elements: ProductElements
    web_url: str

def load_config(config_path: Union[str, Path]) -> dict:
    """
    Load the YAML configuration file and return a config object.
    """
    logger.info(f'Loading config from {config_path}')

    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            # logger.info(f'YAML content: {config}')

        # Prepare a dictionary to store all category configurations
        all_categories_config = {}
        
        for category_name, category_data in config['categories'].items():
            # logger.info(f"Loading configuration for category: {category_name}")
            
            required_keys = ['name', 'id', 'price', 'unit', 'web_url']
            missing_keys = [key for key in required_keys if key not in category_data]

            if missing_keys:
                # logger.warning(f"Category {category_name} is missing the following keys: {missing_keys}. Skipping this category.")
                continue
            
            selector = ScraperSelector(
                container_class=config['product_grid_selector']['container_class'],
                item_class=config['product_grid_selector']['item_class'],
                link_path=config['product_grid_selector']['link_path'],
            )

            category_config = CategoryConfig(
                product_elements=ProductElements(
                    name=category_data['name'],
                    id=category_data['id'],
                    price=category_data.get('price'),
                    unit=category_data.get('unit'),
                    size=category_data.get('size'),
                    weight=category_data.get('weight'),
                ),
                web_url=category_data['web_url']
                
            )
            # logger.info(f'Successfully loaded configuration for category {category}')
            all_categories_config[category_name] = (selector, category_config)
        return all_categories_config

    except FileNotFoundError:
        logger.error(f'Error: the file {config_path} was not found')
        raise

    except yaml.YAMLError as e:
        logger.error(f'Error parsing YAML file: {e}')
        raise
    
    except ValueError as e:
        logger.error(f'Error: {e}')
        raise

