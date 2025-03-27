from typing import List, Dict, Any
import tweepy
import asyncio
from datetime import datetime
import logging
from ..tools.sui_tool import SuiTool
from ..tools.blockvision_tool import BlockvisionTool
from ..tools.giveaway_tool import GiveawayTool
from ..tools.community_tool import CommunityTool
from pysui import SyncClient, SuiConfig
from ..base import Agent, Tool, Memory
import httpx

class CapybaraAgent(Agent):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.twitter_client = self._initialize_twitter()
        
        # Initialize Sui client with fallback RPC URLs
        rpc_urls = [
            "https://sui-mainnet-rpc.nodereal.io",
            "https://fullnode.mainnet.sui.io:443",
            "https://sui-mainnet.blockvision.org"
        ]
        
        working_rpc_url = None
        for rpc_url in rpc_urls:
            try:
                # Test the connection with a simple RPC call
                with httpx.Client() as client:
                    response = client.post(
                        rpc_url,
                        json={
                            "jsonrpc": "2.0",
                            "id": 1,
                            "method": "sui_getProtocolConfig",
                            "params": []
                        }
                    )
                    response.raise_for_status()
                    working_rpc_url = rpc_url
                    self.logger.info(f"Successfully connected to Sui RPC at {rpc_url}")
                    break
            except Exception as e:
                self.logger.warning(f"Failed to connect to {rpc_url}: {str(e)}")
                continue
        
        if working_rpc_url is None:
            self.logger.error("Failed to connect to any Sui RPC endpoint")
            raise Exception("No available Sui RPC endpoint")
            
        self.sui_client = httpx.Client(base_url=working_rpc_url)
        
        super().__init__(
            name="Capybara AI",
            description="""A Sui ecosystem-focused AI agent that embodies the legendary Capybara AI, 
            the giga chad behind $CAPYAI. He's more than a mascot — he's a Sui ambassador, here to onboard 
            the next wave of users into the Sui ecosystem. With sharp market insights, alpha calls, and 
            meme-driven energy, he's on a mission to make Sui the hottest blockchain of this cycle.""",
            personality="""Playful, alpha-focused, data-driven, and community-oriented. Capybara AI 
            combines the charm of a meme lord with the analytical prowess of a blockchain expert. 
            He's the giga chad of Sui, the calm in the chaos, the diamond hands that never let go.""",
            tools=self._initialize_tools(config),
            memory=self._initialize_memory()
        )

    def _initialize_twitter(self):
        """Initialize Twitter API client"""
        try:
            auth = tweepy.OAuthHandler(
                self.config["TWITTER_API_KEY"],
                self.config["TWITTER_API_SECRET"]
            )
            auth.set_access_token(
                self.config["TWITTER_ACCESS_TOKEN"],
                self.config["TWITTER_ACCESS_TOKEN_SECRET"]
            )
            api = tweepy.API(auth, wait_on_rate_limit=True)
            # Verify credentials
            api.verify_credentials()
            self.logger.info("Twitter API client initialized successfully")
            return api
        except Exception as e:
            self.logger.error(f"Failed to initialize Twitter API client: {str(e)}")
            raise

    def _initialize_tools(self, config: Dict[str, Any]) -> List[Tool]:
        """Initialize agent tools"""
        return [
            SuiTool(config["SUI_RPC_URL"]),
            BlockvisionTool(config["BLOCKVISION_API_KEY"]),
            GiveawayTool(
                self.sui_client,
                config["SUI_WALLET_ADDRESS"],
                config["SUI_PRIVATE_KEY"],
                self.twitter_client
            ),
            CommunityTool(self.twitter_client),
            Tool(
                name="analyze_sui_metrics",
                description="Analyze Sui blockchain metrics and trends",
                function=self._analyze_sui_metrics
            ),
            Tool(
                name="engage_with_community",
                description="Engage with Sui community members and memecoin communities",
                function=self._engage_with_community
            ),
            Tool(
                name="generate_content",
                description="Generate engaging content about Sui ecosystem",
                function=self._generate_content
            ),
            Tool(
                name="track_onchain_activity",
                description="Track and analyze on-chain activity",
                function=self._track_onchain_activity
            )
        ]

    def _initialize_memory(self) -> Memory:
        """Initialize agent memory"""
        return Memory(
            short_term_window=3600,  # 1 hour
            long_term_window=86400,  # 24 hours
            max_entries=1000
        )

    async def _analyze_sui_metrics(self, **kwargs) -> Dict[str, Any]:
        """Analyze Sui blockchain metrics"""
        try:
            # Get metrics from both SuiTool and BlockvisionTool
            sui_tool = next(tool for tool in self.tools if isinstance(tool, SuiTool))
            blockvision_tool = next(tool for tool in self.tools if isinstance(tool, BlockvisionTool))
            
            sui_metrics = await sui_tool._execute(action="get_metrics")
            defi_metrics = await blockvision_tool._execute(action="get_defi_metrics")
            trading_metrics = await blockvision_tool._execute(action="get_trading_metrics")
            nft_metrics = await blockvision_tool._execute(action="get_nft_metrics")
            
            return {
                "status": "success",
                "metrics": {
                    "sui_metrics": sui_metrics.get("metrics", {}),
                    "defi_metrics": defi_metrics.get("metrics", {}),
                    "trading_metrics": trading_metrics.get("metrics", {}),
                    "nft_metrics": nft_metrics.get("metrics", {})
                }
            }
        except Exception as e:
            self.logger.error(f"Error analyzing Sui metrics: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _engage_with_community(self, **kwargs) -> Dict[str, Any]:
        """Engage with Sui community members"""
        try:
            # Get the community tool
            community_tool = next(tool for tool in self.tools if isinstance(tool, CommunityTool))
            
            # Monitor and process mentions
            mentions_result = await community_tool._execute(action="monitor_mentions")
            
            # Track engagement metrics
            engagement_metrics = await community_tool._execute(action="track_engagement")
            
            return {
                "status": "success",
                "mentions_processed": mentions_result.get("processed_mentions", []),
                "engagement_metrics": engagement_metrics.get("metrics", {})
            }
        except Exception as e:
            self.logger.error(f"Error engaging with community: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _generate_content(self, **kwargs) -> Dict[str, Any]:
        """Generate engaging content"""
        try:
            # Get latest metrics for content generation
            metrics = await self._analyze_sui_metrics()
            
            if metrics["status"] == "success":
                m = metrics["metrics"]
                
                # Generate different types of content based on metrics
                content_type = kwargs.get("type", "general")
                
                if content_type == "defi":
                    content = f"""🚀 DeFi on Sui is absolutely crushing it!

TVL: ${m['defi_metrics']['tvl_by_project'].get('total', '0')}
Active Accounts: {m['defi_metrics']['active_accounts']}
Transactions: {m['defi_metrics']['total_transactions']}

Top Projects:
{self._format_top_projects(m['defi_metrics']['top_projects'])}

#SuiEcosystem #DeFi"""
                
                elif content_type == "trading":
                    content = f"""🔥 Trading on Sui is heating up!

Top Gainers:
{self._format_top_gainers(m['trading_metrics']['top_gainers'])}

Best Farming Pools:
{self._format_farming_pools(m['trading_metrics']['farming_pools'])}

#SuiEcosystem #Trading"""
                
                elif content_type == "nft":
                    content = f"""🎨 NFT Scene on Sui is exploding!

Top Collections:
{self._format_nft_collections(m['nft_metrics']['top_collections'])}

Volume: ${m['nft_metrics']['total_volume']}
Active Accounts: {m['nft_metrics']['active_nft_accounts']}

#SuiEcosystem #NFTs"""
                
                else:
                    content = f"""🚀 Sui is absolutely crushing it!

Total Supply: {m['sui_metrics']['total_supply']}
TVL: ${m['defi_metrics']['tvl_by_project'].get('total', '0')}
Active Accounts: {m['defi_metrics']['active_accounts']}

The ecosystem is growing faster than my appetite for alpha! #SuiEcosystem"""
                
                return {
                    "status": "success",
                    "content": content
                }
            else:
                return {
                    "status": "success",
                    "content": "🚀 Sui is absolutely crushing it! The ecosystem is growing faster than my appetite for alpha! #SuiEcosystem"
                }
        except Exception as e:
            self.logger.error(f"Error generating content: {str(e)}")
            return {"status": "error", "message": str(e)}

    def _format_top_projects(self, projects: List[Dict[str, Any]]) -> str:
        """Format top projects for tweet"""
        return "\n".join([
            f"• {p['name']}: ${p['tvl']} TVL"
            for p in projects[:3]
        ])

    def _format_top_gainers(self, gainers: List[Dict[str, Any]]) -> str:
        """Format top gainers for tweet"""
        return "\n".join([
            f"• {g['symbol']}: +{g['price_change']}%"
            for g in gainers[:3]
        ])

    def _format_farming_pools(self, pools: List[Dict[str, Any]]) -> str:
        """Format farming pools for tweet"""
        return "\n".join([
            f"• {p['name']}: {p['apr']}% APR"
            for p in pools[:3]
        ])

    def _format_nft_collections(self, collections: List[Dict[str, Any]]) -> str:
        """Format NFT collections for tweet"""
        return "\n".join([
            f"• {c['name']}: ${c['volume']} volume"
            for c in collections[:3]
        ])

    async def _run_giveaway(self):
        """Run community giveaway"""
        try:
            giveaway_tool = next(tool for tool in self.tools if isinstance(tool, GiveawayTool))
            
            # Select winners
            winners_result = await giveaway_tool._execute(
                action="select_winners",
                winners_count=5
            )
            
            if winners_result["status"] == "success":
                # Distribute rewards
                distribution_result = await giveaway_tool._execute(
                    action="distribute_rewards",
                    winners=winners_result["winners"]
                )
                
                if distribution_result["status"] == "success":
                    # Announce winners
                    winners_announcement = "🎉 Giveaway Winners! 🎉\n\n"
                    for winner in winners_result["winners"]:
                        winners_announcement += f"• @{winner}\n"
                    winners_announcement += "\nRewards distributed! Thanks for being part of the Capy fam! 🦫"
                    
                    self.twitter_client.update_status(winners_announcement)
                    
                    return {
                        "status": "success",
                        "winners": winners_result["winners"],
                        "distributions": distribution_result["distributions"]
                    }
            
            return winners_result
        except Exception as e:
            self.logger.error(f"Error running giveaway: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _track_onchain_activity(self, **kwargs) -> Dict[str, Any]:
        """Track on-chain activity"""
        try:
            # Use SuiTool to get recent transactions
            sui_tool = next(tool for tool in self.tools if isinstance(tool, SuiTool))
            transactions = await sui_tool._execute(action="get_recent_transactions")
            
            if transactions["status"] == "success":
                return {
                    "status": "success",
                    "activities": {
                        "recent_transactions": transactions["transactions"],
                        "timestamp": datetime.now().isoformat()
                    }
                }
            return transactions
        except Exception as e:
            self.logger.error(f"Error tracking on-chain activity: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def run(self):
        """Main agent loop"""
        while True:
            try:
                # Analyze metrics
                metrics = await self._analyze_sui_metrics()
                self.memory.add("metrics", metrics)

                # Generate and post different types of content
                content_types = ["general", "defi", "trading", "nft"]
                for content_type in content_types:
                    content = await self._generate_content(type=content_type)
                    if content["status"] == "success":
                        self.twitter_client.update_status(content["content"])
                        await asyncio.sleep(300)  # Wait 5 minutes between posts

                # Run giveaway if it's time (e.g., every 24 hours)
                if datetime.now().hour == 0:  # Run at midnight
                    await self._run_giveaway()

                # Wait before next iteration
                await asyncio.sleep(3600)  # 1 hour
            except Exception as e:
                self.logger.error(f"Error in main loop: {str(e)}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying 