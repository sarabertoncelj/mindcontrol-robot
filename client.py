# Echo client program
import socket
import pygame
import sys
import pygame.locals
import time
import struct
import numpy as np
from keras.models import model_from_json
from emokit.emotiv import Emotiv
from sklearn.externals import joblib

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

if __name__ == "__main__":

    # # load json and create model
    json_file = open('model20122-sara1912.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model20122-sara1912.h5")
    print("Loaded model from disk")

    #from sklearn.preprocessing import StandardScaler
    sc = joblib.load('scaler.save')


    HOST = '192.168.0.196'    # The remote host
    PORT = 50007              # The same port as used by the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        pygame.init()
        screen = pygame.display.set_mode((400, 300))
        run = True
        with Emotiv(display_output=False, verbose=True) as headset:
            levo = 0
            desno = 0
            naprej = 0
            lastcommand = 0
            while run:
                sendthis = None
                for event in pygame.event.get():
                    if event.type == pygame.locals.QUIT:
                        sendthis = 'ext'
                        send_msg(s, bytes(sendthis, encoding='utf-8'))
                        data = recv_msg(s)
                        pygame.quit(); sys.exit()
                        run = false
                packet = headset.dequeue()
                if packet is not None:
                    #print(dir(packet))
                    ps = packet.sensors

                    sensorData = [[ps['F3']['value'] * ps['F3']['quality'], ps['FC6']['value'] * ps['FC6']['quality'], ps['P7']['value'] * ps['P7']['quality'],ps['T8']['value'] * ps['T8']['quality'],
                        ps['F7']['value'] * ps['F7']['quality'], ps['F8']['value'] * ps['F8']['quality'], ps['T7']['value'] * ps['T7']['quality'], ps['P8']['value'] * ps['P8']['quality'],
                        ps['AF4']['value'] * ps['AF4']['quality'], ps['F4']['value'] * ps['F4']['quality'], ps['AF3']['value'] * ps['AF3']['quality'], ps['O2']['value'] * ps['O2']['quality'],
                        ps['O1']['value'] * ps['O1']['quality'], ps['FC5']['value'] * ps['FC5']['quality'], ps['X']['value'] * ps['X']['quality'], ps['Y']['value'] * ps['Y']['quality'],
                        0 * ps['Z']['quality'], ps['Unknown']['value'] * ps['Unknown']['quality']]]

                    sensorData = sc.transform(sensorData)
                    result = loaded_model.predict(sensorData)
                    print(result[0])
                    l = round(result[0][0])
                    n = round(result[0][1])
                    d = round(result[0][2])
                    if result[0][1] > result[0][2] and result[0][1] > result[0][0]:
                        naprej += 1
                        print('prdicted: naprej')
                    elif result[0][0] > result[0][1] and result[0][0] > result[0][2]:
                        levo = levo + 1
                        desno = 0
                        print('predicted: levo')
                    elif result[0][2] > result[0][0] and result[0][2] > result[0][1]:
                        desno = desno + 1
                        levo = 0
                        print('predicted: desno')
                    if levo > 3:
                        if lastcommand != 'l':
                            sendthis='l'
                            lastcommand = 'l'
                        print('left')
                        desno = 0
                        levo = 0
                        naprej = 0
                    if desno > 3:
                        if lastcommand != 'r':
                            sendthis='r'
                            lastcommand = 'r'
                        print('right')
                        desno = 0
                        levo = 0
                        naprej = 0
                    if naprej > 20:
                        if lastcommand != 'f':
                            sendthis='f'
                            lastcommand = 'f'
                        print('forward')
                        desno = 0
                        levo = 0
                        naprej = 0
                time.sleep(0.1)
                if sendthis != None: send_msg(s, bytes(sendthis, encoding='utf-8'))
