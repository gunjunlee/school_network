# client_skel.py
import socket
import time
from datetime import datetime

def difftimemilli(dt_after, dt_before):
    dt = dt_after - dt_before;
    milli = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return milli

#dtb = datetime.now()
#time.sleep(1)
#dta = datetime.now()
#print(difftimemilli(dta, dtb))

server_ip = "127.0.0.1"
server_port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)

for i in range(0, 10):
    message = "Ping #" + str(i)

    try:
        dt_before = datetime.now();
        sock.sendto(message.encode(), (server_ip, server_port))
        print ("Client: send \"" + message + "\"")

        data, addr = sock.recvfrom(1024)
        dt_after = datetime.now()
        dt_diff = difftimemilli(dt_after, dt_before)
        #print ("Client: recv \"" + data.decode('utf-8') + "\" ")
        print ("Client: recv \"" + data.decode('utf-8') + "\" diff: " + str(dt_diff))
    except Exception as e:
        print("package dropped")
        print(e)
