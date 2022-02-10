import tweepy
import logging
import os

logger = logging.getLogger()

def create_api():
    consumer_key = "4giejc8xz8LDWDZ0fxEFN49kl"
    consumer_secret = "UN5JaNJ05yTxrPCsEWlIOUZIHbFHwIwCjT32J9moAJhLTmFQFw"
    access_token = "1272256398005432322-r9A9pXdl0r6oKSu0ZPnfQxDsZO1ghj"
    access_token_secret = "4Pq9B2ULDqZeorjCzBcp6H7kXRqL6mHLXhhhbxU7LX7v8"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api