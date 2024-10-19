import os
from pathlib import Path

import pandas as pd
from loguru import logger

from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR


def clean_data(raw_dir: Path | str) -> pd.DataFrame:
    category_data = {}
    
    for raw_file in raw_dir.glob("*.csv"):
        if raw_file.stat().st_size == 0:
            continue
        
        try:
            df = pd.read_csv(raw_file)
        except pd.errors.EmptyDataError:
            logger.error(f'DataFrame is empty')
            continue
        
        df = df.dropna(subset=['name', 'id'])
        
        if df.empty:
            continue
        
        category = raw_file.stem.split('_')[0]
        
        if category not in category_data:
            category_data[category] = [df]
        else:
            category_data[category].append(df)
    
    for category, df_list in category_data.items():
        combined_df = pd.concat(df_list, ignore_index=True).drop_duplicates()
        processed_file_path = PROCESSED_DATA_DIR / f'{category}.csv'
        combined_df.to_csv(processed_file_path, index=False, encoding='utf-8-sig')
        
 
    
def update_product():
    ...

def main():
    
    clean_data(raw_dir=RAW_DATA_DIR)

if __name__ == "__main__":
    main()