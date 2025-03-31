from pymongo import MongoClient
from config.config import Config
import os

class MongoDBConnection:
    def __init__(self):
        """
        Initialize the MongoDB connection using environment variables.
        """

        # Get MongoDB connection details from environment variables
        self.mongo_host = Config.MONGODB.MONGO_HOST
        self.mongo_port = Config.MONGODB.MONGO_PORT
        self.mongo_db = Config.MONGODB.MONGO_DB
        self.mongo_collection = Config.MONGODB.MONGO_COLLECTION
        self.mongo_url = f"mongodb://{self.mongo_host}:{self.mongo_port}/"

        # Initialize the client
        self.client = None

    def connect(self):
        """
        Establish a connection to MongoDB.
        """
        try:
            print(f"Connecting to MongoDB at: {self.mongo_url}")
            self.client = MongoClient(self.mongo_url)
            print("MongoDB connection established.")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def get_database(self):
        """
        Get the specified database.

        Returns:
        Database: The MongoDB database instance.
        """
        if not self.client:
            raise Exception("MongoDB client is not connected. Call connect() first.")
        return self.client[self.mongo_db]
    
    def load_all_data(self):
        """
        Load all data from the specified MongoDB collection.

        Returns:
        list: A list of all documents in the collection.
        """        
        if not self.client:
            raise Exception("MongoDB client is not connected. Call connect() first.")
        db = self.get_database()
        collection = db[self.mongo_collection]
        return list(collection.find())    

    def close(self):
        """
        Close the MongoDB connection.
        """
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")