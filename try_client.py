import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
# Change to local ipv4 ip address before execution
SERVER = "10.45.251.147"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print(client.recv(2048).decode(FORMAT))

def send(msg):
    message = msg.encode(FORMAT)
    # msg_length = len(message)
    # send_length = str(msg_length).encode(FORMAT)
    # send_length += b' ' * (HEADER - len(send_length))
    # client.send(send_length)
    client.send(message)


while True:
    message = input()
    if message == "Disconnect" or message == "N":
        client.shutdown()
        client.close()
        break
    else:
        send(message)
        print(client.recv(2048).decode(FORMAT))
