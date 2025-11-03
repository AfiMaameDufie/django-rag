import json
from dotenv import load_dotenv
import voyageai
import os

load_dotenv()  

# using API key from environment variables in .env file
VOYAGE_API_KEY = os.environ.get("VOYAGE_API_KEY")
print("VOYAGE_API_KEY:", VOYAGE_API_KEY)

vo = voyageai.Client(VOYAGE_API_KEY)

with open("holiday_movies.json", "r") as f:
   data = json.load(f)


# focusing on "plot" field since that's what we are embedding
movies_list = [movie.get("plot", "") for movie in data.get("movies", [])]


# getting embeddings for the plots using "voyage-3-lite"
result = vo.embed(movies_list, model="voyage-3-lite", input_type="document")


# new field to hold the embeddings
for movie, embedding in zip(data.get("movies", []), result.embeddings):
   movie["embedding"] = embedding


# writing embeddings back to a new file
with open("embedded_holiday_movies.json", "w") as f:
   json.dump(data, f, indent=2)