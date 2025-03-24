import tweepy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CapybaraTwitterBot:
    def __init__(self):
        # Twitter API Authentication
        self.client = tweepy.Client(
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )
        
        # Sui-related accounts to track
        self.sui_accounts = [
            'b1ackd0g', 'EvanWeb3', 'EmanAbio', 'Mysten_Labs', 
            'SuiNetwork', 'SuiChiefEcon', 'SuiCorner', 
            'Community_Sui', 'NotCryptoBro', 'NativeAssets'
        ]

    def track_account_tweets(self, username, max_tweets=10):
        try:
            user_id = self.client.get_user(username=username).data.id
            tweets = self.client.get_users_tweets(
                id=user_id, 
                max_results=max_tweets
            )
            return tweets
        except Exception as e:
            print(f"Error tracking tweets for {username}: {e}")
            return None

def main():
    bot = CapybaraTwitterBot()
    for account in bot.sui_accounts:
        print(f"Tracking tweets for {account}")
        tweets = bot.track_account_tweets(account)
        if tweets and tweets.data:
            for tweet in tweets.data:
                print(tweet.text)

if __name__ == "__main__":
    main()