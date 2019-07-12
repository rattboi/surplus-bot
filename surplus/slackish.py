import json
import requests

from emitter import Emitter

class SlackishEmitter(Emitter):
    def __init__(self, name, webhook):
        self.webhook = webhook
        super().__init__(name)


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
