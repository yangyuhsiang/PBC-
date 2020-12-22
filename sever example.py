import socket
import cv2 as cv
import numpy as np

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

TCP_IP = socket.gethostname()
TCP_PORT = 8002
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((TCP_IP, TCP_PORT))
server.listen(5)
conn, addr = server.accept()
while True:
    length = recvall(conn,16)
    stringData = recvall(conn, int(length))
    data = np.frombuffer(stringData, dtype='uint8')
    decimg=cv.imdecode(data,1)
    cv.imshow('SERVER',decimg)
    key = cv.waitKey(1)
    if key == ord('q'):
        print('first img receive and close')
        break

gray_decimg = cv.cvtColor(decimg, cv.COLOR_BGR2GRAY)  # test 把原本的照片變成黑白的當作測試

while True:  # 把處理好的照片傳到client
    result, imgencode_server = cv.imencode('.jpg', gray_decimg)
    data_server = np.array(imgencode_server)
    stringData_server = data_server.tobytes()
    conn.send( str(len(stringData_server)).ljust(16).encode())
    conn.send(stringData_server)
    print('second img send to client')



server.close()  # test





