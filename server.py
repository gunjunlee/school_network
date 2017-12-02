# server_skel.py
import socket
import time
import threading

def sendtoDelay(sock, data, addr):
	print ("Server: recv \"" + data.decode('utf-8') + "\"")
	time.sleep(0.5)
	sock.sendto(data, addr)
	print ("Server: reply \"" + data.decode('utf-8') + "\"")


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
	sendtoDelay(sock, data, addr)

raw_input("server exit")
