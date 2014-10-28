import urwid, curses, socket, sys, json, logging
from client_network import *

program_name = "MSGSERV VER 0.5"

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
        self.convos = urwid.ListBox(self.convo_list)
        self.users = urwid.ListBox(self.user_list)
        self.controls = urwid.Text(('status_red', 'n to create a new conversation, q to quit'))
        super().__init__([('pack', self.title), urwid.Columns([(25, urwid.LineBox(self.users, title="USERS")), urwid.LineBox(self.convos, title="CONVERSATIONS")], dividechars=5, focus_column=1), ('pack', self.controls)])

    def update_lists(self):
        logging.debug("in update_lists()")
        if len(self.convo_list) > 0:
            convos_old_focus = self.convos.focus_position
        else:
            convos_old_focus = 0

        if len(self.user_list) > 0:
            users_old_focus = self.users.focus_position
        else:
            users_old_focus = 0

        del self.convo_list[:]
        del self.user_list[:]

        convos = get_convos()
        for c in convos:
            button = urwid.Button(c[1], on_press=self.enter_convo, user_data=c[0])
            self.convo_list.append(button)
        
        if len(self.convo_list) > 0:
            self.convos.focus_position = min(convos_old_focus, len(self.convo_list) - 1)

        users = get_users()
        for u in users:
            if u[1] == True:
                self.user_list.append(urwid.Text(('status_green', u[0])))
            else:
                self.user_list.append(urwid.Text(('status_red', u[0])))
        
        if len(self.user_list) > 0:
            self.users.focus_position = min(users_old_focus, len(self.user_list))
            
        loop.event_loop.alarm(.5, main.update_lists)
    
    def enter_convo(self, button, convo_id):
        send.set_id(convo_id)
        loop.widget = send

    def keypress(self, size, key):
        if key != 'q' and key != 'n':
            return super().keypress(size, key)
        elif key == 'q':
            raise urwid.ExitMainLoop()
        elif key == 'n':
            loop.widget = new_message


class NewMessageScreen(urwid.Pile):
    def __init__(self):
        self.title = urwid.Text(('titlebar', program_name))
        self.users_edit = urwid.Edit()
        self.msg_edit = urwid.Edit()
        self.info_text = urwid.Text('')

        super().__init__([('pack', self.title), (3, urwid.LineBox(urwid.Filler(self.users_edit), title="USERS")), urwid.LineBox(urwid.Filler(self.msg_edit, valign='top'), title="MESSAGE"), ('pack', self.info_text)])
    
    def keypress(self, size, key):
        if key == 'q':
            raise urwid.ExitMainLoop()
        if key == 'enter':
            if self.users_edit.edit_text != "" and self.msg_edit.edit_text != "":
                new_convo(self.users_edit.edit_text, self.msg_edit.edit_text)
                self.users_edit.edit_text = "" 
                self.msg_edit.edit_text = ""
            loop.widget = main
        else:
            super().keypress(size, key)

class SendScreen(urwid.Pile):
    def __init__(self):
        self.title = urwid.Text(('titlebar', program_name))
        self.msg_list = urwid.SimpleListWalker([])
        self.edit_area = urwid.Edit()
        self.convo_id = None

        super().__init__([('pack', self.title), urwid.LineBox(urwid.ListBox(self.msg_list)), (5, urwid.LineBox(urwid.Filler(self.edit_area, valign='top'), title="REPLY"))])

    def set_id(self, id_num):
        self.convo_id = id_num

    def update_messages(self):
        logging.debug("in update_messages")
        if self.convo_id == None:
            return
       
        del self.msg_list[:]

        msgs = get_messages(self.convo_id)
        for m in msgs:
            string = "{}({}): {}".format(m[0], m[1], m[2])
            logging.debug("update_messages(): appending {}".format(string))
            self.msg_list.append(urwid.Text(string))
    
        loop.event_loop.alarm(.5, self.update_messages)

    def keypress(self, size, key):
        if key == 'q':
            raise urwid.ExitMainLoop()
        if key == 'enter':
            if self.edit_area.edit_text != "":
                send_message("send {} {}".format(self.convo_id, self.edit_area.edit_text))
            self.edit_area.edit_text = ""
        if key == 'b':
            loop.widget = main
        else:
            super().keypress(size, key)

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
            #loop.event_loop.enter_idle(main.update_lists)
            #loop.event_loop.enter_idle(send.update_messages)
            loop.event_loop.alarm(.5, main.update_lists)
            loop.event_loop.alarm(.5, send.update_messages)
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
