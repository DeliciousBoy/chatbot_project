import os
from pathlib import Path

import pandas as pd
from loguru import logger

from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR


def clean_file(file_path: Path | str) -> pd.DataFrame:
    """ Read a CSV file and clean the data """
    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        logger.error(f'DataFrame is empty: {file_path}')
        return pd.DataFrame()
        
    if df.empty:
        return pd.DataFrame()
    
    # Drop rows with missing essential values
    df = df.dropna(subset=['name', 'id'])
    
    # Validate each column based on the specific conditions 
    if {'size', 'id', 'price'}.issubset(df.columns):
        df = df[df.apply(lambda row: (
            isinstance(row['id'], (str, int)) and str(row['id']).isdigit() and  
            isinstance(row['price'], str) and row['price'].endswith('บาท') and  
            isinstance(row['size'], str) and row['size'].endswith('ซม.') and
            (pd.isna(row['weight']) or (isinstance(row['weight'], str) and row['weight'].endswith('กก.')))
        ), axis=1)]

    return df

def extract_category_name(file_path: Path | str) -> str:
    """ Extract the category name from the file stem """
    return file_path.stem.split('_')[0]

def categorize_files(raw_dir: Path | str) -> dict[str, list[pd.DataFrame]]:
    """ Categorize DataFrames by file category """
    category_data = {}
    for raw_file in raw_dir.glob('*.csv'):
        if raw_file.stat().st_size == 0:
            continue
        
        df = clean_file(raw_file)
        if df.empty:
            continue
        
        category = extract_category_name(raw_file)
        
        if category not in category_data:
            category_data[category] = [df]
        else:
            category_data[category].append(df)
            
    return category_data

def update_product(category_data: dict[str, list[pd.DataFrame]], processed_dir: Path | str) -> None:
    """ Combined and save categorized DataFrames """
    for category, df in category_data.items():
        combined_df = pd.concat(df, ignore_index=True).drop_duplicates()
        processed_file = processed_dir / f'{category}.csv'
        combined_df.to_csv(processed_file, index=False, encoding='utf-8-sig')
        

def main() -> None:
    category_data = categorize_files(RAW_DATA_DIR)
    update_product(category_data, PROCESSED_DATA_DIR) 
    
    flag_file_path = "/app/data/raw/scraping_done.flag"
    if os.path.exists(flag_file_path):
        os.remove(flag_file_path)
        
if __name__ == "__main__":
    main()