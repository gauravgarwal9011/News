import requests
from transformers import pipeline
from bs4 import BeautifulSoup
from newspaper import Article
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from gtts import gTTS
from deep_translator import GoogleTranslator
import spacy
from collections import Counter

# Load spaCy's English language model
nlp = spacy.load("en_core_web_sm")


# Sentiment Models
analyzer = SentimentIntensityAnalyzer()
sentiment_model = pipeline("sentiment-analysis")

# News API Configuration
API_KEY = "fbc2d9cbd685427fae8214e7bf89643f"  # Replace with actual NewsAPI key
NEWS_URL = "https://newsapi.org/v2/everything"

def fetch_news(company):
    """Fetch latest news articles related to a company using NewsAPI."""
    params = {
        "q": company,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY
    }

    response = requests.get(NEWS_URL, params=params)
    data = response.json()

    if data.get("status") == "ok":
        articles = [
            {"title": article["title"], "url": article["url"]}
            for article in data.get("articles", [])[:10]
        ]
        return articles
    return []

def get_news_articles(company_name):
    """Scrapes news articles related to the company from Google Search."""
    search_url = f"https://www.google.com/search?q={company_name}+news"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    for result in soup.find_all("div", class_="tF2Cxc"):
        title = result.find("h3").text if result.find("h3") else "No Title"
        link = result.find("a")["href"] if result.find("a") else "#"

        summary = summarize_article(link)
        sentiment = analyze_sentiment(summary)
        topics = extract_topics(summary)

        article_data = {
            "title": title,
            "link": link,
            "summary": summary,
            "sentiment": sentiment,
            "topics": topics,
        }
        articles.append(article_data)

    return articles

def summarize_article(url):
    """Extracts and summarizes full content from a news article URL."""
    try:
        article = Article(url)
        article.download()
        article.parse()

        # Use first 300 characters as a simple summary
        summary = article.text[:300] if article.text else "Summary not available."
        return summary
    except Exception as e:
        print(f"Error summarizing article: {e}")
        return "Summary not available."

def analyze_sentiment(text):
    """Perform sentiment analysis using both VADER and Transformers."""
    if not text or text == "Summary not available.":
        return "Neutral"

    vader_score = analyzer.polarity_scores(text)["compound"]
    hf_result = sentiment_model(text[:512])[0]["label"]  # First 512 chars

    if vader_score >= 0.05 and hf_result == "POSITIVE":
        return "Positive"
    elif vader_score <= -0.05 and hf_result == "NEGATIVE":
        return "Negative"
    else:
        return "Neutral"

def extract_topics(summary):
    """Extracts key topics from the summary using Named Entity Recognition (NER)."""
    # Process text using spaCy
    doc = nlp(summary)

    # Extract named entities (Proper Nouns, Organizations, Products, etc.)
    named_entities = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT", "GPE", "PERSON", "EVENT"]]

    # Remove generic business terms
    common_words = {"market", "business", "company", "economy", "stock", "finance"}
    filtered_entities = [word for word in named_entities if word.lower() not in common_words]

    # If no named entities found, fall back to noun extraction
    if not filtered_entities:
        # Tokenize and filter out stopwords and non-alphabetic tokens
        filtered_words = [token.text for token in doc if token.is_alpha and not token.is_stop]
        filtered_entities = [word for word, count in Counter(filtered_words).most_common(3)]

    return filtered_entities[:3]

def comparative_analysis(articles):
    """
    Performs comparative sentiment analysis on multiple articles.
    Returns structured sentiment distribution and topic overlap.
    """
    sentiment_counts = Counter([article["sentiment"] for article in articles])

    comparisons = []
    topics = [set(article["topics"]) for article in articles]

    for i in range(len(articles) - 1):
        comparison = {
            "Comparison": f"{articles[i]['title']} vs {articles[i+1]['title']}",
            "Sentiment Impact": f"{articles[i]['sentiment']} vs {articles[i+1]['sentiment']}",
            "Topic Overlap": list(topics[i].intersection(topics[i+1])),
            "Unique Topics in Article 1": list(topics[i] - topics[i+1]),
            "Unique Topics in Article 2": list(topics[i+1] - topics[i]),
        }
        comparisons.append(comparison)

    return {
        "Sentiment Distribution": dict(sentiment_counts),
        "Coverage Differences": comparisons
    }

def generate_hindi_tts(text, filename="hindi_speech.mp3"):
    """Convert English summary to Hindi and generate speech."""
    # Translate English text to Hindi for audio
    translated_text = GoogleTranslator(source="en", target="hi").translate(text)

    # Generate Hindi speech
    tts = gTTS(translated_text, lang="hi")
    tts.save(filename)

    return filename

if __name__ == "__main__":
    company = "Tesla"
    news = get_news_articles(company)

    print("\n✅ **News Articles:**")
    for article in news:
        print(article)

    print("\n✅ **Comparative Analysis:**")
    print(comparative_analysis(news))
