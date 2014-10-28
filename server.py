import socket
import sys
import errno
import select
import json 
import time
import logging

from Accounts import *
from Messages import *

acct_manager = Accounts_Manager("./accounts")

conversations = []
conversations_filename = "./conversations"

class Handler():
    def __init__(self, requires_login, n_args, handler):
        self.requires_login = requires_login
        self.n_args = n_args
        self.handler = handler

    def valid(self, args):
        return len(args) >= self.n_args

    def handle(self, args):
        return self.handler(args)

def handle_login(args):
    logging.debug("handle_login args: {}".format(args))
    if acct_manager.authenticate(args[1], args[2]):
        acct_manager.login(args[1], args[0])
        return "{} logged in".format(args[1])
    else:
        return "Authentication error"

def handle_logout(args):
    if acct_manager.logout(args[0]) == -1:
        return "Logout error"

    return args[0] + " logged out sucessfully"

def handle_list_users(args):
    users = []
    for acct in acct_manager.accounts:
        users.append((acct.uname, acct.peername != None))
    try:
        user_list = json.dumps(users)
    except:
        return "Json error"
    return user_list
    
def handle_send(args):
    msg_txt    = args[2]
    msg_date   = time.ctime(None)
    msg_sender = args[0]

    convo_id = args[1]

    msg = Message(msg_date, msg_sender, msg_txt)

    for convo in conversations:
        if convo.id_num == convo_id:
            convo.send_message(msg)
            return 'Message send to conversation {}'.format(convo_id)
    return 'Error: No conversation with id={}'.format(convo_id)

def handle_create_conversation(args):
    while True:
        id_num = str(random.randint(100000, 999999))
        for convo in conversations:
            if convo.id_num == id_num:
                continue
        break

    users = args
    convo = Conversation(users, id_num)
    conversations.append(convo)

    return "Conversation created. ID = " + convo.id_num

def handle_get_convos(args):
    convos = []
    for convo in conversations:
        if args[0] in convo.users:
            msgs = []
            for m in convo.messages:
                msg = [m.sender, m.date, m.text]
                msgs.append(msg)
            convos.append([convo.id_num, convo.users, msgs])
    response = json.dumps(convos)
    print('response = {}, convos = {}'.format(response, convos))
    return response

def handle_remove_account(args):
    return "Remove account requested"

def handle_create_account(args):
    if acct_manager.user_exists(args[1]):
        return "Error, account for {} already exists".format(args[1])
    acct = Account(args[1], args[2])
    acct_manager.add_user(acct)
    return "Created account for " + args[1] 

handlers = {'login': Handler(False, 3, handle_login), 
            'logout': Handler(True, 1, handle_logout), 
            'list-users': Handler(True, 1, handle_list_users), 
            'send': Handler(True, 3, handle_send), 
            'new-convo': Handler(True, 2, handle_create_conversation),
            'get-convos': Handler(True, 1, handle_get_convos),
            'remove-account': Handler(True, 1, handle_remove_account), 
            'create-account': Handler(False, 2, handle_create_account)
            }

def cmd_parse(data, peername):
    args = data.split()
    
    if args[0] in handlers:
        h = handlers[args[0]]
        args = args[1:]

        if h.requires_login:
            uname = acct_manager.get_uname(peername)
            if uname == None:
                response = "Error: Log in first"
                return response
            else:
                args.insert(0, uname)
        else:
            args.insert(0, peername)

        if h.valid(args):
            response = h.handle(args)
        else:
            response = "Error: Invalid no. of args"
    else: 
        response = "Error: Unknown command"

    return response

def initialize():
    global acct_manager

    acct_manager.load_account_info()
    conversations = load_conversations(conversations_filename)

def serve_forever(host, port):
    lstsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lstsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lstsock.setblocking(0)

    lstsock.bind((host, port))
    lstsock.listen(5)

    rlist, wlist, elist = [lstsock], [], []
   
    oldtime = time.time()

    while True:
        if (time.time() - oldtime > 30): #save info every 30 seconds
            acct_manager.save_account_info()
            save_conversations(conversations, conversations_filename)
            oldtime = time.time()

        readables, writeable, exceptions = select.select(rlist, wlist, elist)

        for sock in readables:
            if sock is lstsock:
                try:
                    conn, addr = lstsock.accept()
                    print('accepted connection from: {}'.format(addr))
                except OSError as e:
                    errnum, errmsg = e.args
                    print(msg)
                    if code == errno.EINTR:
                        continue
                    else:
                        raise
                rlist.append(conn)
                print(rlist)
            else:
                print("received transmission from {}".format(sock.getpeername()))
                data = sock.recv(1024)
                if not data: #connection closed by client
                    print("closing connection with {}".format(sock.getpeername()))
                    acct_manager.logout(acct_manager.get_uname(sock.getpeername()))
                    sock.close()
                    rlist.remove(sock)
                else:
                    response = cmd_parse(data.decode("utf-8"), sock.getpeername())
                    print(response)
                    sock.sendall(bytes(response + '/r/n', "utf-8"));

def main():
    initialize()
    logging.basicConfig(filename="./server.log", level=logging.DEBUG)
    serve_forever("", 5555)

if __name__ == '__main__':
    main()
