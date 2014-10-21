import json
import errno

class Conversation():
    def __init__(self, users, id_num):
        self.id_num =   id_num
        self.users =    []
        self.messages = []
        for usr in users:
            self.users.append(usr)
    
    def send_message(self, msg):
        self.messages.append(msg)

    def join_user(self, usr):
        self.users.append(usr)

class Message():
    def __init__(self, date, sender, text):
        self.date = date
        self.sender = sender
        self.text = text


def load_conversations(conversations_filename):
    convos = []
    try:
        conversations_file = open(conversations_filename, "r")
    except OSError as e:
        print(e.strerror)
        if e.errno == errno.ENOENT:
            print("Creating file: {}".format(conversations_filename))
            open(conversations_filename, "x")
            return []

    content = conversations_file.read()
    if content is not "":
        return json.loads(content)

def save_conversations(conversations, conversations_filename):
    convos = []
    conversations_file = open(conversations_filename, "w")

    for convo in conversations:
        msgs = []
        for msg in self.messages:
            msgs.append((msg.date, msg.sender, msg.text))
        convos.append((convo.id_num, convo.users, convo.messages))
    
    conversations_file.write(json.dumps(convos))
    conversations_file.close()
