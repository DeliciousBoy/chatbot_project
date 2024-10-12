from pathlib import Path

import pandas as pd
from loguru import logger

from src.config import RAW_DATA_DIR
from src.chatbot.text_vectorizer import Embedding
from src.chatbot.similarity_finder import TextSimilarityFinder

def load_data(file_path: str | Path) -> pd.DataFrame:
    """ 
     Loads CSV data from the provided file path.
    
    - param file_path: Path to the CSV file
    - return: DataFrame containing the loaded data or None if an error occurs
    
    """
    try:
        df = pd.read_csv(file_path)
        logger.info(f'Data loaded successfully from {file_path}')
        return df
    except FileNotFoundError:
        logger.error(f'File {file_path} not found')
        return None
    except pd.errors.EmptyDataError:
        logger.error(f"File {file_path} is empty.")
        return None
    except Exception as e:
        logger.error(f"An error occurred while loading the file: {e}")
        return None
    
def main() -> None:
    file_path = RAW_DATA_DIR / "product_report_1.csv"
    df = load_data(file_path)
    
    if df is not None:
        try:
            df.dropna(inplace=True)
            df['combined_text'] = df[['Name']].fillna('').astype(str).agg(' '.join, axis=1)
        except KeyError:
            logger.error('Required column "Name" is missing from the dataframe')
            exit(1)
            
        # Create Embedding    
        embedding_handler = Embedding()
        embedding = embedding_handler.vectorize_text_data(df, 'combined_text')
        
        # Creatae Similarity Finder
        similarity = TextSimilarityFinder(embedding, embedding_handler.vectorizer)
        
        query = 'เคอปเปอร์'
        if not query:
            logger.error("Query is empty. Please provide a valid query.")
            exit(1)
        
        best_match = similarity.find_most_similar(query, df)
        if best_match is not None:
            print(best_match['Name'])
        else:
            logger.error("No match found for the query.")
    else:
        logger.error("Data loading failed, program terminated.")
    
        
if __name__ == "__main__":
    main()