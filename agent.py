import os
import feedparser
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# AGENT 1: News Fetcher Agent
def news_fetcher_agent(topic="AI"):
    print(f"\n🔍 Fetching news for: {topic}")
    feeds = [
        "https://feeds.feedburner.com/TechCrunch",
        "https://www.theverge.com/rss/index.xml",
        "https://rss.cnn.com/rss/edition_technology.rss",
    ]
    articles = []
    for feed_url in feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:2]:
            articles.append({
                "title": entry.get("title", ""),
                "description": entry.get("summary", "")[:300],
                "url": entry.get("link", ""),
                "source": feed.feed.get("title", ""),
            })
    print(f"✅ Fetched {len(articles)} articles!")
    return articles

# AGENT 2: Summarizer Agent
def summarizer_agent(articles):
    print("\n✍️ Summarizing with Groq AI...")
    summarized = []
    for article in articles[:5]:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{
                "role": "user",
                "content": f"Summarize this tech news in 2 simple sentences:\nTitle: {article['title']}\nDescription: {article['description']}"
            }]
        )
        summarized.append({
            "title": article["title"],
            "summary": response.choices[0].message.content.strip(),
            "source": article["source"],
            "url": article["url"],
        })
    print(f"✅ Summarized {len(summarized)} articles!")
    return summarized

# AGENT 3: Digest Formatter Agent
def digest_formatter_agent(summaries, topic):
    print("\n📰 Creating your digest...")
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"Create a beautiful daily tech news digest for topic: {topic}\nArticles: {summaries}\nFormat with catchy title, intro, each article with emoji and summary, closing thought."
        }]
    )
    return response.choices[0].message.content.strip()

# ORCHESTRATOR
def run_techpulse_agent(topic="AI"):
    print("🚀 TechPulse Agent Starting...")
    articles = news_fetcher_agent(topic)
    if not articles:
        return "No articles found!"
    summaries = summarizer_agent(articles)
    digest = digest_formatter_agent(summaries, topic)
    print("\n📬 YOUR TECHPULSE DIGEST:")
    print(digest)
    return digest

if __name__ == "__main__":
    topic = input("Enter topic (e.g. AI, cybersecurity, Python): ")
    run_techpulse_agent(topic)
