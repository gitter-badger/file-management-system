'''
This file is the client program using async I/O
--------
After the connection has been established the
user commands are executed as per the CommandHandler class
--------
The connection is closed based on the user request
'''
import asyncio

async def tcp_client():
    '''
    This function establishes the TCP connection between the server and the client
    '''
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8088)
    message = ''
    while True:
        message = input("$")
        if message == "":
            print("$")
            continue

        writer.write(message.encode())
        data = await reader.read(4096)
        print(f"{data.decode()}")
        if message.lower() == "quit":
            break
    print('Close the connection')
    writer.close()

asyncio.run(tcp_client())
