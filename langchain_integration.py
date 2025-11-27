from langchain_voyageai import VoyageAIEmbeddings
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

voyage_api_key = os.getenv("VOYAGE_API_KEY")
connection_string = os.getenv("MONGO_URI")

# Check if environment variables are loaded
assert voyage_api_key, "ERROR: VOYAGE_API_KEY not found in .env file"
assert connection_string, "ERROR: MONGODB_URI not found in .env file"


# Connect to the Atlas cluster
try:
    client = MongoClient(os.getenv("MONGO_URI"))
    
    collection = client["festive_flix_db"]["holiday_movies_collection"]

except Exception as e:
    print(f"ERROR: Failed to connect to MongoDB: {e}")
    exit(1)

embedding = VoyageAIEmbeddings(
    voyage_api_key=os.getenv("VOYAGE_API_KEY"), 
    model="voyage-3-lite"
)

# Instantiate the vector store with proper LangChain configuration
vector_store = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=embedding,
    index_name="vector_index",
    text_key="plot",
    embedding_key="embedding"
)

# Similarity search
query = "Santa Claus"
print(f"\nSearching for: '{query}'")

try:
    # LangChain  handles embedding the query
    results = vector_store.similarity_search_with_score(query, k=3)
    print(f"Found {len(results)} results")
    
except Exception as e:
    print(f"Error occurred: {e}")
    results = []

# Display results
if results:
    print("\n=== Search Results for the query ===")
    for i, (doc, score) in enumerate(results, 1):
        # Extract metadata from the document
        title = doc.metadata.get("title", "Unknown")
        runtime = doc.metadata.get("runtime", "Unknown")
        genres = doc.metadata.get("genres", [])
        released = doc.metadata.get("released", "Unknown")
        awards = doc.metadata.get("awards", {})
        plot = doc.page_content

        print(f"\nResult {i} (Score: {score:.4f}):")
        print(f"Title: {title}")
        print(f"Plot: {plot}")
        print(f"Runtime: {runtime} minutes")
        print(f"Genres: {', '.join(genres) if isinstance(genres, list) else genres}")
        print(f"Released: {released[:4] if released != 'Unknown' else 'Unknown'}")
        
        if awards and awards.get("text"):
            print(f"Awards: {awards['text']}")
        print("-" * 50)
else:
    print("No results found.")