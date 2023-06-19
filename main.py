from datetime import datetime
import json, os
from mastodon import Mastodon
from dotenv import load_dotenv

load_dotenv()

# Set up Mastodon instance
mastodon = Mastodon(
    access_token=os.getenv('ACCESS_TOKEN'),
    api_base_url=os.getenv('BASE_URL')
)

file_name = 'tweets.js'

with open(file_name, "r") as tweets_file:
    tweets_lines = tweets_file.readlines()
# Replace header
tweets_lines[0] = tweets_lines[0].replace('window.YTD.tweet.part0 = ', '')
# Convert list back to text
tweets_data = ''.join(tweets_lines)
# Parse JSON twitter data
tweets = json.loads(tweets_data)
sorted_tweets = sorted(tweets, key=lambda x: datetime.strptime(x['tweet']['created_at'], "%a %b %d %H:%M:%S %z %Y"))

# Iterate over tweets and post them on Mastodon
for i, tweet in enumerate(sorted_tweets):
    # Extract tweet content
    content = tweet['tweet']['full_text'] + '\n\n#urdu #poetry #pakistan #islam #muslim'
    print(i, tweet['tweet']['created_at'], content[:64])
    # Create the status (post)
    status = mastodon.status_post(content)
    # Print the status ID of the created post
    print(f"Tweet with ID {status['id']} has been posted on Mastodon.")
