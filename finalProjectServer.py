import socket
import numpy as np
import cv2 as cv
import threading
from PIL import Image

def start():
    global conn1
    global conn2
    global addr1
    global addr2
    print("[STARTING] server is starting...")
    server.listen(2)
    print(f'Server is listening on {SERVER}')
    conn1, addr1 = server.accept()
    print('Connected to:', addr1)
    conn1.send("You're Connected!".encode())
    conn1.send('1'.encode())
    conn2, addr2 = server.accept()
    print('Connected to:', addr2)
    conn2.send("You're Connected!".encode())
    conn2.send('2'.encode())


# def check_connection():
#     while True:
#         try:
#             conn1.send("bytes").encode()
#             conn2.send("bytes").encode()
#         except:
#             start()
#             connectionChecker.start()

'''
Connection initiated
'''
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
start()
# connectionChecker=threading.Thread(target = check_connection)
# connectionChecker.start()

# Game mode selection. 0 for bo3, 1 for bo5, 2 for bo7.
while True:
    gameMode = conn1.recv(2048).decode(FORMAT)
    modeString = ''
    if gameMode == '0':
        modeString = "Best of Three"
    elif gameMode == '1':
        modeString = "Best of Five"
    elif gameMode == '2':
        modeString = "Best of Seven"

    print(modeString)

    conn2.send(str(gameMode).encode())
    conn2.send(str(addr1[0]).encode())
    modeDecision = conn2.recv(2048).decode(FORMAT)
    print(modeDecision)
    if modeDecision == 'Y':
        print('Player 2 accept gamemode')
        conn1.send('Y'.encode())
        break
    else:
        print('Player 2 denied gamemode. ')
        conn1.send('N'.encode())
        continue

print('Game Start!')

'''
Game start. Start receiving image and game decision
'''
conn1Win = 0
conn2Win = 0
while True:
    ans1 = conn1.recv(2048).decode(FORMAT)
    print(ans1)
    ans2 = conn2.recv(2048).decode(FORMAT)
    print(ans2)

# Determine game outcome
    winner = -1

    if ans1 != 'R' and ans1 != 'P' and ans1 != 'S':
        print('Value Error')
        continue
    elif ans2 != 'R' and ans2 != 'P' and ans2 != 'S':
        print('Value Error')
        continue
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
        conn1.send('D'.encode())
        conn2.send('D'.encode())
    elif winner == 0:
        conn1Win += 1
        print('Player 1', conn1Win)
        print('Player 2', conn2Win)
        if conn1Win == 2 and gameMode == '0':
            conn1.send('BW'.encode())
            conn2.send('BL'.encode())
            break
        elif conn1Win == 3 and gameMode == '1':
            conn1.send('BW'.encode())
            conn2.send('BL'.encode())
            break
        elif conn1Win == 4 and gameMode == '2':
            conn1.send('BW'.encode())
            conn2.send('BL'.encode())
            break
        else:
            conn1.send('W'.encode())
            conn2.send('L'.encode())
            continue
    elif winner == 1:
        conn2Win += 1
        print('Player 1', conn1Win)
        print('Player 2', conn2Win)
        if conn2Win == 2 and gameMode == '0':
            conn1.send('BL'.encode())
            conn2.send('BW'.encode())
            break
        elif conn2Win == 3 and gameMode == '1':
            conn1.send('BL'.encode())
            conn2.send('BW'.encode())
            break
        elif conn2Win == 4 and gameMode == '2':
            conn1.send('BL'.encode())
            conn2.send('BW'.encode())
            break
        else:
            conn1.send('L'.encode())
            conn2.send('W'.encode())
            continue

print('Over')

'''
Restart after game conclude or not (incomplete)
'''
# res1 = conn1.recv(2048).decode(FORMAT)
# res2 = conn2.recv(2048).decode(FORMAT)
# print(res1)
# print(res2)
# if res1 == 'Y' and res2 == 'Y':
#     conn1.send("Restart!".encode())
#     conn2.send("Restart!".encode())
#     continue
# else:
#     break
