import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# def handle_client(conn, addr):
#     print(f"[NEW CONNECTION] {addr} connected.")
#
#     connected = True
#     while connected:
#         msg_length = conn.recv(HEADER).decode(FORMAT)
#         if msg_length:
#             msg_length = int(msg_length)
#             msg = conn.recv(msg_length).decode(FORMAT)
#             if msg == DISCONNECT_MESSAGE:
#                 connected = False
#
#             print(f"[{addr}] {msg}")
#             conn.send("Msg received".encode(FORMAT))
#
#     conn.close()
#
#
# def start():
#     server.listen()
#     print(f"[LISTENING] Server is listening on {SERVER}")
#     while True:
#         conn, addr = server.accept()
#         thread = threading.Thread(target=handle_client, args=(conn, addr))
#         thread.start()
#         print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
server.listen(2)
print(f'Server is listening on {SERVER}')
conn1, addr1 = server.accept()
print('Connected to:', addr1)
conn1.send("You're Connected!".encode())
conn2, addr2 = server.accept()
print('Connected to:', addr2)
conn2.send("You're Connected!".encode())

while True:
    # msg_length1 = conn1.recv(HEADER).decode(FORMAT)
    # if msg_length1:
    #     msg_length1 = int(msg_length1)
    ans1 = conn1.recv(2048).decode(FORMAT)

    # msg_length2 = conn2.recv(HEADER).decode(FORMAT)
    # if msg_length2:
    #     msg_length2 = int(msg_length2)
    ans2 = conn2.recv(2048).decode(FORMAT)

    winner = -1
    ans1 = ans1.strip()
    ans2 = ans2.strip()

    print(ans1)
    print(ans2)

    if ans1 != 'R' and ans1 != 'P' and ans1 != 'S':
        print('Value Error')
        conn1.send('Bad Value'.encode())
    elif ans2 != 'R' and ans2 != 'P' and ans2 != 'S':
        print('Value Error')
        conn2.send('Bad Value'.encode())
    else:
        if ans1 == "R" and ans2 == "S":
            winner = 0
        elif ans1 == "S" and ans2 == "R":
            winner = 1
        elif ans1 == "P" and ans2 == "R":
            winner = 0
        elif ans1 == "R" and ans2 == "P":
            winner = 1
        elif ans1 == "S" and ans2 == "P":
            winner = 0
        elif ans1 == "P" and ans2 == "S":
            winner = 1
    if winner == -1:
        conn1.send('Draw. Reset Game? Y/N'.encode())
        conn2.send('Draw. Reset Game? Y/N'.encode())
    elif winner == 0:
        conn1.send('You WON!!! Reset Game? Y/N'.encode())
        conn2.send('You LOSE!!! Reset Game? Y/N'.encode())
    elif winner == 1:
        conn1.send('You LOSE!!! Reset Game? Y/N'.encode())
        conn2.send('You WON!!! Reset Game? Y/N'.encode())

    res1 = conn1.recv(2048).decode(FORMAT)
    res2 = conn2.recv(2048).decode(FORMAT)
    print(res1)
    print(res2)
    if res1 == 'Y' and res2 == 'Y':
        conn1.send("Restart!".encode())
        conn2.send("Restart!".encode())
        continue
    else:
        break
