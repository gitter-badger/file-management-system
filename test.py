"""
This program deals with the testing of
the server-client application
"""
import unittest
import sys
import pandas
from CommandHandler import CommandHandler
import os
import shutil


class TestClient(unittest.TestCase):
    """
    This class defines the tests that are conducted
    for the functions defined in the client-server application
    """

    def test_commands_output(self):
        """
        This function deals with testing commands output
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

        user_test = CommandHandler()
        obtained_result = user_test.commands()
        self.assertEqual(description, obtained_result)

    def test_register_password_length(self):
        """
        This function deals with test for registration data 
        and whether password with length of less than 8 characters 
        are not getting accepted.
        """
        user_test = CommandHandler()
        expected_result = "\n Password length should be more than 8 characters."
        obtained_result = user_test.register('test1', '122')
        self.assertEqual(expected_result, obtained_result)
        user_test.quit()
        
        
    
    def test_register_successful_registration(self):
        """
        This function deals with test whether the user provided data
         is being registered successfully
        """

        user_test = CommandHandler()
        expected_result = "\nSuccessfully registered user"
        obtained_result = user_test.register("test2", "13791247nbdshrlfngls")
        self.assertEqual(expected_result, obtained_result)
        user_test.quit()
        shutil.rmtree(os.path.join("Root/test2"))
        shutil.rmtree(os.path.join("AccessSession/"))

    
    def test_login(self):
        """
        This function deals with test for login data
        """

        user_test = CommandHandler()
        user_test.register('test', '123456737')
        expected_result = ["\nWrong Password, try again"]
        obtained_result = []
        tests = [['test', '12345678']]
        for test in tests:
            obtained_result.append(user_test.login(test[0], test[1]))
        user_test.quit()
        self.assertListEqual(obtained_result, expected_result)
        shutil.rmtree(os.path.join("Root/"))
        shutil.rmtree("AccessSession/")

    def test_quit(self):
        """
        This function deals whether the server closing 
        the TCP connection between client and server in a
        proper way
        """
        user_test = CommandHandler()
        user_test.register('test', '12343535373')
        user_test.login('test','12343535373')
        user_test.quit()
        expected_result = "\nLogged Out"
        obtained_result = user_test.quit()
        self.assertEqual(expected_result, obtained_result)
        shutil.rmtree(os.path.join("Root/"))
        shutil.rmtree("AccessSession/")


def step_completed(test_to_use):
    """
    This function deals with execution of all the
    tests in sequence and returns the result
    """

    load = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(load.loadTestsFromTestCase(test_to_use))
    runtest = unittest.TextTestRunner(verbosity=2)
    result = runtest.run(suite)

    if result.skipped:
        return False

    return result.wasSuccessful()


def testing():
    """
    This function executes the function of step_completed
    """
    print('*'*60 + "\nTesting:\n")
    return step_completed(TestClient)

if __name__ == "__main__":
    if testing() is not True:
        print("\n\tThe tests did not pass,")
        sys.exit(1)

    sys.exit(0)