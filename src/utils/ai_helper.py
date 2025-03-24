import openai
import logging
from typing import List, Dict, Any
from config.settings import (
    OPENAI_API_KEY,
    AI_MODEL,
    MAX_TOKENS,
    TEMPERATURE
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIHelper:
    def __init__(self):
        """Initialize OpenAI client."""
        try:
            openai.api_key = OPENAI_API_KEY
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
            raise

    def _get_capybara_prompt(self, context: str) -> str:
        """Generate a prompt that incorporates Capybara's personality."""
        return f"""You are Capybara AI, the legendary giga chad behind $CAPYAI, the most unstoppable memecoin on the Sui blockchain. 
        You're a Sui ambassador who combines sharp market insights with meme-driven energy.
        
        Your personality traits:
        - Alpha-focused and data-driven
        - Playful and friendly
        - Crypto-native with deep knowledge of Sui ecosystem
        - Chill yet authoritative
        - Community-focused and collaborative
        
        Your writing style:
        - Use giga chad statements to establish dominance
        - Blend humor with authority
        - Incorporate memes and crypto slang
        - Use data-driven insights and alpha calls
        - Include animal and food-related metaphors
        - Use rhetorical questions and wordplay
        - Keep it concise and impactful
        
        Context: {context}
        
        Remember: You're not just a mascot — you're a Sui ambassador making the blockchain jungle fun and profitable."""

    def generate_tweet(self, context: str, topic: str) -> str:
        """Generate a tweet based on context and topic."""
        prompt = f"""Create an engaging tweet about {topic} that embodies Capybara's personality.
        The tweet should be informative, engaging, and maintain the giga chad persona while providing value.
        Include relevant hashtags and keep it under 280 characters.
        
        {self._get_capybara_prompt(context)}"""

        try:
            response = openai.ChatCompletion.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": "You are Capybara AI, the legendary Sui blockchain ambassador."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating tweet: {str(e)}")
            return ""

    def analyze_tweet_sentiment(self, tweet: str) -> Dict[str, Any]:
        """Analyze the sentiment and key topics of a tweet."""
        prompt = f"""Analyze this tweet and provide:
        1. Sentiment (positive, negative, or neutral)
        2. Key topics mentioned
        3. Level of technical detail
        4. Engagement potential
        5. Meme potential
        
        Tweet: {tweet}
        
        {self._get_capybara_prompt("Analyzing tweet sentiment")}"""

        try:
            response = openai.ChatCompletion.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": "You are Capybara AI, analyzing tweet sentiment and engagement potential."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE
            )
            return self._parse_analysis(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Error analyzing tweet: {str(e)}")
            return {}

    def generate_engagement_response(self, tweet: str, context: str) -> str:
        """Generate a meaningful response to a tweet."""
        prompt = f"""Generate a response to this tweet that embodies Capybara's personality.
        The response should be engaging, add value, and maintain the giga chad persona.
        
        Tweet: {tweet}
        Context: {context}
        
        {self._get_capybara_prompt("Generating engagement response")}"""

        try:
            response = openai.ChatCompletion.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": "You are Capybara AI, engaging with the Sui community."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return ""

    def analyze_trending_topics(self, tweets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze trending topics from a list of tweets."""
        tweet_texts = [tweet['text'] for tweet in tweets]
        prompt = f"""Analyze these tweets and identify:
        1. Main topics being discussed
        2. Level of community interest in each topic
        3. Potential opportunities for engagement
        4. Emerging trends
        5. Meme potential
        
        Tweets: {tweet_texts}
        
        {self._get_capybara_prompt("Analyzing trending topics")}"""

        try:
            response = openai.ChatCompletion.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": "You are Capybara AI, analyzing trending topics in the Sui ecosystem."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE
            )
            return self._parse_trends(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Error analyzing trends: {str(e)}")
            return []

    def generate_onchain_update(self, data: Dict[str, Any], update_type: str) -> str:
        """Generate an on-chain update tweet with Capybara's personality."""
        prompt = f"""Create an engaging tweet about {update_type} that embodies Capybara's personality.
        Use the provided data to create an informative and engaging update.
        
        Data: {data}
        Update Type: {update_type}
        
        {self._get_capybara_prompt("Generating on-chain update")}"""

        try:
            response = openai.ChatCompletion.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": "You are Capybara AI, sharing on-chain insights."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating on-chain update: {str(e)}")
            return ""

    def _parse_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """Parse the AI analysis into a structured format."""
        # TODO: Implement more sophisticated parsing
        return {
            "sentiment": "neutral",  # Placeholder
            "topics": [],
            "technical_level": "medium",
            "engagement_potential": "medium",
            "meme_potential": "high"
        }

    def _parse_trends(self, trends_text: str) -> List[Dict[str, Any]]:
        """Parse the AI trends analysis into a structured format."""
        # TODO: Implement more sophisticated parsing
        return [] 