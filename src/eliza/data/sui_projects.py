from typing import Dict, Any, List

SUI_PROJECTS: Dict[str, Dict[str, Any]] = {
    "cetus": {
        "name": "Cetus",
        "description": "Leading DEX and liquidity protocol on Sui",
        "features": [
            "Spot trading with deep liquidity",
            "Concentrated liquidity AMM",
            "Yield farming opportunities",
            "Cross-chain bridging"
        ],
        "aspect": "DeFi trading",
        "value": "efficient and secure trading infrastructure",
        "website": "https://cetus.zone",
        "twitter": "@CetusProtocol"
    },
    "navi": {
        "name": "Navi Protocol",
        "description": "Lending and borrowing protocol on Sui",
        "features": [
            "Lending and borrowing",
            "Liquidation protection",
            "Yield optimization",
            "Multi-collateral support"
        ],
        "aspect": "DeFi lending",
        "value": "decentralized lending infrastructure",
        "website": "https://naviprotocol.io",
        "twitter": "@NaviProtocol"
    },
    "sui": {
        "name": "Sui",
        "description": "Layer 1 blockchain designed for high performance",
        "features": [
            "Parallel transaction processing",
            "Object-centric data model",
            "Move programming language",
            "Horizontal scalability"
        ],
        "aspect": "blockchain technology",
        "value": "next-generation blockchain infrastructure",
        "website": "https://sui.io",
        "twitter": "@SuiNetwork"
    },
    "aftermath": {
        "name": "Aftermath Finance",
        "description": "DeFi aggregator and yield optimizer",
        "features": [
            "Yield optimization",
            "DeFi aggregation",
            "Staking rewards",
            "Cross-protocol strategies"
        ],
        "aspect": "DeFi optimization",
        "value": "optimized yield generation",
        "website": "https://aftermath.finance",
        "twitter": "@AftermathFi"
    },
    "turbos": {
        "name": "Turbos Finance",
        "description": "Perpetual futures DEX on Sui",
        "features": [
            "Perpetual futures trading",
            "Leverage trading",
            "Cross-margin support",
            "Advanced order types"
        ],
        "aspect": "derivatives trading",
        "value": "advanced trading capabilities",
        "website": "https://turbos.finance",
        "twitter": "@TurbosFinance"
    }
}

# Technical explanations for common topics
TECHNICAL_EXPLANATIONS: Dict[str, str] = {
    "staking": """Staking on Sui involves locking your SUI tokens to help secure the network and earn rewards. 
    Validators process transactions and maintain the network, while delegators can stake their tokens with validators 
    to earn a share of the rewards.""",
    
    "move": """Move is Sui's native programming language, designed specifically for blockchain development. 
    It features strong type safety, resource-oriented programming, and built-in security features to prevent 
    common blockchain vulnerabilities.""",
    
    "parallel": """Sui's parallel transaction processing allows multiple transactions to be processed simultaneously 
    when they don't conflict with each other. This is achieved through the object-centric data model and 
    Byzantine Consistent Broadcast.""",
    
    "object": """Sui uses an object-centric data model where all data is stored as objects. Each object has a 
    unique ID and can be owned by an address. This model enables parallel transaction processing and better 
    scalability compared to account-based models."""
}

# Common token symbols and their full names
TOKEN_INFO: Dict[str, Dict[str, str]] = {
    "sui": {
        "name": "Sui",
        "description": "Native token of the Sui blockchain",
        "contract": "0x2::sui::SUI"
    },
    "cetus": {
        "name": "CETUS",
        "description": "Governance token of Cetus Protocol",
        "contract": "0x6864a6fee92142e08a9271a9d43dbe1f1b9b0c1a"
    },
    "navi": {
        "name": "NAVI",
        "description": "Governance token of Navi Protocol",
        "contract": "0x2::navi::NAVI"
    }
} 