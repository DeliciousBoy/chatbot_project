import pandas as pd
from loguru import logger
from sklearn.feature_extraction.text import TfidfVectorizer
from pythainlp.tokenize import word_tokenize

class Embedding:
    def __init__(self, vectorizer=None):
        """ 
        Initializes the Embedding class with vectorizer
        
        - param vectorizer: Vectorizer instance, default is TfidfVectorizer
        """
        self.vectorizer = vectorizer if vectorizer else TfidfVectorizer()
        
    def vectorize_text_data(self, dataframe: pd.DataFrame, text_column: str):
        """ 
         Vectorizes the text data in a specific column of the dataframe.
        
        - param dataframe: Pandas DataFrame containing the data
        - param text_column: The column name containing the text data
        - return: Embedding generated from the text data
        """
        try:
            
            if text_column not in dataframe.columns:
                raise ValueError(f'Column "{text_column}" not found in the DataFrame')
            
            if dataframe.empty:
                raise ValueError(f'The input dataframe is empty')
            
            
            text_data = dataframe[text_column].astype(str).apply(lambda x: ' '.join(word_tokenize(x)))
            # text_data = dataframe[text_column].astype(str).tolist()
            
            if text_data.empty:
                raise ValueError(f'No text data found in column "{text_column}"')
            
            embeddings = self.vectorizer.fit_transform(text_data)
        
            return embeddings
        except ValueError as ve:
            logger.error(f"ValueError: {ve}")
            return None
        except Exception as e:
            logger.error(f"Error: {e}")
            return None