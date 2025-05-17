import streamlit as st
import warnings, json, re
from src.data_loader import load_and_split_documents
from src.vector_store import get_vector_store
from src.rag_pipeline import build_qa_chain, call_llm_directly,generate_seo_headline
from src.prompts import format_editorial_prompt  # Keep only needed prompts
from src.utils import get_article_by_id,clean_llm_output

warnings.filterwarnings("ignore")

# Load articles only for headline suggestion
with open("data/news-dataset.json", encoding="utf-8") as f:
    articles = json.load(f)

@st.cache_resource
def setup():
    split_docs, raw_news = load_and_split_documents()
    vector_store = get_vector_store(split_docs)
    qa_chain = build_qa_chain(vector_store)
    return qa_chain

st.title("📰 Editorial Assistant Chatbot")
qa_chain = setup()

query_type = st.selectbox("Choose a task", ["Editorial FAQ", "Headline Suggestion", "Tweet Summary"])

# Initialize variables
content_id = None
article_content = None
query_input = None

# Handle different input types
if query_type == "Headline Suggestion":
    content_id = st.text_input("Enter Content ID (from news-dataset.json)")
elif query_type == "Tweet Summary":
    article_content = st.text_area("Paste article content to summarize for Twitter:", height=150)
else:
    query_input = st.text_area("Enter your editorial question")

if st.button("Submit"):
    if query_type == "Headline Suggestion":
        # Existing headline suggestion code
        article = get_article_by_id(articles, content_id)
        if article:
            st.markdown("**Current Headline:**")
            st.write(article["content_headline"])
            suggestion = generate_seo_headline(article["content_headline"])
            st.markdown("**SEO-Optimized Suggestion:**")
            st.write(suggestion.strip())
        else:
            st.error("No article found for this Content ID.")

    elif query_type == "Tweet Summary":
        if article_content:
            # Directly use input text for Twitter summary
            prompt = (
            "Write a tweet-style summary of the following news article in under 280 characters. "
            "Use plain language, include 1-2 relevant hashtags, and make it engaging for Twitter. "
            "Avoid repeating numbers and words. Dont start with special charcters. End with hashtags. Focus on the main event and its significance:\n\n"
            f"{article_content}"
        )
            result = call_llm_directly(prompt)
            st.markdown("### 🐦 Tweet Summary")
            st.write(result.strip())
        else:
            st.error("Please enter article content to summarize.")

    elif query_type == "Editorial FAQ":
        if not query_input.strip():
            st.error("Please enter your editorial question.")
            st.stop()
        retriever = qa_chain.retriever
        docs = retriever.get_relevant_documents(query_input)
        if not docs:
            st.warning("No relevant guidelines found for this query.")
            st.stop()
        # Use only the top chunk for clarity
        context = docs[0].page_content
        prompt = f"Based on the following guideline, answer the user's question:\n\nGuideline: {context}\n\nQuestion: {query_input}\n\nAnswer in 2-3 sentences."
        result = call_llm_directly(prompt)

        clean_result = clean_llm_output(result)
        st.markdown("### 📢 Response")
        st.write(clean_result or "No relevant answer found.")

        # Show source URL
        url = docs[0].metadata.get('url')
        if url:
            st.markdown(f"### 📄 Source\n[Guideline Link]({url})")

        

