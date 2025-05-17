def format_headline_prompt(article_text):
    return f"Suggest an SEO-optimized headline for this article:\n\n{article_text}"

def format_headline_paraphrase_prompt(original_headline, article_body):
    return (
        f"Paraphrase the following news headline, keeping the meaning the same, "
        f"and make sure it is SEO-friendly and just within 1 sentence and less than 12 words:\n\n"
        f"Original Headline: {original_headline}"    
    )

def format_summary_prompt(article_text):
   return (
        "summarize: "  # required for T5 to know the task
        "Write a concise and engaging tweet-style summary of the following news article (under 280 characters):\n\n"
        f"{article_text}"
    )

def format_editorial_prompt(question, context):
    return (
        "You are an editorial assistant bot.\n\n"
        "Answer the user's question using ONLY the provided editorial guidelines below. "
        "Respond in 3-5 clear, simple English sentences. "
        "If the answer cannot be found, say: 'I could not find a relevant answer in the provided editorial guidelines.'\n\n"
        "### Editorial Guidelines ###\n"
        f"{context}\n"
        "### End Guidelines ###\n"
        f"User Question: {question}\n"
        "### Answer ###\n"
    )
