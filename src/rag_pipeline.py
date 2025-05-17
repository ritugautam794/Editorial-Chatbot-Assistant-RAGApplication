from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from transformers import AutoTokenizer, pipeline

def generate_seo_headline(prompt: str) -> str:
    headline_pipeline = pipeline(
        "text2text-generation",
        model="Michau/t5-base-en-generate-headline",
        tokenizer=AutoTokenizer.from_pretrained("Michau/t5-base-en-generate-headline"),  # Explicit tokenizer
        max_length=32,
        temperature=0.4
    )
    return headline_pipeline(prompt)[0]['generated_text']

def build_qa_chain(vector_store):
    llm_pipeline = pipeline("text2text-generation", model="google/flan-t5-small", temperature=0.3, device=-1)
    llm = HuggingFacePipeline(pipeline=llm_pipeline)

    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain

def call_llm_directly(prompt: str) -> str:
    summarizer = pipeline(
        "text2text-generation",
        model="t5-small",  # options: "t5-small", "t5-base", "t5-large"
        max_length=80,     # shorter for tweet-style
        temperature=0.3,
        device=-1,
        repetition_penalty=1.1
        
    )
    llm = HuggingFacePipeline(pipeline=summarizer)
    return llm.predict(prompt)


# Add to src/rag_pipeline.py

def generate_seo_headline(headline: str) -> str:
    headline_pipeline = pipeline(
        "text2text-generation",
        model="Michau/t5-base-en-generate-headline",
        tokenizer=AutoTokenizer.from_pretrained("Michau/t5-base-en-generate-headline"),
        max_length=32,
        temperature=0.4
    )
    # The model expects the article text, but if you only have the headline, use it directly
    return headline_pipeline(headline)[0]['generated_text']

