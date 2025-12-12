import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# get the environment variable and connect
connection_string = os.getenv("MONGODB_URI")
client = MongoClient(connection_string, appname="devrel.content.django_rag")

# specify the database and collection
database = client["festive_flix_db"]
collection = database["holiday_movies_collection"]

# load json file with embeddings
with open("embeddings_holiday_movies.json", "r") as file:
   data = json.load(file)

if isinstance(data,dict) and "movies" in data:
   movies = data["movies"]

# Clear existing collection and insert new data with embeddings
collection.delete_many({})

# use insert_many to insert multiple documents
result = collection.insert_many(movies)
print(f"Successfully inserted {len(result.inserted_ids)} documents")