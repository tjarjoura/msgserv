import curses

class Messaging_Client():
    def __init__(self):
        print ('init start')
        self.stdscr = curses.initscr()
        curses.cbreak()
        curses.noecho()

        self.windows = {}
        self.menus   = {}
        
        self.active_menu = None
        self.running = True
        
        self.height, self.width = self.stdscr.getmaxyx()

        self.windows['titlebar'] = curses.derwin(1, self.width, 0, 0)
        self.windows['menu_area'] = curses.derwin(10, 20, 1, 0)
        self.windows['user_list'] = curses.derwin(self.height - 11, 20, 11, 0)
        self.windows['message_area'] = curses.derwin(self.height - 1, self.width - 20, 1, 20)
        self.windows['input_area'] = curses.derwin(1, self.width, self.height - 1, 0)

    def handle_input(self):
        c = self.stdscr.getch()
        if c == ord('q'):
            self.running = False
        else:
            stdscr.addch(1, 0, c)

    def update_screen(self):
        for name, window in self.windows.items():
            window.border()
            window.clear()
            window.refresh()

    def __del__(self):
        nocbreak()
        echo()
        endwin()

def main():
    cli = Messaging_Client()
    
    while cli.running:
        print('loop')
        cli.update_screen()
        cli.handle_input()
    
    nobreak()
    echo()
    endwin()

if __name__ == '__main__':
    main()
