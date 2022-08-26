import socket
import sys
import json
import time
import csv
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


f = open('Final.csv', 'w+')
f.close()

fileCounter = 0


patterns = ["data.csv"]
ignore_patterns = None
ignore_directories = False
case_sensitive = True
my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)


def on_modified(event):
    global accel
    global gravity
    global gyro
    global label
    global fileCounter
    with open('data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            lastRow = row[0]
        csv_file.close()
    print(lastRow)
    with open('Final.csv', 'a') as f:
        writer = csv.writer(f)
        if (fileCounter == 1):
            writer.writerow(["RSSI", "accel_x", "accel_y", "accel_z",  "gyro_x", "gyro_y", "gyro_z", "label"])    
        if (fileCounter > 3):
            writer.writerow([lastRow, accel[0] - gravity[0], accel[1] - gravity[1], accel[2] - gravity[2], gyro[0], gyro[1], gyro[2], label])
        else:
            fileCounter = fileCounter +1


my_event_handler.on_modified = on_modified
path = "."
go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)


my_observer.start()

HOST = '192.168.0.163' #this is your localhost
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket.socket: must use to create a socket.
#socket.AF_INET: Address Format, Internet = IP Addresses.
#socket.SOCK_STREAM: two-way, connection-based byte streams.
print('socket created')

#Bind socket to Host and Port
try:
    s.bind((HOST, PORT))
except socket.error as err:
    print('Bind Failed, Error Code: ' + str(err[0]) + ', Message: ' + err[1])
    sys.exit()

print('Socket Bind Success!')


#listen(): This method sets up and start TCP listener.
s.listen(10)
print('Socket is now listening')
accel = [0.0, 0.0, 0.0]
gyro = [0.0, 0.0, 0.0]
gravity = [0.0, 0.0 ,0.0]
label = ""
try:
    while 1:
        conn, addr = s.accept()
        print('Connect with ' + addr[0] + ':' + str(addr[1]))
        while 1:
            buf = conn.recv(200)
            msg = buf.decode("utf-8")
            print(msg)
            d = []
            for i in msg.split("}")[0:-1]:
                if (len(i) > 0):
                    if (i[0] == "{"):
                        d.append(i+"}")
            for i in d:
                # print(i)
                data = json.loads(i)
                if ("S" in data):
                    if (data["S"] == "A"):
                        accel[0] = data["x"]
                        accel[1] = data["y"]
                        accel[2] = data["z"]
                    if (data["S"] == "Gy"):
                        gyro[0] = data["x"]
                        gyro[1] = data["y"]
                        gyro[2] = data["z"]
                    if (data["S"] == "G"):
                        gravity[0] = data["x"]
                        gravity[1] = data["y"]
                        gravity[2] = data["z"]
                elif ("L" in data):
                    label = data["L"]
            # print(type(msg))
            # print("-------------")
            s = "Accel="+str(accel[0])+","+str(accel[1])+","+str(accel[2])
            print(s)
            s = "Gravity="+str(gravity[0])+","+str(gravity[1])+","+str(gravity[2])
            print(s)
            s = "Gyro="+str(gyro[0])+","+str(gyro[1])+","+str(gyro[2])
            print(s)
            s = "Label =" + label
            print(s)
except:
    s.close()
    my_observer.stop()
    my_observer.join()
