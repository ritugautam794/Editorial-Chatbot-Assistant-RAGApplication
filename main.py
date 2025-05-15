import streamlit as st
from src.data_loader import load_and_split_documents
from src.vector_store import get_vector_store
from src.rag_pipeline import build_qa_chain
from src.prompts import format_headline_prompt, format_summary_prompt

@st.cache_resource
def setup():
    docs = load_and_split_documents()
    vs = get_vector_store(docs)
    return build_qa_chain(vs)

st.title("📰 CBC Editorial Assistant Chatbot")
qa_chain = setup()

query_type = st.selectbox("Choose a task", ["Editorial FAQ", "Headline Suggestion", "Tweet Summary"])
query_input = st.text_area("Enter your query or article content")

if st.button("Submit"):
    if query_type == "Headline Suggestion":
        prompt = format_headline_prompt(query_input)
    elif query_type == "Tweet Summary":
        prompt = format_summary_prompt(query_input)
    else:
        prompt = query_input

    result = qa_chain(prompt)
    st.markdown("### 📢 Response")
    st.write(result["result"])

    st.markdown("### 📄 Sources")
    for doc in result["source_documents"]:
        st.write(f"• Source: {doc.metadata.get('source', 'Unknown')}")
