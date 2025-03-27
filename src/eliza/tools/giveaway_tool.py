from typing import Dict, Any, List
import aiohttp
import json
import logging
from datetime import datetime, timedelta
import random
from pysui import SyncClient
import tweepy
from collections import defaultdict
from ..base import Tool

class GiveawayTool(Tool):
    def __init__(self, sui_client: SyncClient, wallet_address: str, private_key: str, twitter_client: tweepy.API):
        super().__init__(
            name="giveaway_manager",
            description="Manage and execute token giveaways on Sui blockchain with Twitter integration",
            function=self._execute
        )
        self.sui_client = sui_client
        self.wallet_address = wallet_address
        self.private_key = private_key
        self.twitter_client = twitter_client
        self.logger = logging.getLogger(__name__)
        
        # Scoring weights
        self.weights = {
            "tweet_count": 0.3,
            "retweet_count": 0.2,
            "like_count": 0.15,
            "reply_count": 0.2,
            "quality_score": 0.15
        }

    async def _execute(self, **kwargs) -> Dict[str, Any]:
        """Execute giveaway operations"""
        try:
            action = kwargs.get("action", "create_giveaway")
            
            if action == "create_giveaway":
                return await self._create_giveaway(
                    kwargs.get("token_id"),
                    kwargs.get("amount"),
                    kwargs.get("requirements")
                )
            elif action == "end_giveaway":
                return await self._end_giveaway(kwargs.get("giveaway_id"))
            elif action == "select_winners":
                return await self._select_winners(kwargs.get("giveaway_id"))
            elif action == "distribute_rewards":
                return await self._distribute_rewards(kwargs.get("giveaway_id"))
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
                
        except Exception as e:
            self.logger.error(f"Error executing giveaway tool: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _create_giveaway(self, token_id: str, amount: int, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new giveaway"""
        try:
            # Create giveaway contract
            contract_data = {
                "token_id": token_id,
                "amount": amount,
                "requirements": requirements,
                "start_time": datetime.now().isoformat(),
                "end_time": (datetime.now() + timedelta(days=7)).isoformat(),
                "status": "active"
            }

            # Store giveaway data on-chain
            tx = await self.sui_client.execute(
                "create_giveaway",
                [contract_data],
                self.wallet_address,
                self.private_key
            )

            # Create Twitter announcement
            tweet_text = f"🎉 New Giveaway Alert! 🎉\n\n"
            tweet_text += f"Prize: {amount} tokens\n"
            tweet_text += f"Requirements: {requirements.get('description', 'Follow and RT')}\n"
            tweet_text += f"Ends: {contract_data['end_time']}\n\n"
            tweet_text += "#Sui #Giveaway #Crypto"

            self.twitter_client.update_status(tweet_text)

            return {
                "status": "success",
                "giveaway_id": tx.id,
                "tweet_id": self.twitter_client.user_timeline(count=1)[0].id
            }

        except Exception as e:
            self.logger.error(f"Error creating giveaway: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _end_giveaway(self, giveaway_id: str) -> Dict[str, Any]:
        """End an active giveaway"""
        try:
            # Update giveaway status on-chain
            tx = await self.sui_client.execute(
                "end_giveaway",
                [giveaway_id],
                self.wallet_address,
                self.private_key
            )

            return {
                "status": "success",
                "transaction_id": tx.id,
                "message": "Giveaway ended successfully"
            }

        except Exception as e:
            self.logger.error(f"Error ending giveaway: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _select_winners(self, giveaway_id: str) -> Dict[str, Any]:
        """Select winners for a giveaway"""
        try:
            # Get participants from on-chain data
            participants = await self.sui_client.execute(
                "get_participants",
                [giveaway_id],
                self.wallet_address,
                self.private_key
            )

            # Select random winners
            winners = self._random_select(participants, 5)  # Select 5 winners

            # Store winners on-chain
            tx = await self.sui_client.execute(
                "store_winners",
                [giveaway_id, winners],
                self.wallet_address,
                self.private_key
            )

            return {
                "status": "success",
                "winners": winners,
                "transaction_id": tx.id
            }

        except Exception as e:
            self.logger.error(f"Error selecting winners: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _distribute_rewards(self, giveaway_id: str) -> Dict[str, Any]:
        """Distribute rewards to winners"""
        try:
            # Get winners from on-chain data
            winners = await self.sui_client.execute(
                "get_winners",
                [giveaway_id],
                self.wallet_address,
                self.private_key
            )

            # Distribute rewards to each winner
            transactions = []
            for winner in winners:
                tx = await self.sui_client.execute(
                    "transfer_tokens",
                    [giveaway_id, winner],
                    self.wallet_address,
                    self.private_key
                )
                transactions.append(tx.id)

            # Announce winners on Twitter
            tweet_text = f"🎉 Giveaway Winners Announced! 🎉\n\n"
            tweet_text += f"Congratulations to our winners:\n"
            for winner in winners:
                tweet_text += f"@{winner}\n"
            tweet_text += "\nRewards have been distributed! 🎁"

            self.twitter_client.update_status(tweet_text)

            return {
                "status": "success",
                "transactions": transactions,
                "tweet_id": self.twitter_client.user_timeline(count=1)[0].id
            }

        except Exception as e:
            self.logger.error(f"Error distributing rewards: {str(e)}")
            return {"status": "error", "message": str(e)}

    def _random_select(self, participants: List[str], num_winners: int) -> List[str]:
        """Randomly select winners from participants"""
        return random.sample(participants, min(num_winners, len(participants)))

    async def _analyze_engagement(self) -> Dict[str, Any]:
        """Analyze community engagement for giveaway selection"""
        try:
            # Get tweets mentioning Capybara in the last 24 hours
            engagement_data = await self._get_twitter_engagement()
            
            # Calculate engagement scores
            scores = self._calculate_engagement_scores(engagement_data)
            
            return {
                "status": "success",
                "engagement_data": {
                    "scores": scores,
                    "timestamp": datetime.now().isoformat()
                }
            }
        except Exception as e:
            self.logger.error(f"Error analyzing engagement: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _get_twitter_engagement(self) -> Dict[str, Any]:
        """Get Twitter engagement data"""
        try:
            # Get tweets from the last 24 hours
            since_time = datetime.now() - timedelta(days=1)
            
            # Search for tweets mentioning Capybara
            query = "(@CapybaraAI OR #CapybaraAI OR #SuiEcosystem) -is:retweet"
            tweets = self.twitter_client.search_tweets(q=query, lang="en", count=100)
            
            engagement_data = defaultdict(lambda: {
                "tweet_count": 0,
                "retweet_count": 0,
                "like_count": 0,
                "reply_count": 0,
                "quality_score": 0
            })
            
            for tweet in tweets:
                if tweet.created_at < since_time:
                    continue
                    
                user_id = tweet.user.screen_name
                
                # Update engagement metrics
                engagement_data[user_id]["tweet_count"] += 1
                engagement_data[user_id]["retweet_count"] += tweet.retweet_count
                engagement_data[user_id]["like_count"] += tweet.favorite_count
                
                # Count replies
                if tweet.in_reply_to_status_id:
                    engagement_data[user_id]["reply_count"] += 1
                
                # Calculate quality score based on tweet content
                quality_score = self._calculate_tweet_quality(tweet.text)
                engagement_data[user_id]["quality_score"] += quality_score
            
            return dict(engagement_data)
            
        except Exception as e:
            self.logger.error(f"Error getting Twitter engagement: {str(e)}")
            return {}

    def _calculate_engagement_scores(self, engagement_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate engagement scores for users"""
        scores = {}
        
        for user_id, metrics in engagement_data.items():
            # Normalize metrics
            normalized_metrics = {
                "tweet_count": min(metrics["tweet_count"] / 10, 1.0),  # Cap at 10 tweets
                "retweet_count": min(metrics["retweet_count"] / 50, 1.0),  # Cap at 50 retweets
                "like_count": min(metrics["like_count"] / 100, 1.0),  # Cap at 100 likes
                "reply_count": min(metrics["reply_count"] / 5, 1.0),  # Cap at 5 replies
                "quality_score": min(metrics["quality_score"] / 5, 1.0)  # Cap at 5 quality points
            }
            
            # Calculate weighted score
            score = sum(
                normalized_metrics[metric] * weight
                for metric, weight in self.weights.items()
            )
            
            scores[user_id] = score
        
        return scores

    def _calculate_tweet_quality(self, tweet_text: str) -> float:
        """Calculate quality score for a tweet"""
        quality_score = 0.0
        
        # Check for relevant hashtags
        relevant_hashtags = ["#SuiEcosystem", "#Sui", "#DeFi", "#NFTs", "#Web3"]
        hashtag_count = sum(1 for tag in relevant_hashtags if tag.lower() in tweet_text.lower())
        quality_score += hashtag_count * 0.5
        
        # Check for meaningful content
        if len(tweet_text.split()) > 5:  # More than 5 words
            quality_score += 0.5
        
        # Check for questions or discussions
        if "?" in tweet_text or "what" in tweet_text.lower() or "how" in tweet_text.lower():
            quality_score += 0.5
        
        # Check for positive sentiment
        positive_words = ["great", "awesome", "amazing", "love", "good", "nice"]
        if any(word in tweet_text.lower() for word in positive_words):
            quality_score += 0.5
        
        return min(quality_score, 5.0)  # Cap at 5 quality points 