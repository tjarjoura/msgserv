import socket
import sys
import errno
import select
import pickle 

from Accounts import *
from Messages import *

acct_manager = Accounts_Manager("./accounts")

conversations = []

class Handler():
    def __init__(self, requires_key, n_args, handler):
        self.requires_key = requires_key
        self.n_args = n_args
        self.handler = handler

    def valid(self, args):
        return len(args) == self.n_args

    def handle(self, args):
        return self.handler(args)

def handle_login(args):
    if acct_manager.authenticate(args[0], args[1]):
        key = acct_manager.login(args[0])
        if key != None:
            return "Login successful. Your key is " + key
        else:
            return "Login error. You're probably already logged in."
    else:
        return "Login error"

def handle_logout(args):
    if logout(args[0]) == -1:
        return "Logout error"

    return args[0] + " logged out sucessfully"

def handle_list_users(args):
    users = []
    for acct in acct_manager.accounts:
        users.append(acct.uname)
    try:
        user_list = pickle.dumps(users)
    except:
        return "Pickle error"
    return user_list.decode("utf-8")
    
def handle_send(args):
    return "Send requested"

def handle_create_conversation(args):
    if acct_manager.check_key(args[0]) == False:
        return "Authentication error. Send your authentication key as the first argument."
    while True:
        id_num = random.randint(100000, 999999)
        for convo in conversations:
            if convo.id_num == id_num:
                continue
        break

    users = args[1:]
    convo = Conversation(users, id_num)
    conversations.apppend(convo)

    return "Conversation created. ID = " + convo.id_num

def handle_remove_account(args):
    return "Remove account requested"

def handle_create_account(args):
    acct = Account(args[0], args[1])
    acct_manager.add_user(acct)
    return "Created account for " + args[0] 

handlers = {'login': Handler(False, 2, handle_login), 
            'logout': Handler(True, 0, handle_logout), 
            'list-users': Handler(True, 0, handle_list_users), 
            'send': Handler(True, 1, handle_send), 
            'remove-account': Handler(True, 0, handle_remove_account), 
            'create-account': Handler(False, 2, handle_create_account)
            }

def cmd_parse(data):
    args = data.split()
    
    if args[0] in handlers:
        h = handlers[args[0]]
        args = args[1:]
        if h.requires_key:
            if len(args) < 1:
                response = "Error: Key required"
                return response
            if not acct_manager.check_key(args[0]):
                response = "Error: Bad key"
                return response
            args = args[1:]

        if h.valid(args):
            response = h.handle(args)
        else:
            response = "Error: Invalid" + str(args)
    else: 
        response = "Error: Unknown command"

    return response

def initialize():
    global acct_manager

    acct_manager.load_account_info()

def serve_forever(host, port):
    lstsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lstsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lstsock.setblocking(0)

    lstsock.bind((host, port))
    lstsock.listen(5)

    rlist, wlist, elist = [lstsock], [], []

    while True:
        readables, writeable, exceptions = select.select(rlist, wlist, elist)

        for sock in readables:
            if sock is lstsock:
                try:
                    conn, addr = lstsock.accept()
                except OSError as e:
                    errnum, errmsg = e.args
                    print(msg)
                    if code == errno.EINTR:
                        continue
                    else:
                        raise
                rlist.append(conn)
            else:
                data = sock.recv(1024)
                if not data: #connection closed by client
                    sock.close()
                    rlist.remove(sock)
                else:
                    response = bytearray()
                    response_string = cmd_parse(data.decode("utf-8"))
                    response.append += response_string.encode("utf-8")
                    response.append([int('0x0d', 16), int('0x0a', 16)]) # append /r/n
                    sock.sendall(response)

def main():
    initialize()
    serve_forever("", 5555)

if __name__ == '__main__':
    main()
