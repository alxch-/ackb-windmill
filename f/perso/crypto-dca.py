import os
import wmill

import asyncio
import logging
import os
from distutils.util import strtobool
from urllib.parse import urlencode

import boto3
import ccxt.async_support as ccxt
import requests


logger = logging.getLogger()
logger.setLevel(os.environ.get("LOGGING_LEVEL", logging.INFO))

def main(symbol: str, funds: float) -> str:
    asyncio.get_event_loop().run_until_complete(
        buy_crypto(symbol, funds)
    )
    return f"successfully bought with {funds} on {symbol}"

async def buy_crypto(symbol, funds):
    exchange = get_coinbase_exchange()
    order = await exchange.create_market_buy_order(
        symbol, funds
    )
    await exchange.close()
    logger.info("exchange closed")
    return order


def get_coinbase_exchange():
    return ccxt.coinbase(
        {
            "enableRateLimit": True,
            "apiKey": wmill.get_variable("f/perso/coinbase_api_key_alex"),
            "secret": wmill.get_variable("f/perso/coinbase_secret_alex").replace('\\n', '\n'),
            "options": {
                "createMarketBuyOrderRequiresPrice": False
            }
        }
    )