from slackish import SlackishEmitter
import secret as secret

class RocketEmitter(SlackishEmitter):
    def format(self, event_type, event):
        colors = {
            'added':    "#00ff00",
            'modified': "#ffff00",
            'removed':  "#ff0000"
        }

        texts = {
            'added':    f"*Item Added* [{event['title']}]({event['link']})",
            'modified': f"*Item Changed* [{event['title']}]({event['link']})",
            'removed':  f"*Item Removed* {event['title']}"
        }

        return {
            "channel": "#surplus",
            "text": texts[event_type],
            "attachments": [{
                "fallback": f"{event['title']} - {event['price']} (#: {event['quantity']}): {event['link']}",
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
    RocketEmitter('rocket', secret.rocket_hook_url).emit()
