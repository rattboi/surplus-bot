from slackish import SlackishEmitter
import secret as secret

class SlackEmitter(SlackishEmitter):
    def format(self, event_type, event):
        colors = {
            'added':    "#00ff00",
            'modified': "#ffff00",
            'removed':  "#ff0000"
        }

        texts = {
            'added':    f"*Item Added* (<{event['link']}|Link>)",
            'modified': f"*Item Changed* (<{event['link']}|Link>)",
            'removed':  f"*Item Removed*"
        }

        return {
            "unfurl_links": True,
            "attachments": [{
                "fallback": f"{event['title']} - {event['price']} (#: {event['quantity']}): {event['link']}",
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
                    "value": event['quantity'],
                    "short": True,
                }],
                "image_url": event['image'],
            }]
        }

if __name__=='__main__':
    SlackEmitter('slack', secret.webhook_url).emit()
