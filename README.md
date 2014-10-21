Work in progress network application written in Python. Allow users to connect to the server, create an account, and join conversations with other accounts.

Server protocol:

login [username] [password] : If the account associated with username and password exists, it will be marked as logged in and the client will receive a randomly generated authentication key for it.
logout [authentication key] : If account associated with the authentication key exists and is logged in, it will be marked as not logged in and the authentication key for it will be set to None
list-users [authentication key] : Assuming the authentication key is valid, this will return a list of users on the server in json notation
new-convo [authentication key] [list of users] : Assuming the authentication key is valid, this will create a new conversation object associated with the every username in list of users
send [authentication key] [conversation key] [message text] : Assuming the authentication and conversation keys are valid, this will add a message object with the given message text to the conversation associated with the id.
remove-account [authentication key] : Assuming the authentication key is valid, this will log the user out and delete their account.
create-account [username] [password] : Creates a new account on the server with username and password.
