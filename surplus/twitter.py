import os
import time
import requests
import tweepy

from emitter import Emitter
from secret import *

class TwitterEmitter(Emitter):
    def __init__(self, name, api):
        self.api = api
        super().__init__(name)

    def format(self, event_type, event):
        if event_type == "added":
            return f"*Item Added*\n{event['title']} - {event['price']} - (#: {event['quantity']}) - ({event['link']})"
        elif event_type == "modified":
            return f"*Item Changed*\n{event['title']} - {event['price']} - (#: {event['quantity']}) - ({event['link']})"
        elif event_type == "removed":
            return f"*Item Removed*\n{event['title']}"

    def post(self, event):
        message = self.parse(event)

        filename = 'temp.jpg'
        try:
            request = requests.get(image, stream=True)
            if request.status_code == 200:
                with open(filename, 'wb') as image:
                    for chunk in request:
                        image.write(chunk)
                api.update_with_media(filename, status=message)
        except Exception as e:
            # if there's an image problem, just post as a status
            api.update_status(message)
        finally:
            try:
                os.remove(filename)
            except OSError:
                pass
        time.sleep(15)

if __name__=='__main__':
    auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
    auth.set_access_token(twitter_token, twitter_token_secret)
    api = tweepy.API(auth)

    TwitterEmitter('twitter', api).emit()
