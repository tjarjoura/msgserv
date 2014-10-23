import curses

class Messaging_Client():
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.cbreak()
        curses.noecho()

        self.windows = {}
        self.menus   = {}
        
        self.active_menu = None
        self.running = True
        
        self.height, self.width = self.stdscr.getmaxyx()

        self.windows['titlebar'] = self.stdscr.derwin(1, self.width, 0, 0)
        self.windows['menu_area'] = self.stdscr.derwin(10, 20, 1, 0)
        self.windows['user_list'] = self.stdscr.derwin(self.height - 11, 20, 11, 0)
        self.windows['message_area'] = self.stdscr.derwin(self.height - 1, self.width - 20, 1, 20)
        self.windows['input_area'] = self.stdscr.derwin(1, self.width, self.height - 1, 0)

    def handle_input(self):
        c = self.stdscr.getch()
        if c == ord('q'):
            self.running = False
        else:
            self.stdscr.echochar(c)

    def update_screen(self):
        for name, window in self.windows.items():
            window.border()
            window.clear()
            window.refresh()

def main():
    cli = Messaging_Client()
   
    print(cli.running)
    while cli.running:
        cli.update_screen()
        cli.handle_input()
    
    curses.nocbreak()
    curses.echo()
    curses.endwin()

if __name__ == '__main__':
    main()
