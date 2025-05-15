def format_headline_prompt(article_text):
    return f"Suggest an SEO-optimized headline for this article:\n\n{article_text}"

def format_summary_prompt(article_text):
    return f"Summarize this article in one tweet-style sentence:\n\n{article_text}"
