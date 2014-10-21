import socket
import sys
import pickle

HOST, PORT = sys.argv[1], 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
except:
    print('connect error')
    sys.exit()

while True:
    try:
        inp = input(">> ")
    except EOFError:
        break
    
    cmd = inp.split()[0]
    print(cmd)
    
    if inp == "done":
        break

    try:
        sock.sendall(bytes(inp + "\n", "utf-8"))
        received = ""
        while True:
            received += sock.recv(1024).decode("utf-8")
            if received[-4:] == '/r/n':
                break
    
    except OSError:
        print('error')
        sock.close()
        break

    print("Sent:     {}".format(inp))
    print("Received: {}".format(received))

sock.close()
