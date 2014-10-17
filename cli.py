import socket
import sys

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
    
    if inp == "done":
        break

    try:
        received = ""
        sock.sendall(bytes(inp + "\n", "utf-8"))
        while True:
            received += sock.recv(1024).decode("utf-8")
            print(received)
            print(received[-4:])
            if received[-4:] == '/r/n':
                break

    except OSError:
        print('error')
        sock.close()
        break

    print("Sent:     {}".format(inp))
    print("Received: {}".format(received))

sock.close()
