import tweepy
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from config.settings import (
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    MEMECOIN_COMMUNITIES,
    MAX_MEMECOIN_REPLIES_PER_INTERVAL
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MemecoinEngagement:
    def __init__(self):
        """Initialize Twitter API client with authentication."""
        try:
            auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
            auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
            self.api = tweepy.API(auth, wait_on_rate_limit=True)
            logger.info("Twitter API client initialized successfully for memecoin engagement")
        except Exception as e:
            logger.error(f"Failed to initialize Twitter API client: {str(e)}")
            raise

    def get_community_tweets(self, username: str, count: int = 5) -> List[Dict[str, Any]]:
        """Fetch recent tweets from a memecoin community account."""
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

    def get_community_mentions(self, username: str, count: int = 5) -> List[Dict[str, Any]]:
        """Fetch recent mentions of a memecoin community."""
        try:
            mentions = self.api.mentions_timeline(count=count, tweet_mode="extended")
            return [{
                'id': mention.id,
                'text': mention.full_text,
                'created_at': mention.created_at,
                'user': mention.user.screen_name,
                'likes': mention.favorite_count,
                'retweets': mention.retweet_count
            } for mention in mentions if username.lower() in mention.full_text.lower()]
        except Exception as e:
            logger.error(f"Error fetching mentions for {username}: {str(e)}")
            return []

    def get_community_hashtags(self, username: str, count: int = 5) -> List[Dict[str, Any]]:
        """Fetch tweets with community-specific hashtags."""
        try:
            # Get community's recent tweets to extract hashtags
            tweets = self.get_community_tweets(username, count)
            hashtags = set()
            for tweet in tweets:
                words = tweet['text'].split()
                hashtags.update(word for word in words if word.startswith('#'))
            
            # Search for tweets with these hashtags
            hashtag_tweets = []
            for hashtag in hashtags:
                search_results = self.api.search_tweets(q=hashtag, count=count, tweet_mode="extended")
                hashtag_tweets.extend([{
                    'id': tweet.id,
                    'text': tweet.full_text,
                    'created_at': tweet.created_at,
                    'user': tweet.user.screen_name,
                    'likes': tweet.favorite_count,
                    'retweets': tweet.retweet_count
                } for tweet in search_results])
            
            return hashtag_tweets[:count]  # Limit to requested count
        except Exception as e:
            logger.error(f"Error fetching hashtag tweets for {username}: {str(e)}")
            return []

    def get_engaging_community_content(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get engaging content from all memecoin communities."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        all_content = []
        
        for community in MEMECOIN_COMMUNITIES:
            try:
                # Get tweets, mentions, and hashtag content
                tweets = self.get_community_tweets(community)
                mentions = self.get_community_mentions(community)
                hashtag_content = self.get_community_hashtags(community)
                
                # Filter recent content
                recent_content = [
                    content for content in tweets + mentions + hashtag_content
                    if content['created_at'] > cutoff_time
                ]
                
                # Sort by engagement
                recent_content.sort(key=lambda x: x['likes'] + x['retweets'], reverse=True)
                all_content.extend(recent_content)
                
            except Exception as e:
                logger.error(f"Error processing community {community}: {str(e)}")
                continue
        
        # Sort all content by engagement and limit to top engaging posts
        all_content.sort(key=lambda x: x['likes'] + x['retweets'], reverse=True)
        return all_content[:MAX_MEMECOIN_REPLIES_PER_INTERVAL]

    def post_reply(self, tweet_id: int, reply_text: str) -> bool:
        """Post a reply to a specific tweet."""
        try:
            self.api.update_status(
                status=reply_text,
                in_reply_to_status_id=tweet_id,
                auto_populate_reply_metadata=True
            )
            logger.info(f"Successfully posted reply to tweet {tweet_id}")
            return True
        except Exception as e:
            logger.error(f"Error posting reply to tweet {tweet_id}: {str(e)}")
            return False

    def like_tweet(self, tweet_id: int) -> bool:
        """Like a specific tweet."""
        try:
            self.api.create_favorite(tweet_id)
            logger.info(f"Successfully liked tweet {tweet_id}")
            return True
        except Exception as e:
            logger.error(f"Error liking tweet {tweet_id}: {str(e)}")
            return False

    def retweet(self, tweet_id: int) -> bool:
        """Retweet a specific tweet."""
        try:
            self.api.retweet(tweet_id)
            logger.info(f"Successfully retweeted tweet {tweet_id}")
            return True
        except Exception as e:
            logger.error(f"Error retweeting tweet {tweet_id}: {str(e)}")
            return False 