import json
import requests

from emitter import Emitter
import secret as secret

class SlackEmitter(Emitter):
    def __init__(self, name, webhook):
        self.webhook = webhook
        super().__init__(name)

    def format(self, event_type, event):
        colors = {
            'added':    "#00ff00",
            'modified': "#ffff00",
            'removed':  "#ff0000"
        }

        texts = {
            'added':    f"*Item Added* (<{event['link']}|Link>)"
            'modified': f"*Item Changed* (<{event['link']}|Link>)"
            'removed':  f"*Item Removed*"
        }

        return {
            "unfurl_links": True,
            "attachments": [{
                "fallback": f"{event['title']} - {event['price']} (#: {event['quant']}): {event['link']}",
                "pretext": texts[event_type],
                "color": colors[event_type],
                "fields": [{
                    "title": "Title",
                    "value": event['title'],
                    "short": True,
                },{
                    "title": "Price",
                    "value": event['price'],
                    "short": True,
                },{
                    "title": "Quantity",
                    "value": event['quant'],
                    "short": True,
                }],
                "image_url": event['image'],
            }]
        }

    def post(self, event):
        data = self.parse(event)

        response = requests.post(
            self.webhook, data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError(
                f"Request to {self.name} returned an error {response.status_code}, the response is:\n{response.text}"
        )

if __name__=='__main__':
    SlackEmitter('slack', secret.webhook_url).emit()
