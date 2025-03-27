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
            self.client = tweepy.Client(
                consumer_key=TWITTER_API_KEY,
                consumer_secret=TWITTER_API_SECRET,
                access_token=TWITTER_ACCESS_TOKEN,
                access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
                wait_on_rate_limit=True
            )
            logger.info("Twitter API client initialized successfully for memecoin engagement")
        except Exception as e:
            logger.error(f"Failed to initialize Twitter API client: {str(e)}")
            raise

    def get_community_tweets(self, username: str, count: int = 5) -> List[Dict[str, Any]]:
        """Fetch recent tweets from a memecoin community account."""
        try:
            # First, get the user ID from the username
            user = self.client.get_user(username=username)
            if not user.data:
                logger.error(f"User {username} not found")
                return []

            user_id = user.data.id
            tweets = self.client.get_users_tweets(
                id=user_id,
                max_results=count,
                tweet_fields=['created_at', 'public_metrics']
            )

            if not tweets.data:
                return []

            return [{
                'id': tweet.id,
                'text': tweet.text,
                'created_at': tweet.created_at,
                'likes': tweet.public_metrics['like_count'],
                'retweets': tweet.public_metrics['retweet_count'],
                'replies': tweet.public_metrics['reply_count'],
                'user': username
            } for tweet in tweets.data]
        except Exception as e:
            logger.error(f"Error fetching tweets for {username}: {str(e)}")
            return []

    def get_community_mentions(self, username: str, count: int = 5) -> List[Dict[str, Any]]:
        """Fetch recent mentions of a memecoin community."""
        try:
            # First, get the user ID from the username
            user = self.client.get_user(username=username)
            if not user.data:
                logger.error(f"User {username} not found")
                return []

            user_id = user.data.id
            mentions = self.client.get_users_mentions(
                id=user_id,
                max_results=count,
                tweet_fields=['created_at', 'public_metrics', 'author_id']
            )

            if not mentions.data:
                return []

            # Get user information for authors
            author_ids = [tweet.author_id for tweet in mentions.data]
            users = self.client.get_users(ids=author_ids)
            user_map = {user.id: user.username for user in users.data} if users.data else {}

            return [{
                'id': mention.id,
                'text': mention.text,
                'created_at': mention.created_at,
                'user': user_map.get(mention.author_id, 'unknown'),
                'likes': mention.public_metrics['like_count'],
                'retweets': mention.public_metrics['retweet_count']
            } for mention in mentions.data]
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
                search_results = self.client.search_recent_tweets(
                    query=hashtag,
                    max_results=count,
                    tweet_fields=['created_at', 'public_metrics', 'author_id']
                )
                
                if not search_results.data:
                    continue

                # Get user information for authors
                author_ids = [tweet.author_id for tweet in search_results.data]
                users = self.client.get_users(ids=author_ids)
                user_map = {user.id: user.username for user in users.data} if users.data else {}

                hashtag_tweets.extend([{
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'user': user_map.get(tweet.author_id, 'unknown'),
                    'likes': tweet.public_metrics['like_count'],
                    'retweets': tweet.public_metrics['retweet_count']
                } for tweet in search_results.data])
            
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
            self.client.create_tweet(
                text=reply_text,
                in_reply_to_tweet_id=tweet_id
            )
            logger.info(f"Successfully posted reply to tweet {tweet_id}")
            return True
        except Exception as e:
            logger.error(f"Error posting reply to tweet {tweet_id}: {str(e)}")
            return False

    def like_tweet(self, tweet_id: int) -> bool:
        """Like a specific tweet."""
        try:
            self.client.like(tweet_id)
            logger.info(f"Successfully liked tweet {tweet_id}")
            return True
        except Exception as e:
            logger.error(f"Error liking tweet {tweet_id}: {str(e)}")
            return False

    def retweet(self, tweet_id: int) -> bool:
        """Retweet a specific tweet."""
        try:
            self.client.retweet(tweet_id)
            logger.info(f"Successfully retweeted tweet {tweet_id}")
            return True
        except Exception as e:
            logger.error(f"Error retweeting tweet {tweet_id}: {str(e)}")
            return False 