import socket, sys, json, logging

conversations = []
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logging.basicConfig(filename='mylog', level=logging.DEBUG)
logging.debug('test test test')

def connect_socket(ip_addr, port):
    try:
        sock.connect((ip_addr, int(port)))
    except:
        print('Error connecting to {}, {}'.format(ip_addr, port))
        sys.exit(0)

def send_message(msg):
    try:
        sock.sendall(bytes(msg, "utf-8"))
        received = ""
        while True:
            received += sock.recv(1024).decode("utf-8")
            if received[-4:] == '/r/n':
                break
     
    except OSError as e:
        print(e.strerror)
        print('error sending {}'.format(msg))
        sock.close()
        sys.exit(0)
    
    return received[:-4] 

def attempt_login(uname, pword):
    response = send_message('login {} {}'.format(uname, pword))
    logging.debug('In attempt_login({} {}) -- Received: {}'.format(uname, pword, response))

    if response == '{} logged in'.format(uname):
        return 1
    else:
        return -1

def get_convos():
    response = send_message('get-convos')
    logging.debug('In get_convos() -- Received: {}'.format(response))
    convos = json.loads(response)
    convos_strings = []

    for convo in convos:
        string = convo[0]
        for usr in convo[1]:
            string += " {},".format(usr)
        convos_strings.append(string)

    return convos_strings

def get_users():
    response = send_message('list-users')
    logging.debug('In get_users() -- Received: {}'.format(response))

    return json.loads(response)
