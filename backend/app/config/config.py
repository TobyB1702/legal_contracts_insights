import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv("../../../.env"))

class API:
    HOST = os.getenv("API_HOST")
    PORT = os.getenv("API_PORT")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Default value if not found

class MongoDB:
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = os.getenv("MONGO_PORT", "27017")
    MONGO_DB = os.getenv("MONGO_DB")
    MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
    # Construct the MongoDB connection string
    MONGO_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"

class Config:
    API = API
    MONGODB = MongoDB