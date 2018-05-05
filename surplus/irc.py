import socket
import sys
import persistqueue
from persistqueue.exceptions import Empty


def post_to_irc(event):
    event_type = event['event']
    title = event['title']
    price = event['price']
    link = event['link']

    if event_type == "added":
        message = "*Item Added*   {} - {} - ({})\n".format(title, price, link)
    elif event_type == "removed":
        message = "*Item Removed* {}\n".format(title)

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 12345)
    sock.connect(server_address)

    try:
        # Send data
        sock.send(message.encode())
    finally:
        sock.close()


def main():
    q = persistqueue.SQLiteQueue('db/irc', auto_commit=True)

    while True:
        try:
            event = q.get(block=False)
            print("Posting '{}' event to IRC".format(event['event']))
            post_to_irc(event)
        except Empty:
            print("No more events to process")
            sys.exit()


main()
