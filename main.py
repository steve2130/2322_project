# Cheung Man Tik Tommy
# 22083184D
#
# Comp2322 Project

import socket
import asyncio
from time import process_time 

class HTTPresponse(object):
    OK = "HTTP/1.1 200 OK\n\n"
    BAD_REQUEST = "HTTP/1.1 400 Bad Request\n\n"
    NOT_FOUND = "HTTP/1.1 404 Not Found\n\n"
    NOT_MODIFIED = "HTTP/1.1 304 Not Modified\n\n"
    




async def ServerInitialization(serverSocket):
    loop = asyncio.get_event_loop()
    while True:
        print(f"Listening on {serverPort}")

        # t1_start = process_time()  

        connectedSocket, clientAddress = await loop.sock_accept(serverSocket)
        await ServerManager(connectedSocket, clientAddress)

        # t1_stop = process_time() 
        # print("Elapsed time:", t1_stop, t1_start)  
        # print("Elapsed time during the whole program in seconds:", t1_stop-t1_start)





async def ServerManager(connectedSocket, clientAddress):
    request = await ReadRequest(connectedSocket)
    response = await CreateResponse(request, clientAddress)
    await loop.sock_sendall(connectedSocket, response)
    connectedSocket.close()





async def ReadRequest(connectedSocket):
    request = (await loop.sock_recv(connectedSocket, 4096)).decode("utf8")
    print(request)
    return [x.strip() for x in request.split('\n')]





async def CreateResponse(request, clientAddress):
        fields = request[0].split()
        request_type = fields[0]
        file_name = fields[1]


        if request_type == "GET":
        # process the GET request
            try:
                # filename = 
                if file_name == '/':
                    file_name = '/index.html'

                # if filename.contains():

                with open("htdocs" + file_name) as file:
                    content = file.read()
                    response = HTTPresponse.OK + content
            except:
                with open("htdocs/404.html") as file:
                    content = file.read()
                    response = HTTPresponse.NOT_FOUND + content
        else:
            response = HTTPresponse. BAD_REQUEST + "Request Not Supported"

        return response.encode("utf8")













serverAddress = "localhost"
serverPort = 2130

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((serverAddress, serverPort))
serverSocket.listen(128)





loop = asyncio.get_event_loop()
loop.run_until_complete(ServerInitialization(serverSocket))


