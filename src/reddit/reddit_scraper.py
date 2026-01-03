"""Reddit scraping and data collection."""
import praw
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import time

from src.config import Config


class RedditScraper:
    """Scrape and collect Reddit posts and comments."""
    
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=Config.REDDIT_CLIENT_ID,
            client_secret=Config.REDDIT_CLIENT_SECRET,
            user_agent=Config.REDDIT_USER_AGENT
        )
    
    def get_posts_from_subreddit(self, subreddit_name: str, limit: int = 100,
                                 time_filter: str = "day") -> List[Dict]:
        """
        Get posts from a subreddit.
        
        Args:
            subreddit_name: Name of the subreddit
            limit: Number of posts to retrieve
            time_filter: 'all', 'day', 'hour', 'month', 'week', 'year'
        """
        posts = []
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            for post in subreddit.top(time_filter=time_filter, limit=limit):
                post_data = {
                    "id": post.id,
                    "title": post.title,
                    "selftext": post.selftext,
                    "author": str(post.author) if post.author else "[deleted]",
                    "score": post.score,
                    "upvote_ratio": post.upvote_ratio,
                    "num_comments": post.num_comments,
                    "created_utc": datetime.fromtimestamp(post.created_utc),
                    "url": post.url,
                    "permalink": f"https://reddit.com{post.permalink}",
                    "subreddit": str(post.subreddit),
                    "is_self": post.is_self,
                }
                posts.append(post_data)
        except Exception as e:
            print(f"Error scraping subreddit {subreddit_name}: {e}")
        
        return posts
    
    def get_user_posts(self, username: str, limit: int = 100) -> List[Dict]:
        """Get posts from a specific user."""
        posts = []
        try:
            user = self.reddit.redditor(username)
            
            for post in user.submissions.new(limit=limit):
                post_data = {
                    "id": post.id,
                    "title": post.title,
                    "selftext": post.selftext,
                    "author": username,
                    "score": post.score,
                    "upvote_ratio": post.upvote_ratio,
                    "num_comments": post.num_comments,
                    "created_utc": datetime.fromtimestamp(post.created_utc),
                    "url": post.url,
                    "permalink": f"https://reddit.com{post.permalink}",
                    "subreddit": str(post.subreddit),
                }
                posts.append(post_data)
        except Exception as e:
            print(f"Error getting posts from user {username}: {e}")
        
        return posts
    
    def get_user_comments(self, username: str, limit: int = 100) -> List[Dict]:
        """Get comments from a specific user."""
        comments = []
        try:
            user = self.reddit.redditor(username)
            
            for comment in user.comments.new(limit=limit):
                comment_data = {
                    "id": comment.id,
                    "body": comment.body,
                    "author": username,
                    "score": comment.score,
                    "created_utc": datetime.fromtimestamp(comment.created_utc),
                    "permalink": f"https://reddit.com{comment.permalink}",
                    "subreddit": str(comment.subreddit),
                    "parent_id": comment.parent_id,
                }
                comments.append(comment_data)
        except Exception as e:
            print(f"Error getting comments from user {username}: {e}")
        
        return comments
    
    def get_user_profile(self, username: str) -> Dict:
        """Get profile information for a user."""
        try:
            user = self.reddit.redditor(username)
            
            # Note: Some attributes may not be available for all users
            profile = {
                "username": username,
                "comment_karma": user.comment_karma,
                "link_karma": user.link_karma,
                "created_utc": datetime.fromtimestamp(user.created_utc) if hasattr(user, 'created_utc') else None,
                "is_gold": user.is_gold if hasattr(user, 'is_gold') else False,
                "is_mod": user.is_mod if hasattr(user, 'is_mod') else False,
            }
            
            return profile
        except Exception as e:
            print(f"Error getting profile for {username}: {e}")
            return {}
    
    def search_posts(self, query: str, subreddit: str = None, 
                    limit: int = 100, sort: str = "relevance") -> List[Dict]:
        """
        Search for posts.
        
        Args:
            query: Search query
            subreddit: Optional subreddit to search in
            limit: Number of results
            sort: 'relevance', 'hot', 'top', 'new', 'comments'
        """
        posts = []
        try:
            if subreddit:
                search_target = self.reddit.subreddit(subreddit)
            else:
                search_target = self.reddit
            
            for post in search_target.search(query, limit=limit, sort=sort):
                post_data = {
                    "id": post.id,
                    "title": post.title,
                    "selftext": post.selftext,
                    "author": str(post.author) if post.author else "[deleted]",
                    "score": post.score,
                    "upvote_ratio": post.upvote_ratio,
                    "num_comments": post.num_comments,
                    "created_utc": datetime.fromtimestamp(post.created_utc),
                    "url": post.url,
                    "permalink": f"https://reddit.com{post.permalink}",
                    "subreddit": str(post.subreddit),
                }
                posts.append(post_data)
        except Exception as e:
            print(f"Error searching posts: {e}")
        
        return posts
    
    def get_post_comments(self, post_id: str, limit: int = 100) -> List[Dict]:
        """Get comments from a specific post."""
        comments = []
        try:
            submission = self.reddit.submission(id=post_id)
            submission.comments.replace_more(limit=0)
            
            for comment in submission.comments.list()[:limit]:
                comment_data = {
                    "id": comment.id,
                    "body": comment.body,
                    "author": str(comment.author) if comment.author else "[deleted]",
                    "score": comment.score,
                    "created_utc": datetime.fromtimestamp(comment.created_utc),
                    "permalink": f"https://reddit.com{comment.permalink}",
                    "parent_id": comment.parent_id,
                }
                comments.append(comment_data)
        except Exception as e:
            print(f"Error getting comments for post {post_id}: {e}")
        
        return comments
    
    def get_relevant_subreddits(self, keywords: List[str]) -> List[str]:
        """Find subreddits relevant to trading keywords."""
        relevant = []
        
        for keyword in keywords:
            try:
                # Search for subreddits
                for subreddit in self.reddit.subreddits.search(keyword, limit=10):
                    if subreddit.display_name not in relevant:
                        relevant.append(subreddit.display_name)
            except Exception as e:
                print(f"Error searching for subreddits with keyword {keyword}: {e}")
        
        return relevant

