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
        text = "*Item Added* [Link]({})".format(link)
    elif event_type == "modified":
        text = "*Item Changed* [Link]({})".format(link)
    elif event_type == "removed":
        text = "*Item Removed*"

    rc_data = {
        "text": text
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
