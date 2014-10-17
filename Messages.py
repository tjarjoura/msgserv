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
    def __init__(self, id_num, date, sender, text):
        self.id_num = id_num
        self.date = date
        self.sender = sender
        self.text = text


