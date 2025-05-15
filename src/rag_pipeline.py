from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

def build_qa_chain(vector_store):
    llm_pipeline = pipeline("text2text-generation", model="google/flan-t5-large", temperature=0.3)
    llm = HuggingFacePipeline(pipeline=llm_pipeline)

    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain
