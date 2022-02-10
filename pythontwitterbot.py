
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import tweepy
import logging
import time

print("Initialising the Model 1/2")
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
print("Initialising the Model 2/2")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")
print("Initialising done!")


def take_command(command):
    new_user_input_ids = tokenizer.encode(command + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat([new_user_input_ids], dim=-1)
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    text = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return text


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
try:
    api.verify_credentials()
except Exception as e:
    logger.error("Error creating API", exc_info=True)
    raise e
logger.info("API created")


def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")

            if not tweet.user.following:
                tweet.user.follow()
            command = tweet.text.lower()
            command = command.replace('#askme','')
            command = command.replace('@puramnihal','').strip()
            print(command)
            api.update_status(
                status=take_command(command),
                in_reply_to_status_id=tweet.id,
            )
    return new_since_id

def main():
    since_id = 1
    while True:
        since_id = check_mentions(api, ["#askme"], since_id)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()




