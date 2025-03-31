from pymongo import MongoClient
from typing import List
from database.mongo_engine import MongoDBConnection

class RelevantChunksCollector:
    def __init__(self):
        """
        Initialize the RelevantChunksCollector with a MongoDB connection.
        """
        self.mongo_client = MongoDBConnection()
        self.mongo_client.connect()
        self.collection = self.mongo_client.get_database()[self.mongo_client.mongo_collection]
        
    def retrieve_relevant_chunks(self, query: str, top_k: int = 5) -> List[dict]:
        """
        Retrieve relevant chunks from the MongoDB collection based on the query.
            
        Parameters:
        query (str): The query to search for in the chunks. Can include multiple terms separated by spaces.
        top_k (int): The number of top relevant chunks to retrieve.
            
        Returns:
        List[dict]: A list of relevant chunks containing the query terms.
        """
            
        try:
            #Split the query into individual terms
            terms = query.split()
            # Build a MongoDB query to match any of the terms
            search_query = {"$or": [{"content": {"$regex": term, "$options": "i"}} for term in terms]}
            # Retrieve and sort chunks by cosine similarity in descending order, limit to top_k
            results = (
                self.collection.find(search_query)
                    .sort("cosine_similarity_to_query", -1)  # Sort by cosine similarity (descending)
                    .limit(top_k)  # Limit to top_k results
                    )
            # Convert results to a list
            relevant_chunks = [
            {"filename": chunk.get("filename", "N/A"), "content": chunk.get("content", "N/A")}
            for chunk in results]
                
            print(f"Found {len(relevant_chunks)} relevant chunks for query: '{query}'")
            return relevant_chunks
            
        except Exception as e:
            print(f"Error retrieving relevant chunks: {e}")
            return []

    def close_connection(self):
        """
        Close the MongoDB connection.
        """
        self.mongo_client.close()