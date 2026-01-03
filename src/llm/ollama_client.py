"""Ollama LLM client for text analysis and signal detection."""
import requests
import json
from typing import List, Dict, Optional
from datetime import datetime

from src.config import Config


class OllamaClient:
    """Client for interacting with Ollama LLM."""
    
    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = base_url or Config.OLLAMA_BASE_URL
        self.model = model or Config.OLLAMA_MODEL
    
    def _request(self, endpoint: str, data: Dict) -> Dict:
        """Make request to Ollama API."""
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=data, timeout=120)
        response.raise_for_status()
        return response.json()
    
    def generate(self, prompt: str, system: str = None, 
                temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Generate text using Ollama."""
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        if system:
            data["system"] = system
        
        try:
            response = self._request("/api/generate", data)
            return response.get("response", "")
        except Exception as e:
            print(f"Error generating text with Ollama: {e}")
            return ""
    
    def summarize_reddit_post(self, post: Dict) -> Dict:
        """Summarize a Reddit post and extract key information."""
        content = f"Title: {post.get('title', '')}\n\nContent: {post.get('selftext', '')}"
        
        system_prompt = """You are a financial analyst specializing in prediction markets. 
        Analyze Reddit posts and extract:
        1. Key claims or predictions
        2. Sentiment (bullish/bearish/neutral)
        3. Confidence level
        4. Relevant market indicators
        5. Trading signals (if any)
        
        Format your response as JSON with these fields."""
        
        prompt = f"""Analyze this Reddit post about prediction markets or trading:
        
        {content}
        
        Provide a structured analysis in JSON format."""
        
        analysis_text = self.generate(prompt, system=system_prompt, temperature=0.3)
        
        # Try to extract JSON from response
        try:
            # Find JSON in the response
            json_start = analysis_text.find('{')
            json_end = analysis_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                analysis = json.loads(analysis_text[json_start:json_end])
            else:
                analysis = {"raw_analysis": analysis_text}
        except:
            analysis = {"raw_analysis": analysis_text}
        
        return {
            "post_id": post.get("id"),
            "post_title": post.get("title"),
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    
    def analyze_reddit_account(self, username: str, posts: List[Dict], 
                              comments: List[Dict]) -> Dict:
        """Analyze a Reddit account's posting history for trading signals."""
        # Combine recent posts and comments
        recent_content = []
        for post in posts[:20]:  # Last 20 posts
            recent_content.append(f"POST: {post.get('title', '')} - {post.get('selftext', '')[:500]}")
        
        for comment in comments[:30]:  # Last 30 comments
            recent_content.append(f"COMMENT: {comment.get('body', '')[:500]}")
        
        content_text = "\n\n".join(recent_content)
        
        system_prompt = """You are a financial analyst. Analyze a Reddit user's posting history to determine:
        1. Their expertise level in prediction markets/trading
        2. Their track record (if mentions of past predictions)
        3. Their typical sentiment and positions
        4. Reliability and credibility indicators
        5. Whether following this user's signals would be profitable
        
        Provide a structured assessment."""
        
        prompt = f"""Analyze this Reddit user's posting history:
        
        Username: {username}
        
        Recent Posts and Comments:
        {content_text}
        
        Provide a comprehensive analysis of this user's credibility and potential value as a trading signal source."""
        
        analysis = self.generate(prompt, system=system_prompt, temperature=0.3)
        
        return {
            "username": username,
            "analysis": analysis,
            "posts_analyzed": len(posts),
            "comments_analyzed": len(comments),
            "timestamp": datetime.now().isoformat()
        }
    
    def detect_trading_signals(self, posts: List[Dict], market_keywords: List[str] = None) -> List[Dict]:
        """Detect trading signals from a collection of Reddit posts."""
        signals = []
        
        # Filter posts relevant to markets
        relevant_posts = posts
        if market_keywords:
            relevant_posts = [
                p for p in posts 
                if any(kw.lower() in (p.get('title', '') + p.get('selftext', '')).lower() 
                      for kw in market_keywords)
            ]
        
        for post in relevant_posts[:50]:  # Analyze top 50 posts
            summary = self.summarize_reddit_post(post)
            
            # Check if analysis contains trading signals
            analysis_text = str(summary.get('analysis', {})).lower()
            if any(keyword in analysis_text for keyword in ['buy', 'sell', 'signal', 'bet', 'position', 'predict']):
                signals.append({
                    "post_id": post.get("id"),
                    "post_title": post.get("title"),
                    "signal": summary.get("analysis"),
                    "source_url": post.get("permalink"),
                    "timestamp": datetime.now().isoformat()
                })
        
        return signals
    
    def summarize_market_sentiment(self, posts: List[Dict], market_topic: str) -> Dict:
        """Summarize overall sentiment about a market topic from Reddit posts."""
        # Filter posts about the topic
        relevant_posts = [
            p for p in posts 
            if market_topic.lower() in (p.get('title', '') + p.get('selftext', '')).lower()
        ]
        
        if not relevant_posts:
            return {"sentiment": "neutral", "confidence": 0, "summary": "No relevant posts found"}
        
        # Create summary of posts
        posts_summary = "\n\n".join([
            f"Post {i+1}: {p.get('title', '')} - {p.get('selftext', '')[:300]}"
            for i, p in enumerate(relevant_posts[:20])
        ])
        
        system_prompt = """You are a sentiment analyst for prediction markets. Analyze posts and determine:
        1. Overall sentiment (bullish/bearish/neutral)
        2. Confidence level (0-1)
        3. Key themes and arguments
        4. Consensus view (if any)
        5. Trading recommendation based on sentiment"""
        
        prompt = f"""Analyze sentiment about this market topic: {market_topic}
        
        Relevant Reddit posts:
        {posts_summary}
        
        Provide a sentiment analysis with trading implications."""
        
        analysis = self.generate(prompt, system=system_prompt, temperature=0.3)
        
        return {
            "market_topic": market_topic,
            "posts_analyzed": len(relevant_posts),
            "sentiment_analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }

