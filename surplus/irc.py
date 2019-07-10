import socket

from emitter import Emitter

class IrcEmitter(Emitter):
    def format(self, event_type, event):
        if event_type == "added":
            return f"*\x0309Item Added\x03*   \x02{event['title']}\x02 - {event['price']} - (#: {event['quant']}) - ({event['link']})\n"
        elif event_type == "modified":
            return f"*\x0307Item Changed\x03* \x02{event['title']}\x02 - {event['price']} - (#: {event['quant']}) - ({event['link']})\n"
        elif event_type == "removed":
            return f"*\x0304Item Removed\x03* \x02{event['title']}\n"

    def post(self, event):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 12345)
        sock.connect(server_address)

        try:
            # Send data
            sock.send(self.parse(event).encode())
        finally:
            sock.close()

if __name__=='__main__':
    IrcEmitter('irc').emit()
