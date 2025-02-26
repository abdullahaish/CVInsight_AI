import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DB_NAME = os.getenv("DB_NAME", "cv_analysis")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "cvs")

# Initialize MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
cvs_collection = db[COLLECTION_NAME]
