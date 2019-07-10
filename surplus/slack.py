import json
import requests

try:
    from emitter import Emitter
except:
    from surplus.emitter import Emitter

try:
    import secret as secret
except:
    import surplus.secret as secret

class SlackEmitter(Emitter):
    def post(self, event):
        webhook_url = secret.webhook_url

        event_type = event['event']
        title = event['title']
        price = event['price']
        quant = event['quantity']
        link = event['link']
        image = event['image']

        if event_type == "added":
            color = "#00ff00"
            text = "*Item Added* (<{}|Link>)".format(link)
        elif event_type == "modified":
            color = "#ffff00"
            text = "*Item Changed* (<{}|Link>)".format(link)
        elif event_type == "removed":
            color = "#ff0000"
            text = "*Item Removed*"
        else:
            color = "#0000ff"  # What's this? Just in case, I guess

        fallback = "{} - {} (#: {}): {}".format(title, price, quant, link)

        slack_data = {
            "unfurl_links": True,
            "attachments": [{
                "fallback": fallback,
                "pretext": text,
                "color": color,
                "fields": [{
                    "title": "Title",
                    "value": title,
                    "short": True,
                },{
                    "title": "Price",
                    "value": price,
                    "short": True,
                },{
                    "title": "Quantity",
                    "value": quant,
                    "short": True,
                }],
                "image_url": image,
            }]
        }

        response = requests.post(
            webhook_url, data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
        )

if __name__=='__main__':
    emitter = SlackEmitter('slack')
    emitter.emit()
