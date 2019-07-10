import sys

import persistqueue
from persistqueue.exceptions import Empty

class Emitter():
    def __init__(self, name):
        self.name = name
        self.q = persistqueue.SQLiteQueue("db/{}".format(name), auto_commit=True)

    def emit(self):
        while True:
            try:
                event = self.q.get(block=False)
                print("Posting '{}' event to {}".format(event['event'], self.name))
                self.post(event)
            except Empty:
                print("No more events to process")
                sys.exit()

    def parse(self, event):
        event_type = event['event']
        return self.format(event_type, event)

    def post(self, event):
        pass

