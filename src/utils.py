# src/utils.py

import json, re

def get_article_by_id(articles, content_id):
    for article in articles:
        if str(article.get("content_id")) == str(content_id):
            return article
    return "Article not found for the given content_id."


def get_headline_by_id(raw_news, content_id):
    for doc in raw_news:
        if isinstance(doc.page_content, dict) and doc.page_content.get("content_id") == content_id:
            return doc.page_content.get("content_headline", "Headline not available.")
    return "Headline not found for the given content_id."

def clean_llm_output(text):
    # Remove repeated instructions or prompt artifacts
    text = re.sub(r"Respond in 3-5.*?guidelines'?", '', text, flags=re.IGNORECASE)
    text = re.sub(r"###.*?Guidelines.*?\n", '', text, flags=re.IGNORECASE)
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
