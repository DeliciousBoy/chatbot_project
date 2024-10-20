import os
from pathlib import Path

import pandas as pd
import pickle
from loguru import logger
from FlagEmbedding import BGEM3FlagModel

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

def combine_columns(row: pd.DataFrame) -> str:
    """ Combined all relevant columns into a single string with prefixes"""
    return (
            f"ชื่อสินค้า {row['name']} "
            f"รหัสสินค้า {row['id']} "
            f"ราคา {row['price']} "
            f"{row['unit']} "
            f"ขนาด {row['size']} "
            f"น้ำหนัก {row['weight']} "
           )

def update_product(category_data: dict[str, list[pd.DataFrame]], processed_dir: Path | str) -> None:
    """ Combined and save categorized DataFrames """
    all_combined_data = []
    for category, df in category_data.items():
        combined_df = pd.concat(df, ignore_index=True).drop_duplicates()
        processed_file = processed_dir / f'{category}.csv'
        
        # Save the categorized data separately
        combined_df.to_csv(processed_file, index=False, encoding='utf-8-sig')
        
        # Combine each row's relevant columns into a single string
        combined_df['combined_text'] = combined_df.apply(combine_columns, axis=1)
        all_combined_data.append(combined_df['combined_text'])
        
    # Concatenate all combined data into a single DataFrame and save to a file
    final_combined_df = pd.DataFrame({'combined_text': pd.concat(all_combined_data, ignore_index=True)})
    final_combined_file = processed_dir / 'product_data.csv'
    final_combined_df.to_csv(final_combined_file, index=False, encoding='utf-8-sig')
    
def embedding(input_file: Path | str, output_dir: Path | str):
    """  Create embeddings from input CSV file using a specified model and save the embeddings. """
    
    try:
        data = pd.read_csv(input_file, header=None)
        data_list = data[0].tolist() # Convert data to list
    
        embed_model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)
        # Generate embeddings for the data list
        embeddings = embed_model.encode(data_list, batch_size=8, max_length=1200)['dense_vecs']
    
        output_file = output_dir / f"{Path(input_file.stem)}_embeddings.pkl"
        with open(output_file, 'wb') as f:
            pickle.dump(embeddings, f)
    except Exception as e:
        logger.error(f'Error occurred during embedding | {e}')

def main() -> None:
    
    category_data = categorize_files(RAW_DATA_DIR)
    update_product(category_data, PROCESSED_DATA_DIR) 
    embedding(PROCESSED_DATA_DIR / 'product_data.csv', PROCESSED_DATA_DIR)
    
    flag_file_path = "/app/data/raw/scraping_done.flag"
    if os.path.exists(flag_file_path):
        os.remove(flag_file_path)
    

if __name__ == "__main__":
    main()