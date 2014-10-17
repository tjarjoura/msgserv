import socket
import sys
import errno
import select
import cpickle as pickle

from Accounts import *
from Messages import *

acct_manager = Accounts_Manager("./accounts")

conversations = []

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
    return "List users requested"

def handle_send(args):
    return "Send requested"

def handle_create_conversation(args):
    if check_key(args[0]) == False:
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

def cmd_parse(data):
    arguments = data.split()
    
    if arguments[0] == "login":
        response = handle_login(arguments[1:])
    elif arguments[0] == "logout":
        response = handle_logout(arguments[1:])
    elif arguments[0] == "list-users":
        response = handle_list-users(arguments[1:])
    elif arguments[0] == "send":
        response = handle_send(arguments[1:])
    elif arguments[0] == "remove-account":
        response = handle_remove_account(arguments[1:])
    elif arguments[0] == "create-account":
        response = handle_create_account(arguments[1:])
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
                    response = cmd_parse(data.decode("utf-8"))
                    sock.sendall(bytes(response + '/r/n', "utf-8"))

def main():
    initialize()
    serve_forever("", 5555)

if __name__ == '__main__':
    main()
