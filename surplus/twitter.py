import os
import time
import requests
import tweepy

try:
    from emitter import Emitter
except:
    from surplus.emitter import Emitter

try:
    from surplus.secret import *
except:
    from secret import *

class TwitterEmitter(Emitter):
    def __init__(self, name, api):
        self.api = api
        super().__init__(name)

    def post(self, event):
        event_type = event['event']
        title = event['title']
        price = event['price']
        quant = event['quantity']
        image = event['image']
        link = event['link']

        if event_type == "added":
            message = "*Item Added*\n{} - {} - (#: ) - ({})".format(title, price, quant, link)
        if event_type == "modified":
            message = "*Item Changed*\n{} - {} - (#: ) - ({})".format(title, price, quant, link)
        elif event_type == "removed":
            message = "*Item Removed*\n{}".format(title)

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

    emitter = TwitterEmitter('twitter', api)
    emitter.emit()
