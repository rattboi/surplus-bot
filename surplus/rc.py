import json
import requests
import persistqueue
import sys
from persistqueue.exceptions import Empty
try:
    import secret as secret
except:
    import surplus.secret as secret

def post_to_rc(event):
    rc_hook_url = secret.rc_hook_url

    event_type = event['event']
    title = event['title']
    price = event['price']
    quant = event['quantity']
    link = event['link']
    image = event['image']

    if event_type == "added":
        color = "#00ff00"
        text = "*Item Added* [Link]({})".format(link)
    elif event_type == "modified":
        color = "#ffff00"
        text = "*Item Changed* [Link]({})".format(link)
    elif event_type == "removed":
        color = "#ff0000"
        text = "*Item Removed*"
    else:
        color = "#0000ff"  # What's this? Just in case, I guess

    fallback = "{} - {} (#: {}): {}".format(title, price, quant, link)

    rc_data = {
        "text": text,
        "attachments": [{
            "fallback": fallback,
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
        rc_hook_url, data=json.dumps(rc_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to Rocket.Chat returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
    )

def main():
    q = persistqueue.SQLiteQueue('db/rc', auto_commit=True)

    while True:
        try:
            event = q.get(block=False)
            print("Posting '{}' event to Rocket.Chat".format(event['event']))
            post_to_rc(event)
        except Empty:
            print("No more events to process")
            sys.exit();

main()
