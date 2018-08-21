import socket
import sys
import persistqueue
from persistqueue.exceptions import Empty


def post_to_irc(event):
    event_type = event['event']
    title = event['title']
    price = event['price']
    quant = event['quantity']
    link = event['link']

    if event_type == "added":
        message = "*\x0309Item Added\x03*   \x02{}\x02 - {} - (#: {}) - ({})\n".format(title, price, quant, link)
    elif event_type == "modified":
        message = "*\x0307Item Changed\x03* \x02{}\x02 - {} - (#: {}) - ({})\n".format(title, price, quant, link)
    elif event_type == "removed":
        message = "*\x0304Item Removed\x03* \x02{}\x02\n".format(title)

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
