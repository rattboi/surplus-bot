import socket

try:
    from emitter import Emitter
except:
    from surplus.emitter import Emitter

class IrcEmitter(Emitter):
    def post(self, event):
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

if __name__=='__main__':
    emitter = IrcEmitter('irc')
    emitter.emit()
