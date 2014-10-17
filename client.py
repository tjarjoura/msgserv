import npyscreen
import curses



class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', LoginForm, name='MSGSERV VER 0.1')

class LoginForm(npyscreen.FormBaseNew):
    def create(self):
        messages_widget = self.add(npyscreen.TitlePager, name='MESSAGES', rely=1, relx=20)
        menu_widget = self.add(npyscreen.MultiLine, name='MENU', rely=2, relx=1, max_width=20, values = ['Login', 'Exit'])
        users_widget = self.add(npyscreen.TitlePager, name='USERS', rely=11, relx=1, max_width=20, max_height=150)
        input_widget = self.add(npyscreen.TitleText, name='INPUT')

if __name__ == '__main__':
    app = App().run()
