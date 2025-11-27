from django.shortcuts import render

import os
from dotenv import load_dotenv
from langchain_voyageai.embeddings import VoyageAIEmbeddings
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch

from langchain_voyageai import VoyageAIEmbeddings
from pymongo import MongoClient

load_dotenv()

def search_holiday_movies(request):

    query = request.GET.get("q", "")
    results = []

    if query:
        # use API keys
        voyage_api_key = os.getenv("VOYAGE_API_KEY")
        connection_string = os.getenv("MONGO_URI") 

        # Check if environment variables are loaded
        assert voyage_api_key, "ERROR: VOYAGE_API_KEY not found in .env file"
        assert connection_string, "ERROR: MONGO_URI not found in .env file"

        # This is the embedding object.
        embeddings = VoyageAIEmbeddings(
            voyage_api_key=voyage_api_key,
            model="voyage-3-lite"
        )

        # specify our database and collection
        client = MongoClient(os.getenv("MONGO_URI"))
        database = client["festive_flix_db"]
        collection = database["holiday_movies_collection"]

        # vector store with the embeddings model
        vector_store = MongoDBAtlasVectorSearch(
            collection=collection,
            embedding_key="embedding",
            index_name="vector_index",
            text_key="plot",
            embedding=embeddings
        )

        # Similarity search with the user's actual query
        print(f"\nSearching for: '{query}'")

        try:
            # LangChain handles embedding the query
            search_results = vector_store.similarity_search_with_score(query, k=3)
            print(f"Found {len(search_results)} results")
            
            # Format results for the template
            results = []
            for doc, score in search_results:
                result = {
                    'title': doc.metadata.get("title", "Unknown"),
                    'plot': doc.page_content,
                    'runtime': doc.metadata.get("runtime", "Unknown"),
                    'genres': doc.metadata.get("genres", []),
                    'released': doc.metadata.get("released", "Unknown"),
                    'awards': doc.metadata.get("awards", {}),
                    'score': score
                }
                results.append(result)
            
        except Exception as e:
            print(f"Error occurred: {e}")
            results = []

        # Print output to console
        if results:
            print(f"\n=== Search Results for '{query}' ===")
            for i, result in enumerate(results, 1):
                print(f"\nResult {i} (Score: {result['score']:.4f}):")
                print(f"Title: {result['title']}")
                print(f"Plot: {result['plot'][:100]}...")
                print("-" * 50)
        else:
            print(f"No results found for query: '{query}'")

    return render(request, "search_results.html", {"results": results, "query": query})
