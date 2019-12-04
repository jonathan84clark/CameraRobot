import socket

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
Message = [81, 12, 0, 0, 0, 0, 0, 0]


data = bytearray(Message)
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

clientSock.sendto(data, (UDP_IP_ADDRESS, UDP_PORT_NO))