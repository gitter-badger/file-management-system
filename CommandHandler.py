"""
This program handles the commands
passed by the client to server.
"""

import pathlib
import os
import pandas
import time
from shutil import rmtree
import csv

class CommandHandler():
    """
    Used to create a user
    This class involves attributes like
    --------
    self.user_id : Returns a string representing the user ID of the user
    --------
    self.is_login : Gives data if the user is logged in or not
    --------
    self.registered_users: Returns list of registered users
    --------
    self.logged_in_users : Returns a list of users who are already logged in
    ========
    Methods:
    This class involves methods like:
    --------
    register(): Used to register a new user and enables to create
                a username and password of their choice inorder to
                login.
    --------
    login(): Logs in the user only if the username and password provided matches the 
            data in registered data.
    --------
    quit(): Quits the Login Session, sets back all the parameters to initial values.
    --------
    change_folder(): Changes the current directory position to the specified position.
                    If the specified position is one up the Root directory, it will 
                    return an error.
    --------
    list(): Returns the list of subdirectories and files under the current directory. 
            Prints out the name, size, modified date of the files and subdirectories.
    --------
    read_file(): Read data from the file using the filename provided. Each time the function 
                is called reads next 100 characters of data. 
    --------
    write_file(): Writes data to the file using the filename provided.
    --------
    create_folder(): Creates a new folder with the specified name. If the specified folder 
                    already exists, returns an error message. 
    """


    REGISTERED_USERS_CSV_FILE = "AccessSession/registered_users.csv"
    LOGGED_IN_USERS_CSV_FILE = "AccessSession/logged_in_users.csv"
    CSV_HEADING = "username,password\n"
    NOT_LOGGED_IN = "\nLogin to Continue"
    ROOT_DIR = "Root/"


    def __init__(self):
        """
        The parameters are passed to the __init__ function
        The Parameters include :
        ------
        self.user_id : A string representing the user ID of the user
        ------
        self.is_login : A Boolean value (whether the user is logged in or not)
        ------
        self.registered_users : A list of registered usernames
        ------
        self.logged_in_users : A list of already logged in usernames 
        ------
        self.current_directory : The current file path of the user. By default, 
                                set to "Root/"
        ------
        self.char_count : Number of characters that should be read each time read_file() function 
                            is called
        """
        self.user_id = ""
        self.is_login = None
        self.registered_users = None
        self.logged_in_users = None
        self.current_directory = CommandHandler.ROOT_DIR
        self.read_index = {}
        self.char_count = 100
    

    def access_user_info(self):
        """
        This function deals with accessing the user information
        ----------------------------------------------------
        The user information involves both registered users
        and logged in users per session
        """

        if not os.path.exists("AccessSession"):
            os.mkdir("AccessSession")

        if not os.path.isfile(CommandHandler.REGISTERED_USERS_CSV_FILE):
            with open(CommandHandler.REGISTERED_USERS_CSV_FILE, "w") as writer:
                writer.write(CommandHandler.CSV_HEADING)
        if not os.path.isfile(CommandHandler.LOGGED_IN_USERS_CSV_FILE):
            with open(CommandHandler.LOGGED_IN_USERS_CSV_FILE, "w") as writer:
                writer.write(CommandHandler.CSV_HEADING)
        self.logged_in_users = pandas.read_csv(CommandHandler.LOGGED_IN_USERS_CSV_FILE)
        self.registered_users = pandas.read_csv(CommandHandler.REGISTERED_USERS_CSV_FILE)


    def commands(self):
        """
        This function returns the description of the commands that can be used by the user
        and the detailed functionality of each command
        """

        commands = ["register : For registering the new user ,command:register <username> <password> \n",
                 "login : To login, command:login <username> <password>,Note:password should be in integer\n",
                 "quit : To logout, command:quit\n",
                 
                 "change_folder : To change the path, command:change_folder <name>\n",
                 "list : list of all files in the path, command:list\n",
                 "read_file : To read content from the file, command:read_file <name>\n",
                 "write_file : To write content into the file, command:write_file <name>\n",
                 "create_folder : To create new folder, command:create_folder <name>\n"
                ]
        description = ""
        for command in commands:
            description += command
        return description

    
    def register(self, user_id, password):
        """
        This function is used to create a new user
         using the username and password provided.
        --------
        If a username already exists, it displays that the username is not
        available.
        --------
        Note that length of passwords should be more than 8
        """
        self.access_user_info()
        if user_id in self.registered_users['username'].tolist():
            return "\nUsername not available"
        if len(password) < 8:
            return "\n Password length should be more than 8 characters."
        with open(CommandHandler.REGISTERED_USERS_CSV_FILE, "a") as writer:
            writer.write(user_id+","+password+"\n")
        if not os.path.exists(self.current_directory):
            os.mkdir(self.current_directory)
        os.mkdir(os.path.join(self.current_directory, user_id))
        self.current_directory = self.current_directory + self.user_id
        return "\nSuccessfully registered user"


    def login(self, user_id, password):
        """
        This function is used to login the user, when respective credentials
        are provided by the user.
        --------
        When the username and password provided by the user matches the
        register data, then the user is allowed to login.
        --------
        Displays "Username not registered, please register to continue" when the credentials provided doesnot
        match the previous register data.
        --------
        Displays "Wrong password, try again", if the entered password does not match the registered
        username.
        """
        
        self.access_user_info()
        if self.is_login:
            return "\nAlready Logged In"
        if user_id not in self.registered_users['username'].tolist():
           # print (self.registered_users)
            return "\nUser not registered, please register to continue"
        if password not in self.registered_users['password'].tolist() and user_id in self.registered_users['username'].tolist():
            return "\nWrong Password, try again"
        if user_id in self.logged_in_users['username'].tolist():
            self.is_login = True
            self.user_id = user_id
            self.current_directory = self.current_directory + self.user_id
            return "\nUser logged through another port"
        
        self.is_login = True
        self.user_id = user_id
        self.current_directory = self.current_directory + self.user_id
        with open(CommandHandler.LOGGED_IN_USERS_CSV_FILE, "a") as writer:
            writer.write(user_id + "," + password + "\n")
        return "Logged into the system successfully!"


    def quit(self):
        """
        This function is used to 'Log Out' the user from the current login session.
        """
        
        try:
            self.access_user_info()
            with open(CommandHandler.LOGGED_IN_USERS_CSV_FILE, "w") as file:
                file.write(CommandHandler.CSV_HEADING)
                user_ids = self.logged_in_users['username'].tolist()
                passwords = self.logged_in_users['password'].tolist()
                for i in range(len(user_ids)):
                    if self.user_id != str(user_ids[i]):
                        file.write(user_ids[i]+","+passwords[i])
            self.is_login = False
            self.user_id = ""
            return "\nLogged Out"
        except KeyError:
            return "\nForced Logged Out through Keyboard Interruption (CTRL-C)"


    def list(self):
        """
        This function gives information about the name, size, date and
        time of creation of the request.
        -------
        It also prints all files and folders in the current working directory
        for issuing the request.
        -------
        It only has access to the current directory and can not print
        the information regarding content in sub- directories.
        """

        self.access_user_info()
        if not self.is_login:
            return CommandHandler.NOT_LOGGED_IN
        path = os.path.join(self.current_directory)
        directories = []
        try:
            for file_name in os.listdir(path):
               a = os.stat(os.path.join(path, file_name))
               directories.append([file_name, str(a.st_size), str(time.ctime(a.st_ctime))])
        except NotADirectoryError:
            return "\nNot A Directory"
        details = "\nFile | Size | Modified Date"
        for directory in directories:
            line = " | ".join([directory[0], directory[1], directory[2]]) + "\n"
            details += "-----------------------\n" + line
        return details


    def write_file(self, filepath, data):
        """
        This function appends data to the file in the diectotry
        as per the command given
        --------
        The file will be written with the data of the user input
        --------
        If data already exists in the file in the directory,
        the new data will be appended to the existing data
        without any data loss.
        """

        self.access_user_info()
        if not self.is_login:
            return CommandHandler.NOT_LOGGED_IN
        t_file = []
        for file in os.listdir(os.path.join(self.current_directory)):
            if os.path.isfile(os.path.join(self.current_directory, file)):
                t_file.append(file)
            
        writeable_data = ""
        path = os.path.join(self.current_directory, filepath)
        for i in data:
            writeable_data += i
        if filepath in t_file:
            with open(path, "a+") as file:
                file.write(writeable_data)
            return "\nSuccess Written data to file " + filepath + "successfully"
        with open(path, "w+") as file:
            file.write(writeable_data)
        return "\nCreated and written data to file " + filepath + "successfully"


    def create_folder(self, directory):
        """
        This function creates new directory as per the user command
        --------
        The function checks the existing directories before creating
        new ones to avoid duplication.
        """

        if not self.is_login:
            return CommandHandler.NOT_LOGGED_IN
        self.access_user_info()
        path = os.path.join(self.current_directory)
        directories = []
        for subdirectory in os.listdir(path):
            path2 = os.path.join(subdirectory)
            if os.path.isdir(path2):
                directories.append(path2)
        if directory in directories:
            return "\nThe directory is already created"
        os.mkdir(os.path.join(path, directory))
        return "\nSuccessfully created directory " + directory



    def change_folder(self, directory):
        """
        This function is used to change the position of current directory for
        the current user to the specified directory.
        """

        self.access_user_info()
        if not self.is_login:
            return CommandHandler.NOT_LOGGED_IN

        if directory == ".." and self.current_directory != CommandHandler.ROOT_DIR + self.user_id:
            self.current_directory = os.path.dirname(os.path.join(self.current_directory))
            return "\nSuccessfully moved to directory " + self.current_directory
        
        elif directory == ".." and self.current_directory == CommandHandler.ROOT_DIR + self.user_id:
            return "\nCannot Move Back from Root/" + self.user_id + " directory"

        if directory in os.listdir(self.current_directory):
            self.current_directory = os.path.join(self.current_directory, directory)
            return "\nSuccessfully Moved to directory " + self.current_directory
        return "\n No such directory exists"


    def read_file(self, filepath):
        """
        This function is used to read data from the file standing
        in the current directory.
        -------
        If a file with specified name does not exist in the current
        working directory for the user, the request is denied.
        """

        self.access_user_info()
        if not self.is_login:
            return CommandHandler.NOT_LOGGED_IN
        files = []
        for file in os.listdir(os.path.join(self.current_directory)):
            if os.path.isfile(os.path.join(self.current_directory, file)):
                files.append(file)
        if filepath not in files:
            return "\nGiven file does not exist"
        t_path = os.path.join(self.current_directory, filepath)
        if t_path not in list(self.read_index.keys()):
            self.read_index[t_path] = 0
        with open(t_path, "r") as file:
            content = file.read()
        old_index = str(self.read_index[t_path]*self.char_count)
        index = self.read_index[t_path]
        data = content[index*self.char_count:(index+1)*self.char_count]
        self.read_index[t_path] += 1
        self.read_index[t_path] %= len(content) // self.char_count + 1
        return "\n" + "Read file from " + old_index + " to " + str(int(old_index)+self.char_count) + "are\n" + data