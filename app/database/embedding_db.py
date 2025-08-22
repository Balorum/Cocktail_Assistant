from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

print(API_KEY)

pc = Pinecone(api_key=API_KEY)


index = pc.Index("cocktail-embedding-system")

print(index.describe_index_stats())