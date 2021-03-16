'''
This file is the server program using async I/O
--------
'''
import asyncio
import signal
from CommandHandler import CommandHandler

signal.signal(signal.SIGINT, signal.SIG_DFL)

def client_request(commandhandler, message):
    '''
    This function initiates the functions for given commands by user
    '''
    message = message.rstrip("\n").rstrip(" ").lstrip(" ")
    if message.split(" ")[0] == "commands":
        return commandhandler.commands()
    if message.split(" ")[0] == "register":
        if len(message.split(" ")) == 3:
            return commandhandler.register(message.split(" ")[1], message.split(" ")[2])
        return "Enter correct command"

    if message.split(" ")[0] == "login":
        if len(message.split(" ")) == 3:
            return commandhandler.login(message.split(" ")[1], message.split(" ")[2])
        return "Enter Right Command"

    if message.split(" ")[0] == "quit":
        return commandhandler.quit()
    
    if message.split(" ")[0] == "list":
        return commandhandler.list()

    if message.split(" ")[0] == "write_file":
        if len(message.split(" ")) >= 2:
            return commandhandler.write_file(message.split(" ")[1], " ".join(message.split(" ")[2:]))
        return "Enter correct command"

    if message.split(" ")[0] == "create_folder":
        if len(message.split(" ")) == 2:
            return commandhandler.create_folder(message.split(" ")[1])

        return "Enter correct command"
    
    if message.split(" ")[0] == "change_folder":
        if len(message.split(" ")) == 2:
            return commandhandler.change_folder(message.split(" ")[1])
        return "Enter correct command"

    if message.split(" ")[0] == "read_file":
        if len(message.split(" ")) == 2:
            return commandhandler.read_file(message.split(" ")[1])
        return "Enter correct command"

    
async def handle_echo(reader, writer):
    '''
    This funtion acknowledges the connection from the client,
    acknowledges the messages from the client
    '''
    addr = writer.get_extra_info('peername')
    message = f"{addr} is connected !!!!"
    print(message)
    commandhandler = CommandHandler()
    while True:
        data = await reader.read(4096)
        message = data.decode().strip()
        if message == 'exit':
            break

        print(f"Received {message} from {addr}")
        mymsg = client_request(commandhandler, message)
        msg = str(mymsg).encode()
        writer.write(msg)
        await writer.drain()
    print("Close the connection")
    writer.close()


async def main():
    '''
    This function starts the connection between the server and client
    '''
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8088)


    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


asyncio.run(main())

