from typing import List, Dict, Any
import tweepy
from datetime import datetime, timedelta
import logging
from ..base import Tool
from textblob import TextBlob
import asyncio
import re
from ..data.sui_projects import SUI_PROJECTS, TECHNICAL_EXPLANATIONS, TOKEN_INFO
from .price_tool import PriceTool

class CommunityTool(Tool):
    def __init__(self, twitter_client: tweepy.API):
        super().__init__(
            name="community_engagement",
            description="Handles community engagement, sentiment analysis, and automated responses",
            function=self._execute  # Pass the _execute method as the function
        )
        self.twitter_client = twitter_client
        self.logger = logging.getLogger(__name__)
        self.engagement_history = []
        self.price_tool = PriceTool()
        
        # Enhanced response templates with more variety and context
        self.response_templates = {
            "price_query": [
                "💰 Current price of {token} is ${price} (24h change: {change}%)",
                "📊 {token} is trading at ${price} with a {change}% change in 24h",
                "💎 {token} price: ${price} | 24h: {change}% | Market cap: ${mcap}"
            ],
            "project_info": [
                "🏗️ {project} is building on Sui! Key features:\n{features}",
                "🚀 {project} is revolutionizing {aspect} on Sui!",
                "💫 {project} brings {value} to the Sui ecosystem!",
                "📚 {project} - {description}\n\nKey features:\n{features}"
            ],
            "positive": [
                "🚀 Absolutely! {context} is what makes Sui special!",
                "💪 This is the way! {context} is just the beginning!",
                "🔥 You're speaking my language! {context} is why we're here!",
                "🦫 Capy approved! {context} is the future of Sui!",
                "💎 Diamond hands unite! {context} is just getting started!"
            ],
            "negative": [
                "🤔 Let me help clarify about {context}. Here's what's actually happening...",
                "💡 I understand your concern about {context}. Let me explain...",
                "📚 Let me share some insights about {context}...",
                "🔍 Let's look at the facts about {context}...",
                "💪 Stay strong! {context} is just a temporary setback."
            ],
            "neutral": [
                "📊 Here's some data about {context} that might interest you...",
                "🔍 Let me break down {context} for you...",
                "💫 Interesting perspective on {context}. Here's what I know...",
                "📈 Let's analyze {context} together...",
                "🎯 Here's what you need to know about {context}..."
            ],
            "technical": [
                "⚡ {topic} on Sui works like this: {explanation}",
                "🔧 Here's how {topic} functions in the Sui ecosystem: {explanation}",
                "⚙️ Let me explain the technical details of {topic}: {explanation}"
            ],
            "meme": [
                "🦫 *Capy noises* {meme}",
                "🐊 *Wen moon?* {meme}",
                "🚀 *To the moon!* {meme}",
                "💎 *Diamond hands* {meme}",
                "🔥 *FOMO intensifies* {meme}"
            ],
            "defi": [
                "📈 DeFi on Sui is growing fast! Here are the top protocols:\n{protocols}",
                "💧 Liquidity is flowing! Current TVL: ${tvl}",
                "🌊 DeFi waves on Sui:\n{protocols}"
            ],
            "nft": [
                "🎨 NFT scene on Sui is heating up! Top collections:\n{collections}",
                "🖼️ Check out these amazing Sui NFTs:\n{collections}",
                "✨ NFT highlights on Sui:\n{collections}"
            ]
        }
        
        # Enhanced query patterns for different types of questions
        self.query_patterns = {
            "price_query": r"(what'?s|what is|how much|price of|value of)\s+(\w+)\s*(token|coin)?",
            "project_info": r"(tell me about|what is|explain|describe)\s+(\w+)",
            "technical": r"(how does|explain|describe|what is)\s+(\w+)\s+(work|function|operate)",
            "meme": r"(meme|funny|joke|lol|haha)",
            "defi": r"(defi|protocols|tvl|liquidity|yield|farming)",
            "nft": r"(nft|collection|art|gallery)",
            "staking": r"(stake|staking|rewards|validator|delegate)",
            "token_info": r"(token|coin|symbol|contract)\s+(\w+)",
            "ecosystem": r"(ecosystem|projects|building|developing)",
            "roadmap": r"(roadmap|updates|future|planning)"
        }

    async def _execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute community engagement actions"""
        try:
            if action == "monitor_mentions":
                return await self._monitor_mentions()
            elif action == "analyze_sentiment":
                return await self._analyze_sentiment(kwargs.get("text", ""))
            elif action == "generate_response":
                return await self._generate_response(
                    kwargs.get("tweet", {}),
                    kwargs.get("sentiment", "neutral")
                )
            elif action == "track_engagement":
                return await self._track_engagement()
            elif action == "handle_query":
                return await self._handle_specific_query(kwargs.get("text", ""))
            else:
                raise ValueError(f"Unknown action: {action}")
        except Exception as e:
            self.logger.error(f"Error executing community engagement action: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _handle_specific_query(self, text: str) -> Dict[str, Any]:
        """Handle specific types of queries"""
        try:
            text = text.lower()
            
            # Check for price queries
            price_match = re.search(self.query_patterns["price_query"], text)
            if price_match:
                token = price_match.group(2)
                price_data = await self.price_tool._execute("get_price", token=token)
                if price_data["status"] == "success":
                    return {
                        "status": "success",
                        "type": "price_query",
                        "response": self.response_templates["price_query"][0].format(
                            token=token.upper(),
                            price=price_data["price"],
                            change=price_data["change"],
                            mcap=price_data["mcap"]
                        )
                    }
            
            # Check for project info queries
            project_match = re.search(self.query_patterns["project_info"], text)
            if project_match:
                project = project_match.group(2)
                project_info = SUI_PROJECTS.get(project.lower())
                if project_info:
                    features = "\n".join([f"• {feature}" for feature in project_info["features"]])
                    return {
                        "status": "success",
                        "type": "project_info",
                        "response": self.response_templates["project_info"][3].format(
                            project=project_info["name"],
                            description=project_info["description"],
                            features=features
                        )
                    }
            
            # Check for technical queries
            technical_match = re.search(self.query_patterns["technical"], text)
            if technical_match:
                topic = technical_match.group(2)
                explanation = TECHNICAL_EXPLANATIONS.get(topic.lower())
                if explanation:
                    return {
                        "status": "success",
                        "type": "technical",
                        "response": self.response_templates["technical"][0].format(
                            topic=topic,
                            explanation=explanation
                        )
                    }
            
            # Check for DeFi queries
            defi_match = re.search(self.query_patterns["defi"], text)
            if defi_match:
                protocols = "\n".join([
                    f"• {project['name']}: {project['description']}"
                    for project in SUI_PROJECTS.values()
                    if "defi" in project["aspect"].lower()
                ])
                return {
                    "status": "success",
                    "type": "defi",
                    "response": self.response_templates["defi"][0].format(
                        protocols=protocols
                    )
                }
            
            # Check for NFT queries
            nft_match = re.search(self.query_patterns["nft"], text)
            if nft_match:
                collections = "\n".join([
                    f"• {project['name']}: {project['description']}"
                    for project in SUI_PROJECTS.values()
                    if "nft" in project["aspect"].lower()
                ])
                return {
                    "status": "success",
                    "type": "nft",
                    "response": self.response_templates["nft"][0].format(
                        collections=collections
                    )
                }
            
            # Check for token info queries
            token_match = re.search(self.query_patterns["token_info"], text)
            if token_match:
                token = token_match.group(2)
                token_info = TOKEN_INFO.get(token.lower())
                if token_info:
                    return {
                        "status": "success",
                        "type": "token_info",
                        "response": f"ℹ️ {token_info['name']} ({token.upper()})\n{token_info['description']}\nContract: {token_info['contract']}"
                    }
            
            # Check for ecosystem queries
            ecosystem_match = re.search(self.query_patterns["ecosystem"], text)
            if ecosystem_match:
                projects = "\n".join([
                    f"• {project['name']}: {project['description']}"
                    for project in SUI_PROJECTS.values()
                ])
                return {
                    "status": "success",
                    "type": "ecosystem",
                    "response": f"🌐 Sui Ecosystem Projects:\n{projects}"
                }
            
            # Check for meme requests
            meme_match = re.search(self.query_patterns["meme"], text)
            if meme_match:
                return {
                    "status": "success",
                    "type": "meme",
                    "response": self.response_templates["meme"][0].format(
                        meme="🚀 To the moon! 🚀"
                    )
                }
            
            return {"status": "error", "message": "No specific query pattern matched"}
        except Exception as e:
            self.logger.error(f"Error handling specific query: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _monitor_mentions(self) -> Dict[str, Any]:
        """Monitor and process mentions"""
        try:
            mentions = self.twitter_client.get_mentions_timeline()
            processed_mentions = []
            
            for mention in mentions:
                # Skip if we've already processed this mention
                if any(h["tweet_id"] == mention.id for h in self.engagement_history):
                    continue
                
                # Analyze sentiment
                sentiment = await self._analyze_sentiment(mention.text)
                
                # Generate response
                response = await self._generate_response(mention, sentiment["sentiment"])
                
                # Reply to the mention
                if response["status"] == "success":
                    self.twitter_client.update_status(
                        status=response["response"],
                        in_reply_to_status_id=mention.id
                    )
                
                processed_mentions.append({
                    "tweet_id": mention.id,
                    "user": mention.user.screen_name,
                    "text": mention.text,
                    "sentiment": sentiment["sentiment"],
                    "response": response.get("response", ""),
                    "timestamp": datetime.now().isoformat()
                })
            
            # Update engagement history
            self.engagement_history.extend(processed_mentions)
            
            # Keep only last 24 hours of history
            cutoff_time = datetime.now() - timedelta(hours=24)
            self.engagement_history = [
                h for h in self.engagement_history
                if datetime.fromisoformat(h["timestamp"]) > cutoff_time
            ]
            
            return {
                "status": "success",
                "processed_mentions": processed_mentions
            }
        except Exception as e:
            self.logger.error(f"Error monitoring mentions: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        try:
            analysis = TextBlob(text)
            sentiment_score = analysis.sentiment.polarity
            
            if sentiment_score > 0.2:
                sentiment = "positive"
            elif sentiment_score < -0.2:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            return {
                "status": "success",
                "sentiment": sentiment,
                "score": sentiment_score
            }
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _generate_response(self, tweet: Dict[str, Any], sentiment: str) -> Dict[str, Any]:
        """Generate contextual response based on tweet content and sentiment"""
        try:
            # First try to handle specific queries
            query_result = await self._handle_specific_query(tweet.get("text", ""))
            if query_result["status"] == "success":
                return query_result
            
            # If no specific query matched, use sentiment-based response
            text = tweet.get("text", "").lower()
            context = self._extract_context(text)
            
            # Select appropriate response template
            templates = self.response_templates.get(sentiment, self.response_templates["neutral"])
            response = templates[0].format(context=context)
            
            return {
                "status": "success",
                "response": response
            }
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            return {"status": "error", "message": str(e)}

    def _extract_context(self, text: str) -> str:
        """Extract relevant context from tweet text"""
        # Remove mentions and URLs
        text = " ".join(word for word in text.split() 
                       if not word.startswith(("@", "http")))
        
        # Extract key terms related to Sui ecosystem
        sui_terms = ["sui", "defi", "nft", "dao", "token", "swap", "pool", "stake"]
        context_terms = [term for term in sui_terms if term in text]
        
        if context_terms:
            return context_terms[0]
        return "the Sui ecosystem"

    async def _track_engagement(self) -> Dict[str, Any]:
        """Track engagement metrics"""
        try:
            # Calculate engagement metrics
            total_mentions = len(self.engagement_history)
            sentiment_distribution = {
                "positive": len([h for h in self.engagement_history if h["sentiment"] == "positive"]),
                "negative": len([h for h in self.engagement_history if h["sentiment"] == "negative"]),
                "neutral": len([h for h in self.engagement_history if h["sentiment"] == "neutral"])
            }
            
            # Calculate response rate
            responses = len([h for h in self.engagement_history if h.get("response")])
            response_rate = (responses / total_mentions * 100) if total_mentions > 0 else 0
            
            return {
                "status": "success",
                "metrics": {
                    "total_mentions": total_mentions,
                    "sentiment_distribution": sentiment_distribution,
                    "response_rate": response_rate,
                    "last_24h_mentions": len(self.engagement_history)
                }
            }
        except Exception as e:
            self.logger.error(f"Error tracking engagement: {str(e)}")
            return {"status": "error", "message": str(e)} 