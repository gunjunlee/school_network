# client.py
import socket
import time
from datetime import datetime
import threading
import getopt
import sys

#두 datetime 간의 차이(단위: millisecond)를 구함
def difftimemilli(dt_after, dt_before):
    dt = dt_after - dt_before;
    milli = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return milli

#패킷을 서버에 전송하고 받는 함수
def ping(RTTlist, sock, i):

    # seq#가 기록되어 있는 message 생성
    message = "Ping #" + str(i)
    try:
        #패킷 전송 직전 시간
        dt_before = datetime.now();

        #패킷 송신
        sock.sendto(message.encode(), (server_ip, server_port))
        print ("Client: send \"" + message + "\"")

        #답장되어 오는 패킷 수신.
        data, addr = sock.recvfrom(1024)

        #패킷 수신 직후 시간
        dt_after = datetime.now()

        #패킷 송신 직전과 수신 직후 시간 차이(=RTT) 구함
        dt_diff = difftimemilli(dt_after, dt_before)
        print ("Client: recv \"" + data.decode('utf-8') + "\" diff: " + str(dt_diff))

        #패킷 잘 받았을 경우 RTT 기록함
        RTTlist.append(dt_diff)

    #패킷 드랍된 경우 처리
    except Exception as e:
        print("package dropped: seq#", i)
        print(e)

#waittime 기본값 1000ms
waittime = 1

#opt 설정
try:
    opts, args = getopt.getopt(sys.argv[1:], "c:p:w:")
#설정 안 된 opt 있을 경우 예외 처리
except getopt.GetoptError as err:
    print(str(err))
    exit()
#opt 받아 옴
for opt, arg in opts:
    if(opt == "-c"):
        server_ip = str(arg)
    elif(opt == "-p"):
        server_port = int(arg)
    elif(opt == "-w"):
        waittime = float(arg) / 1000

#RTT 저장하기 위한 리스트
RTTlist = []

#server_ip 설정되지 않은 경우 처리
if 'server_ip' in globals():
    pass
else:
    print("server_ip is not defined")
    exit()

#server_port 설정되지 않은 경우 처리
if 'server_port' in globals():
    pass
else:
    print("server_port is not defined")
    exit()

#UDP 소켓 엶
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#UPD timeout 값 설정
sock.settimeout(waittime)

#스레드 리스트
threadlist = []

#패킷 전송 스레드 10개 생성
for i in range(0, 10):
    t = threading.Thread(target=ping, args=(RTTlist, sock, i))
    threadlist.append(t)
    t.start()

#모든 스레드 종료 기다림.
for i in range(0, 10):
    threadlist[i].join()

#모든 패킷이 timeout 된 경우 처리.
if(len(RTTlist) == 0):
    print("there is no packet replied, cannot get average RTT")
    exit()

#UDP 소켓 닫음.
sock.close()

#averageRTT 구함
sumRTT = 0
averageRTT = 0
for i in RTTlist:
    sumRTT = sumRTT + i

averageRTT = sumRTT / len(RTTlist)

print("average of RTTs:", averageRTT)
