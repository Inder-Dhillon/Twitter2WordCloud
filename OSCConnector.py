from pythonosc.udp_client import SimpleUDPClient

ip = '127.0.0.1'
port = 12001
address = "/keywords"
client = SimpleUDPClient(ip, port)  # Create client


def send(msg):
    client.send_message(address, msg)
    print("Message Sent to Processing!")
