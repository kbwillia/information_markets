"""Example script for Reddit analysis with Ollama."""
from src.reddit.reddit_scraper import RedditScraper
from src.llm.ollama_client import OllamaClient

# Initialize components
reddit_scraper = RedditScraper()
ollama_client = OllamaClient()

# Example: Analyze posts from a subreddit
subreddit = "predictit"
posts = reddit_scraper.get_posts_from_subreddit(subreddit, limit=20)

print(f"Found {len(posts)} posts from r/{subreddit}")

# Summarize and analyze posts
for post in posts[:5]:  # Analyze top 5 posts
    print(f"\nAnalyzing: {post['title']}")
    summary = ollama_client.summarize_reddit_post(post)
    print(f"Analysis: {summary['analysis']}")

# Example: Analyze a Reddit user
username = "example_user"
user_analysis = ollama_client.analyze_reddit_account(
    username,
    reddit_scraper.get_user_posts(username, limit=20),
    reddit_scraper.get_user_comments(username, limit=50)
)

print(f"\nUser Analysis for u/{username}:")
print(user_analysis['analysis'])

# Example: Detect trading signals
signals = ollama_client.detect_trading_signals(posts, market_keywords=["election", "president"])
print(f"\nFound {len(signals)} trading signals")
for signal in signals:
    print(f"  Signal: {signal['post_title']}")

# Example: Market sentiment analysis
sentiment = ollama_client.summarize_market_sentiment(posts, "2024 election")
print(f"\nMarket Sentiment Analysis:")
print(sentiment['sentiment_analysis'])

