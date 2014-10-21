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
        received = bytearray() 
        sock.sendall(bytes(inp + "\n", "utf-8"))
        while True:
            received += sock.recv(1024)
            if received[-2:] == [int('0x0d', 16), int('0x0a', 16)]:
                break

        if cmd == 'list-users':
            users = pickle.loads(received[:-4])
            print(users)
    
    except OSError:
        print('error')
        sock.close()
        break

    print("Sent:     {}".format(inp))
    print("Received: {}".format(received))

sock.close()
