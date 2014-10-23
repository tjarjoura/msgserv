import errno, random

class Accounts_Manager():
    def __init__(self, accounts_filename):
        self.accounts_filename = accounts_filename
        self.accounts = []
        self.active_account = None
        
        random.seed()
    
    def add_user(self, user):
        self.accounts.append(user)
    
    def rmv_user(self, uname):
        for account in self.accounts:
            if account.uname == uname:
                self.accounts.remove(account)
                return 0
        return -1

    def get_uname(self, peername):
        for acct in self.accounts:
            if acct.peername == peername:
                return acct.uname
        return None

    def login(self, uname, peername):
        for account in self.accounts:
            if account.uname == uname:
                if account.peername is not None:
                    return None
                account.peername = peername
        return None

    def logout(self, uname):
        for account in self.accounts:
            if account.uname == uname:
                account.peername = None
                return 0
        return -1

    def load_account_info(self):
        try:
            accounts_file = open(self.accounts_filename, 'r')
        except OSError as e:
            print(e.strerror)
            if (e.errno == errno.ENOENT):
                print("Creating file")
                open(self.accounts_filename, 'x')
            return

        for line in accounts_file:
            entries = line.split(' ', 2)
            entries[1] = entries[1][:-1]
            acct = Account(entries[0], entries[1])
            print('adding Account({}, {})'.format(entries[0], entries[1]))
            self.add_user(acct)
        accounts_file.close()

    def save_account_info(self):
        try:
            accounts_file = open(self.accounts_filename, 'w')
        except OSError as e:
            print(e.strerror)
            return
        for acct in self.accounts:
            accounts_file.write(acct.uname + ' ' + acct.pword + '\n')
        accounts_file.close()

    def authenticate(self, uname, pword):
        for acct in self.accounts:
            if acct.uname == uname:
                if acct.pword == pword:
                    return True
                return False
        return False

    def user_exists(self, uname):
        for acct in self.accounts:
            if acct.uname == uname:
                return True
        return False

class Account():
    def __init__(self, uname, pword):
        self.uname = uname
        self.pword = pword
        self.peername = None

