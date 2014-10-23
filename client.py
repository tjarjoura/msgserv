import urwid, curses, socket, sys, json
from client_network import *

program_name = "MSGSERV VER 0.1"

palette = [
        ('titlebar', 'white, bold', 'dark blue'),
        ('status_red', 'light red', 'black'),
        ('status_green', 'dark green', 'black'),
        ('prompt', 'bold, underline', 'black'),
        ('section_title', 'bold, black', 'dark red')
        ]

class MainScreen(urwid.Filler):
    def __init__(self):
        self.title = urwid.Text(('titlebar', program_name))
        self.convos_body = urwid.SimpleFocusListWalker([urwid.Text(('section_title', "CONVERSATIONS"))])
        self.convo_list = urwid.ListBox(self.convos_body)
        self.users_body = urwid.SimpleFocusListWalker([urwid.Text(('section_title', "USERS"))])
        self.user_list = urwid.ListBox(self.users_body)
        
        self.screen = urwid.Columns([self.user_list, self.convo_list], dividechars=5, focus_column=1)

        super().__init__(self.screen, valign='top')

    def update_lists(self):
        self.convos_body = self.convos_body[:1]
        convos = get_convos()
        for c in convos:
            self.convos_body.append(urwid.Text(c))

        self.users_body = self.users_body[:1]
        users = get_users()
        for u in users:
            if u[1] == True:
                self.users_body.append(urwid.Text(('status_green', u[0])))
            else:
                self.users_body.append(urwid.Text(('status_red', u[0])))

class LoginScreen(urwid.Filler):
    def __init__(self):
        self.title = urwid.Text(('titlebar', program_name))
        div_a = urwid.Divider()
        self.username_prompt = urwid.Edit([('prompt', "Username:"), " "], align='left')
        self.password_prompt = urwid.Edit([('prompt', "Password:"), " "], align='left')
        div_b = urwid.Divider()
        self.status_text = urwid.Text("", align='left')
        self.screen = urwid.Pile([self.title, div_a, self.username_prompt, self.password_prompt, div_b, self.status_text])

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

    loop = urwid.MainLoop(login, palette)

    loop.run()
