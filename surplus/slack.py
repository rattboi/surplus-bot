import json
import requests
import persistqueue
import sys
from persistqueue.exceptions import Empty
import surplus.secret as secret

def post_to_slack(event):
    webhook_url = secret.webhook_url

    event_type = event['event']
    title = event['title']
    price = event['price']
    link = event['link']
    image = event['image']

    if event_type == "added":
        color = "#00ff00"
        text = "*Item Added* (<{}|Link>)".format(link)
    elif event_type == "removed":
        text = "*Item Removed*"
        color = "#ff0000"
    else:
        color = "#0000ff" #What's this? Just in case, I guess

    fallback = "{} - {}: {}".format(title, price, link)

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

def main():
    q = persistqueue.SQLiteQueue('db/slack', auto_commit=True)

    while True:
        try:
            event = q.get(block=False)
            print("Posting '{}' event to Slack".format(event['event']))
            post_to_slack(event)
        except Empty:
            print("No more events to process")
            sys.exit();

main()
