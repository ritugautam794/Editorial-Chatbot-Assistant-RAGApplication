# CBC Editorial Assistant

An AI-powered chatbot using RAG to support CBC's editorial teams with policy queries, SEO headlines, and social media summaries.

## Features
- Policy Q&A from CBC guidelines
- SEO-optimized headline generation
- Tweet-style article summarization

## Setup Instructions

### 1. Clone Repository
git clone https://github.com/yourusername/cbc-editorial-assistant.git
cd cbc-editorial-assistant

text

### 2. Install Dependencies
python -m venv venv
source venv/bin/activate # Linux/Mac

venv\Scripts\activate # Windows
pip install -r requirements.txt

text

### 3. Data Preparation
Place files in `data/` directory:
- `cbc_guidelines.json`
- `news-dataset.json`

### 4. Initialize Vector Store
python src/embeddings.py

text

### 5. Run Application
streamlit run main.py

text

## Technical Choices

### Vector Store
- **FAISS**: Chosen for efficient similarity search on CPU
- **Embedding Model**: `sentence-transformers/all-mpnet-base-v2`
  - 768d embeddings with strong semantic understanding
  - Balance between accuracy and computational efficiency

### Generative Models
1. **Policy Q&A**: 
   - `google/flan-t5-large`
   - 3B parameter model for comprehensive answers
   - Temperature: 0.2 for factual responses

2. **SEO/Tweet Generation**:
   - `t5-small` (248M parameters)
   - Faster inference for creative tasks
   - Temperature: 0.3-0.5 for varied outputs

### Chunking Strategy
- **Method**: Recursive character text splitting
- **Chunk Size**: 1000 tokens
- **Overlap**: 200 tokens
- Preserves context while maintaining processing efficiency

## Optimization Considerations
1. **Alternative Models**:
   - Commercial: OpenAI's GPT-3.5/4 (better coherence)
   - Specialized: DeBERTa-v3 for policy understanding
   - Lightweight: DistilBERT for faster responses

2. **Hybrid Search**:
   - Combine semantic + keyword search
   - Implement using Weaviate/ElasticSearch

3. **Caching**:
   - Redis for frequent query caching
   - Reduce LLM API costs

## Sample Conversations

### 1. Policy Q&A
**User**: What's CBC's guideline on citing anonymous sources?  
**Assistant**: CBC permits using anonymous sources only when essential information cannot be obtained through identified channels. Journalists must verify credibility, disclose reasons for anonymity to editors, and provide context to audiences. [Source: CBC Source Guidelines]

---

### 2. Headline Suggestion  
**User**: Suggest SEO headline for climate change article  
**Original**: "Climate Report Findings"  
**Suggested**: "2024 Climate Crisis Report: 5 Key Impacts on Global Ecosystems | CBC Analysis"

---

### 3. Tweet Summary  
**Input Article**: "New study reveals 40% decline in Arctic ice..."  
**Tweet**: "🚨 Breaking: Arctic ice shrinks 40% in decade, study shows. Urgent climate action needed to preserve polar ecosystems. #ClimateChange #ArcticNews 🌍"
