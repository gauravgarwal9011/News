import streamlit as st
from utils import get_news_articles, summarize_article, analyze_sentiment, comparative_analysis, generate_hindi_tts, extract_topics

# Set page title & favicon
st.set_page_config(page_title="News Summarization & Sentiment Analysis", page_icon="📰", layout="wide")

# Custom Styling
st.markdown("""
    <style>
        .main {background-color: #f5f5f5;}
        .stTextInput > div > div > input {border-radius: 10px; padding: 10px;}
        .stButton > button {border-radius: 10px; background-color: #2b7a78; color: white; font-weight: bold;}
        .stButton > button:hover {background-color: #17252a;}
        .custom-card {background-color: white; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);}
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("📰 News Summarization & Sentiment Analysis with Hindi TTS")
st.markdown("### 🔍 Enter a company name to fetch news articles and analyze sentiment.")

# Input box for the company name
company_name = st.text_input("🏢 **Enter Company Name:**", "")

if company_name:
    st.markdown(f"## 🔎 Fetching News for: **{company_name}**")

    # Step 1: Get News Articles
    articles = get_news_articles(company_name)
    if not articles:
        st.warning("⚠️ No articles found. Try another company name.")
    else:
        processed_articles = []

        # Display articles using an improved layout
        st.markdown("### 🗞️ Latest News Articles")
        for article in articles:
            with st.container():
                st.markdown(f"""
                    <div class="custom-card">
                        <h4>📰 {article['title']}</h4>
                        <a href="{article['url']}" target="_blank">🔗 Read Full Article</a>
                    </div>
                """, unsafe_allow_html=True)

                summary = summarize_article(article["url"])
                sentiment = analyze_sentiment(summary)
                topics = extract_topics(summary)

                # Display article information
                with st.expander(f"📌 **Details for:** {article['title']}"):
                    st.write(f"📖 **Summary:** {summary}")
                    st.write(f"🎭 **Sentiment:** `{sentiment}`")
                    st.write(f"🏷️ **Extracted Topics:** {', '.join(topics) if topics else 'No topics detected'}")

                processed_articles.append({
                    "title": article["title"],
                    "summary": summary,
                    "sentiment": sentiment,
                    "topics": topics
                })

        # Step 2: Perform Comparative Analysis
        st.markdown("---")
        st.markdown("## 📊 Sentiment & Comparative Analysis")
        analysis = comparative_analysis(processed_articles)

        # Display analysis results with a JSON viewer
        with st.expander("📌 **View Detailed Sentiment Analysis**"):
            st.json(analysis)

        # Step 3: Generate Hindi TTS
        st.markdown("## 🔊 Hindi Text-to-Speech Summary")
        final_summary = f"Company: {company_name}. Sentiment Report: {analysis['final sentiments']}"
        tts_file = generate_hindi_tts(final_summary)

        # Step 4: Play Hindi Speech Output
        if tts_file:
            st.audio(tts_file, format="audio/mp3", start_time=0)
            st.success("✅ **Hindi Speech Generated! Click play to listen.**")

# Footer
st.markdown("---")
st.markdown("🎤 **Developed with ❤️ using BeautifulSoup, Streamlit, NLP & TTS.**")

