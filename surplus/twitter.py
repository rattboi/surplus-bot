import sys
import tweepy
import requests
import persistqueue
from persistqueue.exceptions import Empty

from surplus.secret import *


def post_to_twitter(api, event):
    event_type = event['event']
    title = event['title']
    price = event['price']
    image = event['image']
    link = event['link']

    if event_type == "added":
        message = "*Item Added*\n{} - {} - ({})".format(title, price, link)
    elif event_type == "removed":
        message = "*Item Removed*\n{}".format(title)

    try:
        filename = 'temp.jpg'
        request = requests.get(image, stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            api.update_with_media(filename, status=message)
    except e:
        # if there's an image problem, just post as a status
        api.update_status(message)
        try:
            os.remove(filename)
        except OSError:
            pass
    sleep(15)


def main():
    auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
    auth.set_access_token(twitter_token, twitter_token_secret)
    api = tweepy.API(auth)

    q = persistqueue.SQLiteQueue('db/twitter', auto_commit=True)

    while True:
        try:
            event = q.get(block=False)
            print("Posting '{}' event to Twitter".format(event['event']))
            post_to_twitter(api, event)
            return
        except Empty:
            print("No more events to process")
            sys.exit()


main()
