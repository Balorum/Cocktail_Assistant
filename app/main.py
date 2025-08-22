import streamlit as st
import pandas as pd
from google import genai
import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

client = genai.Client(api_key=GEMINI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)

st.title('Cocktail recommendation chatbot🍸')

index = pc.Index("cocktail-embedding-system")

st.text_input("Enter your query", key="question")

results = index.search(
    namespace="cocktails-embeddings-namespace",
    query={
        "inputs": {"text": st.session_state.question},
        "top_k": 5
    },
    fields=["name", "text", "ingredients", "instructions", "glassType", "alcoholic"]
)

st.write(results)

request = (f"The user entered the following query: {st.session_state.question}. "
           f"The database contains information about such cocktails and information about them: {results}"
           f"Based on this data, display the answer to the user's request.")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=request
)

st.write(response.text)

df = pd.read_csv("data/raw/final_cocktails.csv")


st.dataframe(df[["name", "ingredients", "instructions",  "glassType", "category", "alcoholic"]], use_container_width=False)