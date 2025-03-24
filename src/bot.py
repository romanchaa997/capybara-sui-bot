import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from src.twitter.tracker import TwitterTracker
from src.twitter.memecoin_engagement import MemecoinEngagement
from src.utils.ai_helper import AIHelper
from src.blockchain.sui_client import SuiClient
from config.settings import (
    TWEET_ANALYSIS_INTERVAL,
    ONCHAIN_UPDATE_INTERVAL,
    GIVEAWAY_INTERVAL,
    MAX_DAILY_TWEETS,
    MAX_DAILY_REPLIES,
    MEMECOIN_ENGAGEMENT_INTERVAL
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CapybaraBot:
    def __init__(self):
        """Initialize the Capybara bot with all necessary components."""
        self.twitter_tracker = TwitterTracker()
        self.memecoin_engagement = MemecoinEngagement()
        self.ai_helper = AIHelper()
        self.sui_client = SuiClient()
        self.daily_tweet_count = 0
        self.daily_reply_count = 0
        self.last_reset = datetime.now()

    async def start(self):
        """Start the bot and run all tasks."""
        logger.info("Starting Capybara bot...")
        
        # Reset daily counters
        self._reset_daily_counters()
        
        # Start main tasks
        tasks = [
            self._run_tweet_analysis(),
            self._run_onchain_updates(),
            self._run_giveaways(),
            self._run_memecoin_engagement()
        ]
        
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"Error in main bot loop: {str(e)}")
            raise

    async def _run_tweet_analysis(self):
        """Run tweet analysis and engagement tasks."""
        while True:
            try:
                # Reset counters if needed
                self._reset_daily_counters()
                
                # Analyze tweets from Sui accounts
                tweets = self.twitter_tracker.analyze_sui_accounts()
                
                # Generate and post content based on analysis
                if self.daily_tweet_count < MAX_DAILY_TWEETS:
                    await self._generate_and_post_content(tweets)
                
                # Engage with tweets
                if self.daily_reply_count < MAX_DAILY_REPLIES:
                    await self._engage_with_tweets(tweets)
                
                # Wait for next interval
                await asyncio.sleep(TWEET_ANALYSIS_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error in tweet analysis task: {str(e)}")
                await asyncio.sleep(60)  # Wait before retrying

    async def _run_onchain_updates(self):
        """Run on-chain data analysis and updates."""
        while True:
            try:
                async with self.sui_client as client:
                    # Get various on-chain metrics
                    tvl_data = await client.get_tvl_by_project()
                    top_projects = await client.get_top_projects()
                    trading_pairs = await client.get_trading_pairs()
                    farming_pools = await client.get_farming_pools()
                    nft_collections = await client.get_nft_collections()
                    
                    # Generate and post updates
                    if self.daily_tweet_count < MAX_DAILY_TWEETS:
                        await self._post_onchain_updates(
                            tvl_data, top_projects, trading_pairs,
                            farming_pools, nft_collections
                        )
                
                await asyncio.sleep(ONCHAIN_UPDATE_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error in on-chain updates task: {str(e)}")
                await asyncio.sleep(60)  # Wait before retrying

    async def _run_giveaways(self):
        """Run community giveaway tasks."""
        while True:
            try:
                # TODO: Implement giveaway logic
                await asyncio.sleep(GIVEAWAY_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error in giveaway task: {str(e)}")
                await asyncio.sleep(60)  # Wait before retrying

    async def _run_memecoin_engagement(self):
        """Run memecoin community engagement tasks."""
        while True:
            try:
                # Get engaging content from memecoin communities
                community_content = self.memecoin_engagement.get_engaging_community_content(hours=24)
                
                # Engage with community content
                for content in community_content:
                    if self.daily_reply_count >= MAX_DAILY_REPLIES:
                        break
                    
                    # Generate friendly and engaging response
                    context = f"Engaging with {content['user']}'s tweet about their memecoin community"
                    response = self.ai_helper.generate_engagement_response(
                        content['text'],
                        context
                    )
                    
                    if response:
                        # Post reply and engage with the tweet
                        if self.memecoin_engagement.post_reply(content['id'], response):
                            self.memecoin_engagement.like_tweet(content['id'])
                            self.memecoin_engagement.retweet(content['id'])
                            self.daily_reply_count += 1
                            logger.info(f"Engaged with memecoin community tweet: {content['id']}")
                
                # Wait for next interval
                await asyncio.sleep(MEMECOIN_ENGAGEMENT_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error in memecoin engagement task: {str(e)}")
                await asyncio.sleep(60)  # Wait before retrying

    async def _generate_and_post_content(self, tweets: List[Dict[str, Any]]):
        """Generate and post content based on tweet analysis."""
        try:
            # Analyze trending topics
            trending_topics = self.ai_helper.analyze_trending_topics(tweets)
            
            # Generate content for each trending topic
            for topic in trending_topics:
                if self.daily_tweet_count >= MAX_DAILY_TWEETS:
                    break
                    
                context = f"Based on recent discussions in the Sui ecosystem about {topic}"
                tweet_content = self.ai_helper.generate_tweet(context, topic)
                
                if tweet_content:
                    # TODO: Implement actual tweet posting
                    self.daily_tweet_count += 1
                    logger.info(f"Generated tweet: {tweet_content}")
                    
        except Exception as e:
            logger.error(f"Error generating and posting content: {str(e)}")

    async def _engage_with_tweets(self, tweets: List[Dict[str, Any]]):
        """Engage with relevant tweets."""
        try:
            for tweet in tweets:
                if self.daily_reply_count >= MAX_DAILY_REPLIES:
                    break
                    
                # Analyze tweet sentiment and engagement potential
                analysis = self.ai_helper.analyze_tweet_sentiment(tweet['text'])
                
                if analysis.get('engagement_potential') == 'high':
                    # Generate response
                    context = f"Responding to tweet from {tweet['user']} about {analysis.get('topics', [])}"
                    response = self.ai_helper.generate_engagement_response(tweet['text'], context)
                    
                    if response:
                        # TODO: Implement actual reply posting
                        self.daily_reply_count += 1
                        logger.info(f"Generated reply: {response}")
                        
        except Exception as e:
            logger.error(f"Error engaging with tweets: {str(e)}")

    async def _post_onchain_updates(self, tvl_data: List[Dict[str, Any]],
                                  top_projects: List[Dict[str, Any]],
                                  trading_pairs: List[Dict[str, Any]],
                                  farming_pools: List[Dict[str, Any]],
                                  nft_collections: List[Dict[str, Any]]):
        """Post updates about on-chain activity."""
        try:
            # Generate and post TVL update
            if tvl_data and self.daily_tweet_count < MAX_DAILY_TWEETS:
                tvl_data_formatted = {
                    'total_tvl': tvl_data[0].get('tvl', 0),
                    'top_projects': [p['name'] for p in tvl_data[:3]],
                    'growth': tvl_data[0].get('growth', 0)
                }
                tvl_tweet = self.ai_helper.generate_onchain_update(
                    tvl_data_formatted,
                    "TVL Update"
                )
                if tvl_tweet:
                    # TODO: Implement actual tweet posting
                    self.daily_tweet_count += 1
                    logger.info(f"Posted TVL update: {tvl_tweet}")
            
            # Generate and post top projects update
            if top_projects and self.daily_tweet_count < MAX_DAILY_TWEETS:
                projects_data = {
                    'top_projects': [{
                        'name': p['name'],
                        'volume': p.get('volume', 0),
                        'growth': p.get('growth', 0)
                    } for p in top_projects[:3]]
                }
                projects_tweet = self.ai_helper.generate_onchain_update(
                    projects_data,
                    "Top Projects"
                )
                if projects_tweet:
                    # TODO: Implement actual tweet posting
                    self.daily_tweet_count += 1
                    logger.info(f"Posted projects update: {projects_tweet}")
            
            # Generate and post trading pairs update
            if trading_pairs and self.daily_tweet_count < MAX_DAILY_TWEETS:
                pairs_data = {
                    'top_pairs': [{
                        'pair': p['pair'],
                        'volume': p.get('volume', 0),
                        'price_change': p.get('price_change', 0)
                    } for p in trading_pairs[:3]]
                }
                pairs_tweet = self.ai_helper.generate_onchain_update(
                    pairs_data,
                    "Trading Pairs"
                )
                if pairs_tweet:
                    # TODO: Implement actual tweet posting
                    self.daily_tweet_count += 1
                    logger.info(f"Posted trading pairs update: {pairs_tweet}")
            
            # Generate and post farming pools update
            if farming_pools and self.daily_tweet_count < MAX_DAILY_TWEETS:
                pools_data = {
                    'top_pools': [{
                        'name': p['name'],
                        'apr': p.get('apr', 0),
                        'tvl': p.get('tvl', 0)
                    } for p in farming_pools[:3]]
                }
                pools_tweet = self.ai_helper.generate_onchain_update(
                    pools_data,
                    "Farming Pools"
                )
                if pools_tweet:
                    # TODO: Implement actual tweet posting
                    self.daily_tweet_count += 1
                    logger.info(f"Posted farming pools update: {pools_tweet}")
            
            # Generate and post NFT collections update
            if nft_collections and self.daily_tweet_count < MAX_DAILY_TWEETS:
                nft_data = {
                    'top_collections': [{
                        'name': c['name'],
                        'volume': c.get('volume', 0),
                        'floor_price': c.get('floor_price', 0)
                    } for c in nft_collections[:3]]
                }
                nft_tweet = self.ai_helper.generate_onchain_update(
                    nft_data,
                    "NFT Collections"
                )
                if nft_tweet:
                    # TODO: Implement actual tweet posting
                    self.daily_tweet_count += 1
                    logger.info(f"Posted NFT collections update: {nft_tweet}")
                    
        except Exception as e:
            logger.error(f"Error posting on-chain updates: {str(e)}")

    def _reset_daily_counters(self):
        """Reset daily tweet and reply counters if needed."""
        now = datetime.now()
        if (now - self.last_reset).days >= 1:
            self.daily_tweet_count = 0
            self.daily_reply_count = 0
            self.last_reset = now
            logger.info("Reset daily counters") 