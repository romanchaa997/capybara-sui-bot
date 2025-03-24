import tweepy
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from config.settings import (
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    SUI_ACCOUNTS,
    MAX_TWEETS_PER_ACCOUNT
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TwitterTracker:
    def __init__(self):
        """Initialize Twitter API client with authentication."""
        try:
            auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
            auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
            self.api = tweepy.API(auth, wait_on_rate_limit=True)
            logger.info("Twitter API client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Twitter API client: {str(e)}")
            raise

    def get_user_tweets(self, username: str, count: int = MAX_TWEETS_PER_ACCOUNT) -> List[Dict[str, Any]]:
        """Fetch recent tweets from a specific user."""
        try:
            tweets = self.api.user_timeline(screen_name=username, count=count, tweet_mode="extended")
            return [{
                'id': tweet.id,
                'text': tweet.full_text,
                'created_at': tweet.created_at,
                'likes': tweet.favorite_count,
                'retweets': tweet.retweet_count,
                'replies': tweet.reply_count if hasattr(tweet, 'reply_count') else 0,
                'user': username
            } for tweet in tweets]
        except Exception as e:
            logger.error(f"Error fetching tweets for {username}: {str(e)}")
            return []

    def analyze_sui_accounts(self) -> List[Dict[str, Any]]:
        """Analyze tweets from all Sui-related accounts."""
        all_tweets = []
        for account in SUI_ACCOUNTS:
            tweets = self.get_user_tweets(account)
            all_tweets.extend(tweets)
        
        # Sort by engagement (likes + retweets)
        all_tweets.sort(key=lambda x: x['likes'] + x['retweets'], reverse=True)
        return all_tweets

    def get_trending_topics(self, tweets: List[Dict[str, Any]]) -> List[str]:
        """Extract trending topics from tweets using basic text analysis."""
        # TODO: Implement more sophisticated topic extraction
        # For now, return a simple list of unique words
        words = set()
        for tweet in tweets:
            words.update(tweet['text'].lower().split())
        return list(words)[:10]  # Return top 10 words

    def get_engagement_metrics(self, tweets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate engagement metrics for the analyzed tweets."""
        total_likes = sum(tweet['likes'] for tweet in tweets)
        total_retweets = sum(tweet['retweets'] for tweet in tweets)
        total_replies = sum(tweet['replies'] for tweet in tweets)
        
        return {
            'total_tweets': len(tweets),
            'total_likes': total_likes,
            'total_retweets': total_retweets,
            'total_replies': total_replies,
            'avg_engagement': (total_likes + total_retweets + total_replies) / len(tweets) if tweets else 0
        }

    def get_active_accounts(self, hours: int = 24) -> List[str]:
        """Get list of accounts that have tweeted in the last specified hours."""
        active_accounts = []
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        for account in SUI_ACCOUNTS:
            try:
                tweets = self.get_user_tweets(account, count=1)
                if tweets and tweets[0]['created_at'] > cutoff_time:
                    active_accounts.append(account)
            except Exception as e:
                logger.error(f"Error checking activity for {account}: {str(e)}")
                continue
        
        return active_accounts

    def get_most_engaging_tweets(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get the most engaging tweets from the last specified hours."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        all_tweets = []
        
        for account in SUI_ACCOUNTS:
            tweets = self.get_user_tweets(account)
            recent_tweets = [t for t in tweets if t['created_at'] > cutoff_time]
            all_tweets.extend(recent_tweets)
        
        # Sort by engagement and return top 10
        all_tweets.sort(key=lambda x: x['likes'] + x['retweets'], reverse=True)
        return all_tweets[:10] 