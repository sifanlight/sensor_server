# Sensor and BLE servers
For sensor data just run newServer.py. 
Please be careful that you have to enter your ip addreess in the code:
```
HOST = '192.168.1.2' #this is your localhost
PORT = 8888
```
For bluetooth code, first install libbluetooth-dev package with this command:
```
$> apt install libbluetooth-dev
```
and compile it with this flag:
```
$> gcc scannerMod.c -o scannerMod -lbluetooth
```
and run the output with root access.

For this android client please visit this repository:</br>
https://github.com/sifanlight/sensor_android_client
