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

    def check_key(self, key):
        for acct in self.accounts:
            if acct.authentication_key == key:
                return acct.uname
        return None

    def login(self, uname):
        for account in self.accounts:
            if account.uname == uname:
                if account.logged_in:
                    return None
                account.logged_in = True
                account.authentication_key = str(random.randint(10000, 99999))
                return account.authentication_key
        return None

    def logout(self, uname):
        for account in self.accounts:
            if account.uname == uname:
                account.logged_in = False
                account.authentication_key = None
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
            acct = Account(entries[0], entries[1])
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

class Account():
    def __init__(self, uname, pword):
        self.uname = uname
        self.pword = pword
        self.logged_in = False
        self.authentication_key = None

