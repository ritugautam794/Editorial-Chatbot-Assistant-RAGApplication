from langchain_community.document_loaders import JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split_documents():
    loader1 = JSONLoader(file_path="data/cbc_guidelines.json", jq_schema=".[]", text_content=False)
    loader2 = JSONLoader(file_path="data/news-dataset.json", jq_schema=".[]", text_content=False)

    raw_guidelines = loader1.load()
    raw_news = loader2.load()

    docs = []
    for doc in raw_guidelines + raw_news:
        if isinstance(doc.page_content, dict):
            doc.page_content = str(doc.page_content)
        docs.append(doc)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    split_docs = splitter.split_documents(docs)

    return split_docs, raw_news  # Return split docs for vectorstore, raw news for lookup/tweet

