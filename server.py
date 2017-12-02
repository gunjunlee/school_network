# server_skel.py
import socket
import time
import threading
import random

def sendtoDelay(sock, data, addr):
	print ("Server: recv \"" + data.decode('utf-8') + "\"")
	if(random.randrange(1, 6) < 5):
		time.sleep(random.random())
		sock.sendto(data, addr)
		print ("Server: reply \"" + data.decode('utf-8') + "\"")
	else:
		print("Server: drop \"" + data.decode('utf-8') + "\"")

server_ip = "127.0.0.1"
server_port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_ip, server_port))

while True:
	data, addr = sock.recvfrom(1024)
	# print ("Server: recv \"" + data.decode('utf-8') + "\"")
	# time.sleep(0.5)
	# sock.sendto(data, addr)
	# print ("Server: reply \"" + data.decode('utf-8') + "\"")
	t1 = threading.Thread(target=sendtoDelay, args=(sock, data, addr))
	t1.start()

raw_input("server exit")
