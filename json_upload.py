import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

#Pick up MONGO_URI envvar from .env file and connect
connection_string = os.getenv("MONGO_URI")
connect = MongoClient(connection_string)

# specify our database and collection
database = connect["festive_flix_db"]
collection = database["holiday_movies_collection"]


# load in our json file with embeddings
with open("embedded_holiday_movies.json", "r") as file:
   data = json.load(file)

if isinstance(data,dict) and "movies" in data:
   movies = data["movies"]

# Clear existing collection and insert new data with embeddings
collection.delete_many({})

# use insert_many to insert multiple documents
result = collection.insert_many(movies)
print(f"Successfully inserted {len(result.inserted_ids)} documents")