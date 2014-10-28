import urwid, curses, socket, sys, json, logging
from client_network import *

program_name = "MSGSERV VER 0.1"

palette = [
        ('titlebar', 'white, bold', 'dark blue'),
        ('status_red', 'light red', 'black'),
        ('status_green', 'dark green', 'black'),
        ('prompt', 'bold, underline', 'black'),
        ('section_title', 'bold, black', 'dark red')
        ]

class MainScreen(urwid.Pile):
    def __init__(self):
        self.title = urwid.Text(('titlebar', program_name))
        self.convo_list = urwid.SimpleListWalker([])
        self.user_list = urwid.SimpleListWalker([])
        self.controls = urwid.Text(('status_red', 'Ctrl-X for menu, q to quit'))
        super().__init__([('pack', self.title), urwid.Columns([(25, urwid.LineBox(urwid.ListBox(self.user_list), title="USERS")), urwid.LineBox(urwid.ListBox(self.convo_list), title="CONVERSATIONS")], dividechars=5, focus_column=1), ('pack', self.controls)])

    def update_lists(self):
        convos = get_convos()
        for c in convos:
            button = urwid.Button(c[1], on_press=enter_convo, user_data=c[0])
            self.convos_list.append(button)

        users = get_users()
        for u in users:
            if u[1] == True:
                self.user_list.append(urwid.Text(('status_green', u[0])))
            else:
                self.user_list.append(urwid.Text(('status_red', u[0])))
   
    def enter_convo(self, convo_id):
        send.set_id(convo_id)
        send.update_messages()
        loop.widget = send

    def keypress(self, size, key):
        if key != 'r' and key != 'q' and key != 'n':
            return super().keypress(size, key)
        if key == 'r':
            logging.debug('r key pressed.')
            self.update_lists()
        elif key == 'q':
            raise urwid.ExitMainLoop()
        elif key == 'n':
            loop.widget = new_message


class NewMessageScreen(urwid.Pile):
    def __init__(self):
        self.title = urwid.Text(('titlebar', program_name))
        self.users_edit = urwid.Edit(caption="Users: ")
        self.msg_edit = urwid.Edit(caption="Message: ")
        self.info_text = urwid.Text('')

        super().__init__([('pack', self.title), (3, urwid.LineBox(self.users_edit)), urwid.LineBox(self.msg_edit), ('pack', self.info_text)])
    
    def keypress(self, size, key):
        if key == 'q':
            raise urwid.ExitMainLoop()
        if key == 'enter':
            if self.users_edit.edit_text != None and self.msg_edit.edit_text != None:
                new_convo(self.users_edit.edit_text, self.msg_edit.edit_text)
            main.update_lists()
            loop.widget = main

class SendScreen(urwid.Pile):
    def __init__(self):
        self.title = urwid.Text(('titlebar', program_name))
        self.msg_list = urwid.SimpleListWalker([])
        self.edit_area = urwid.Edit(caption="Reply")
        self.convo_id = None

        super().__init__([('pack', self.title), urwid.LineBox(urwid.ListBox(self.msg_list)), (5, urwid.LineBox(self.edit_area))])

    def set_id(self, id_num):
        self.convo_id = id_num

    def update_messages(self):
        if self.convo_id == None:
            return
        
        msgs = get_messages(self.convo_id)
        for m in msgs:
            string = "{}({}): {}".format(m[0], m[1], m[2])
            self.msg_list.apppend(urwid.Text(string))

class LoginScreen(urwid.Filler):
    def __init__(self):
        self.title = urwid.Text(('titlebar', program_name))
        div_a = urwid.Divider()
        self.username_prompt = urwid.Edit([('prompt', "Username:"), " "], align='left')
        self.password_prompt = urwid.Edit([('prompt', "Password:"), " "], align='left')
        div_b = urwid.Divider()
        self.status_text = urwid.Text("", align='left')
        self.screen = urwid.LineBox(urwid.Pile([self.title, div_a, self.username_prompt, self.password_prompt, div_b, self.status_text]))

        super().__init__(self.screen, valign='top')

    def keypress(self, size, key):
        if key != 'enter' and key != 'q':
            return super().keypress(size, key)
        
        if key == 'q':
            raise urwid.ExitMainLoop()

        uname = self.username_prompt.edit_text
        pword = self.password_prompt.edit_text

        if (uname is None) or (pword is None):
            return key
        rc = attempt_login(uname, pword)

        if rc == -1:
            self.status_text.set_text(('status_red', "Error authenticating."))
        else:
            # Switch screens
            main.update_lists()
            loop.widget = main

if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print('Usage: {} <ip address> <port>\n'.format(sys.argv[0]))
        sys.exit(0)

    connect_socket(sys.argv[1], sys.argv[2])

    login = LoginScreen()
    main = MainScreen()
    send = SendScreen()
    new_message = NewMessageScreen()

    loop = urwid.MainLoop(login, palette)

    loop.run()
