import numpy as np
import pandas as pd
from loguru import logger
from scipy.spatial.distance import cdist
from sklearn.feature_extraction.text import TfidfVectorizer


class TextSimilarityFinder:
    def __init__(self, embedding_matrix: np.ndarray, vectorizer: TfidfVectorizer):
        """  
        Initilaizes SimilarityFinder with embedding matrix and vectorizer.
        
        """
        
        if embedding_matrix is None or embedding_matrix.size == 0:
            raise ValueError("Embedding matrix must not be empty")
        
        self.embedding_matrix = embedding_matrix
        self.vectorizer = vectorizer
        
    
    def vectorize_query(self, query: str) -> np.ndarray:
        """ 
         Vectorizes the query text using the vectorizer.

         
        - param query: the text query to be  vectorized
        - return: The vector representation of the query
        """
        if not query:
            raise ValueError("Query text must not be empty")
        
        try:
            return self.vectorizer.transform([query]).toarray()
        except ValueError as ve:
            logger.error(f'Error vectorizing query: {query}. Error: {ve}')
            raise
            
    def find_most_similar(self, query: str, dataframe: pd.DataFrame):
        """ 
        Finds the most similar text in the DataFrame to the provied query
        
        - param query: The text query to match
        - param dataframe: DataFrame containing the data to compare against
        - return: The row in the DataFrame that best macthes the query
        """
        if dataframe.empty:
            raise ValueError("Input dataframe must not be empty")
        
        try:
            query_embedding = self.vectorize_query(query)
            similarites = 1 - cdist(query_embedding,
                                    self.embedding_matrix.toarray(),
                                    metric='cosine')
            idx = np.argmax(similarites)
            return dataframe.iloc[idx]
        except Exception as ve:
            logger.error(f"ValueError: {ve} occurred with query: {query}")
            return None
        
        except Exception as e:
            logger.error(f"Error: {e} occurred with query: {query}")
            return None
        