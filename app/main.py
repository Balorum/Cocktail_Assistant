import streamlit as st
from services.gemini_llm import get_gemini_response, generate_prompt
from services.get_recommendations import get_recommendations

st.title('Cocktail recommendation chatbot🍸')

st.text_input("Enter your query", key="question")
top_matches = st.slider("Select number of top matches", 1, 10, 5)

pinecone_results = get_recommendations(st.session_state.question, top_k=top_matches)

st.write(pinecone_results)

promt = generate_prompt(st.session_state.question, pinecone_results)

response = get_gemini_response(promt)

st.write(response.text)

# df = pd.read_csv("data/raw/final_cocktails.csv")
#
#
# st.dataframe(df[["name", "ingredients", "instructions",  "glassType", "category", "alcoholic"]], use_container_width=False)