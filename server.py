# server.py
import socket
import time
import threading
import random

#딜레이를 가지고 패킷 답장하는 함수
def sendtoDelay(sock, data, addr):
	print ("Server: recv \"" + data.decode('utf-8') + "\"")

	#0.2의 확률로 패킷 드랍
	if(random.randrange(1, 6) < 5):
		#0~1초 사이에서 uniform distribution 따르도록 delay 줌
		time.sleep(random.uniform(0, 2))
		#패킷 답장
		sock.sendto(data, addr)
		print ("Server: reply \"" + data.decode('utf-8') + "\"")
	else:
		print("Server: drop \"" + data.decode('utf-8') + "\"")

server_ip = "127.0.0.1"
server_port = 5005

#UDP socket 엶
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#UDP socket을 지정한 port와 bind함.
sock.bind((server_ip, server_port))

while True:
	#패킷 수신
	data, addr = sock.recvfrom(1024)

	#패킷 답장하는 스레드 생성 및 시작
	t1 = threading.Thread(target=sendtoDelay, args=(sock, data, addr))
	t1.start()

raw_input("server exit")

#소켓 닫음
sock.close()
