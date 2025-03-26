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

def get_news_articles(company_name):
    """Scrapes news articles related to the company from BBC Search."""
    
    search_url = f"https://www.bbc.com/search?q={company_name}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch articles. Status Code: {response.status_code}")
        return []

    if not response.text.strip():
        print("Empty response received from BBC News")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    titles = soup.find_all(class_='sc-87075214-3 cXFiLO')
    all_urls=[]
    links = soup.select('a[href^="/news/articles/"]')
    base_url="https://www.bbc.com"
    for link in links:
        href=link.get('href')
        if href:
            all_urls.append(base_url+href)
    

    ### Ensure both lists have the same length
    for i in range(min(len(titles), len(all_urls))):
        article_data = {
            "title": titles[i].text.strip(),
            "url": all_urls[i],
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

    final_sentiment = max(sentiment_counts, key=sentiment_counts.get)

    return {
        "Sentiment Distribution": dict(sentiment_counts),
        "Coverage Differences": comparisons,
        "final sentiments": f"The Latest news about the company is mostly {final_sentiment.upper()}"
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
