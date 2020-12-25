import socket
import numpy as np
import cv2 as cv
import threading
from PIL import Image
from queue import Queue


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf


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


def check_connection():
    while True:
        try:
            conn1.send("bytes").encode()
            conn2.send("bytes").encode()
        except:
            HEADER = 64
            PORT = 5050
            SERVER = socket.gethostbyname(socket.gethostname())
            ADDR = (SERVER, PORT)
            FORMAT = 'utf-8'
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(ADDR)
            start()


# Image processed and merge forfurther usage
# Read the two images
def combine_image(photo1, photo2):
    image1 = photo1
    image1.show()
    image2 = photo2
    image2.show()
# resize, first image
    image1 = image1.resize((426, 240))
    image1_size = image1.size
    image2_size = image2.size
    new_image = Image.new(
                'RGB', (2*image1_size[0], image1_size[1]), (250, 250, 250))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1_size[0], 0))
    new_image.show()
    return new_image

connectionChecker = threading.Thread(target=check_connection)
# connectionChecker.start()

# def rec1():
#     ans1 = conn1.recv(2048).decode(FORMAT)
#     return ans1


# def rec2():
#     ans2 = conn2.recv(2048).decode(FORMAT)
#     return ans2

# getAns1 = threading.Thread(target=rec1)
# getAns2 = threading.Thread(target=rec2)


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

# Game mode selection. 0 for bo3, 1 for bo5, 2 for bo7.
# conn1.send("Please select game mode.".encode())
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
    elif modeDecision == 'N':
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
    # msg_length1 = conn1.recv(HEADER).decode(FORMAT)
    # if msg_length1:
    #     msg_length1 = int(msg_length1)

    # getAns1.start()
    ans1 = conn1.recv(2048).decode(FORMAT)
    print(ans1)

   

    # msg_length2 = conn2.recv(HEADER).decode(FORMAT)
    # if msg_length2:
    #     msg_length2 = int(msg_length2)

    # getAns2.start()
    ans2 = conn2.recv(2048).decode(FORMAT)
    print(ans2)
    
    

    # getAns2.join()


