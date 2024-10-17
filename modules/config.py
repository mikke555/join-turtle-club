from sys import stderr

from inquirer import List
from loguru import logger

logger.remove()
logger.add(
    stderr,
    format="<white>{time:HH:mm:ss}</white> | <level>{message}</level>",
)

actions = [
    List(
        "user_action",
        message="Select action",
        choices=[
            "Use referral",
            "Parse accounts",
        ],
    )
]


chain_data = {
    "ethereum": {
        "rpc": "https://rpc.ankr.com/eth",
        "explorer": "https://etherscan.io",
        "token": "ETH",
        "chain_id": 1,
    },
    "base": {
        "rpc": "https://mainnet.base.org",
        "explorer": "https://basescan.org",
        "token": "ETH",
        "chain_id": 8453,
    },
    "arbitrum": {
        "rpc": "https://rpc.ankr.com/arbitrum",
        "explorer": "https://arbiscan.io",
        "token": "ETH",
        "chain_id": 42161,
    },
}
