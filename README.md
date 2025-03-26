---
title: News Summarization App
emoji: 😻
colorFrom: blue
colorTo: gray
sdk: streamlit
sdk_version: 1.43.2
app_file: app.py
pinned: false
---
# 📢 News Summarization and Text-to-Speech Application

This application extracts key details from multiple news articles related to a given company, performs sentiment analysis, conducts a comparative analysis, and generates a text-to-speech (TTS) output in Hindi.

## ✨ Features

- **✅News Extraction**: Extracts news articles from various sources using BeautifulSoup
- **✅Sentiment Analysis**: Analyzes sentiment of news articles (positive, negative, neutral)
- **✅Comparative Analysis**: Compares sentiment across articles and identifies common themes
- **✅Topic Extraction**: Identifies key topics for each article
- **✅Text-to-Speech**: Converts summarized content to Hindi speech
- **✅Web Interface**: Simple UI built with Streamlit
- **✅API**: Backend APIs for frontend communication

## 📂 Project Structure

```
news-summarization-app/
├── app.py                # Streamlit web application
├── api.py                # Fast API endpoints
├── utils.py              # News extraction and analysis utilities
├── requirements.txt      # Required dependencies
└── README.md             # Project documentation
```

## 🚀 Installation & Setup

### 🔧 Local Development

1️⃣ Clone the repository:
   ```bash
   git clone https://github.com/yourusername/News-App.git
   cd News-App
   ```

2️⃣ Create a virtual environment:
   ```bash
   conda create -p venv python == 3.10 -y
   conda activate venv/  # On Windows: venv\Scripts\activate
   ```

3️⃣ Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4️⃣ Run the API server:
   ```bash
   python api.py
   ```

5️⃣ In a new terminal, run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## 🏗️ Models and Implementation Details

### 🔍 News Extraction

The application uses BeautifulSoup to extract news articles from various sources. It fetches the HTML content of news pages and parses it to extract relevant information such as the title, content, and publication date.

### 📊 Sentiment Analysis

The sentiment analysis component uses NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner) sentiment analyzer. This is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media and news articles.

### 🎙️ Text-to-Speech

The text-to-speech functionality uses the gTTS (Google Text-to-Speech) library to convert the summarized content into Hindi speech. In a production environment, more advanced TTS solutions like Mozilla TTS or Hugging Face's speech synthesis models could be used for better quality.

### 🔄 Comparative Analysis

The comparative analysis component performs a cross-article analysis to identify common themes, sentiment trends, and topic overlaps. It generates insights into how different news sources are covering the company.

## 🌐 API Documentation

The application exposes several API endpoints for communication between the frontend and backend:

- `POST /api/get_news`: Combined endpoint for fetching news, summarize articles, analyzing sentiment, extract topics
- `POST /api/tts`: Generates Hindi TTS from a report

## ⚠️ Assumptions & Limitations

- The application assumes that the news sources are accessible and can be scraped using BeautifulSoup.
- For Hindi translation, the application uses a simple approach. In a production environment, this would be replaced with a more sophisticated translation service.
- The sentiment analysis is based on NLTK's VADER, which may not capture all nuances in financial news.
- The application may not handle all edge cases related to news source formatting variations.

## 🚀 Future Improvements

- **🚀 Caching Mechanism**: Reduce API calls and enhance performance.
- **🚀 Advanced NLP Models**: Implement transformer-based models for better sentiment accuracy.
- **🚀 User Authentication**: Save user history and allow personalization.
- **🚀 Data Visualization**: Add interactive charts for comparative analysis.
- **🚀 Multi-Language Support**: Expand TTS to other languages beyond Hindi.