# Determine game outcome


    # ans1 = ans1.strip()
    # ans2 = ans2.strip()
    winner = -1

    if ans1 != 'R' and ans1 != 'P' and ans1 != 'S':
        print('Value Error')
        conn1.send('Bad Value'.encode())
        continue
    elif ans2 != 'R' and ans2 != 'P' and ans2 != 'S':
        print('Value Error')
        conn2.send('Bad Value'.encode())
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
        # conn1.send(new_image)
        conn2.send('D'.encode())
        # conn2.send(new_image)
    elif winner == 0:
        conn1Win += 1
        print('Player 1', conn1Win)
        print('Player 2', conn2Win)
        if conn1Win == 2:
            if gameMode == '0':
                conn1.send('BW'.encode())
                length1 = recvall(conn1, 16)
                stringData1 = recvall(conn1, int(length1))
                data1 = np.frombuffer(stringData1, dtype='uint8')
                decimg1 = cv.imdecode(data1, 1)
                cv.imshow('SERVER', decimg1)
                key1 = cv.waitKey(1)
                if key1 == ord('q'):
                    print('first img receive and close')
                conn2.send('BL'.encode())
                length2 = recvall(conn2, 16)
                stringData2 = recvall(conn2, int(length2))
                data2 = np.frombuffer(stringData2, dtype='uint8')
                decimg2 = cv.imdecode(data2, 1)
                cv.imshow('SERVER1', decimg2)
                key2 = cv.waitKey(1)
                if key2 == ord('q'):
                    print('first img receive and close')
            break
        elif conn1Win == 3:
            if gameMode == '1':
                conn1.send('BW'.encode())
                length1 = recvall(conn1, 16)
                stringData1 = recvall(conn1, int(length1))
                data1 = np.frombuffer(stringData1, dtype='uint8')
                decimg1 = cv.imdecode(data1, 1)
                cv.imshow('SERVER', decimg1)
                key1 = cv.waitKey(1)
                if key1 == ord('q'):
                    print('first img receive and close')
                conn2.send('BL'.encode())
                length2 = recvall(conn2, 16)
                stringData2 = recvall(conn2, int(length2))
                data2 = np.frombuffer(stringData2, dtype='uint8')
                decimg2 = cv.imdecode(data2, 1)
                cv.imshow('SERVER1', decimg2)
                key2 = cv.waitKey(1)
                if key2 == ord('q'):
                    print('first img receive and close')
            break
        elif conn1Win == 4:
            if gameMode == '2':
                conn1.send('BW'.encode())
                length1 = recvall(conn1, 16)
                stringData1 = recvall(conn1, int(length1))
                data1 = np.frombuffer(stringData1, dtype='uint8')
                decimg1 = cv.imdecode(data1, 1)
                cv.imshow('SERVER', decimg1)
                key1 = cv.waitKey(1)
                if key1 == ord('q'):
                    print('first img receive and close')
                conn2.send('BL'.encode())
                length2 = recvall(conn2, 16)
                stringData2 = recvall(conn2, int(length2))
                data2 = np.frombuffer(stringData2, dtype='uint8')
                decimg2 = cv.imdecode(data2, 1)
                cv.imshow('SERVER1', decimg2)
                key2 = cv.waitKey(1)
                if key2 == ord('q'):
                    print('first img receive and close')
            break
        else:
            conn1.send('W'.encode())
            # conn1.send(new_image)
            conn2.send('L'.encode())
            # conn2.send(new_image)

    elif winner == 1:
        conn2Win += 1
        print('Player 1', conn1Win)
        print('Player 2', conn2Win)
        if conn2Win == 2:
            if gameMode == '0':
                conn1.send('BL'.encode())
                length1 = recvall(conn1, 16)
                stringData1 = recvall(conn1, int(length1))
                data1 = np.frombuffer(stringData1, dtype='uint8')
                decimg1 = cv.imdecode(data1, 1)
                cv.imshow('SERVER', decimg1)
                key1 = cv.waitKey(1)
                if key1 == ord('q'):
                    print('first img receive and close')
                conn2.send('BW'.encode())
                length2 = recvall(conn2, 16)
                stringData2 = recvall(conn2, int(length2))
                data2 = np.frombuffer(stringData2, dtype='uint8')
                decimg2 = cv.imdecode(data2, 1)
                cv.imshow('SERVER1', decimg2)
                key2 = cv.waitKey(1)
                if key2 == ord('q'):
                    print('first img receive and close')
            break
        elif conn2Win == 3:
            if gameMode == '1':
                conn1.send('BL'.encode())
                length1 = recvall(conn1, 16)
                stringData1 = recvall(conn1, int(length1))
                data1 = np.frombuffer(stringData1, dtype='uint8')
                decimg1 = cv.imdecode(data1, 1)
                cv.imshow('SERVER', decimg1)
                key1 = cv.waitKey(1)
                if key1 == ord('q'):
                    print('first img receive and close')
                conn2.send('BW'.encode())
                length2 = recvall(conn2, 16)
                stringData2 = recvall(conn2, int(length2))
                data2 = np.frombuffer(stringData2, dtype='uint8')
                decimg2 = cv.imdecode(data2, 1)
                cv.imshow('SERVER1', decimg2)
                key2 = cv.waitKey(1)
                if key2 == ord('q'):
                    print('first img receive and close')
            break
        elif conn2Win == 4:
            if gameMode == '2':
                conn1.send('BL'.encode())
                length1 = recvall(conn1, 16)
                stringData1 = recvall(conn1, int(length1))
                data1 = np.frombuffer(stringData1, dtype='uint8')
                decimg1 = cv.imdecode(data1, 1)
                cv.imshow('SERVER', decimg1)
                key1 = cv.waitKey(1)
                if key1 == ord('q'):
                    print('first img receive and close')
                conn2.send('BW'.encode())
                length2 = recvall(conn2, 16)
                stringData2 = recvall(conn2, int(length2))
                data2 = np.frombuffer(stringData2, dtype='uint8')
                decimg2 = cv.imdecode(data2, 1)
                cv.imshow('SERVER1', decimg2)
                key2 = cv.waitKey(1)
                if key2 == ord('q'):
                    print('first img receive and close')
            break
        else:
            conn1.send('L'.encode())
            # conn1.send(new_image)
            conn2.send('W'.encode())
            # conn2.send(new_image)
decimg1 = cv.cvtColor(decimg1, cv.COLOR_BGR2RGB)
decimg2 = cv.cvtColor(decimg1, cv.COLOR_BGR2RGB)
img1 = Image.fromarray(decimg1)
img2 = Image.fromarray(decimg2)
img1rgb = img1.convert('RGB')
img2rgb = img2.convert('RGB')
cv.imshow('er', combine_image(img1rgb, img2rgb))
key1 = cv.waitKey(1)

while True:
    result, imgencode = cv.imencode('.jpg', combine_image(img1rgb, img2rgb))
    data = np.array(imgencode)
    stringData = data.tobytes()
    conn1.send(str(len(stringData)).ljust(16).encode())
    conn1.send(stringData)
    conn2.send(str(len(stringData)).ljust(16).encode())
    conn2.send(stringData)

print('Over')


    # if gameMode == 0:
    #     if conn1Win == 2:
    #         conn1.send('You WON !!!'.encode())
    #         conn2.send('You LOSE!!!'.encode())
    #     elif conn2Win == 2:
    #         conn1.send('You LOSE!!!'.encode())
    #         conn2.send('You WON!!!'.encode())
    #     else:
    #         continue
    # elif gameMode == 1:
    #     if conn1Win == 3:
    #         conn1.send('You WON !!!'.encode())
    #         conn2.send('You LOSE!!!'.encode())
    #     elif conn2Win == 3:
    #         conn1.send('You LOSE!!!'.encode())
    #         conn2.send('You WON!!!'.encode())
    #     else:
    #         continue
    # elif gameMode == 3:
    #     if conn1Win == 4:
    #         conn1.send('You WON !!!'.encode())
    #         conn2.send('You LOSE!!!'.encode())
    #     elif conn2Win == 4:
    #         conn1.send('You LOSE!!!'.encode())
    #         conn2.send('You WON!!!'.encode())
    #     else:
    #         continue
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
