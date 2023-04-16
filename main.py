# Cheung Man Tik Tommy
# 22083184D
#
# Comp2322 Project

import socket
import asyncio
from time import process_time
import os 

class HTTPResponse(object):
    OK = "HTTP/1.1 200 OK\n\n"
    BAD_REQUEST = "HTTP/1.1 400 Bad Request\n\n"
    NOT_FOUND = "HTTP/1.1 404 Not Found\n\n"
    NOT_MODIFIED = "HTTP/1.1 304 Not Modified\n\n"


class TypeOfContent(object):
    HTML = 'Content-Type: text/html\n\n'
    PNG = 'Content-Type: img/png\n\n'
    JPG = 'Content-Type: img/jpg\n\n'


class HTTPRequest(object):
    def __init__(self):
        self.HTTPMethod = None
        self.FileURL = None
        self.HTTPVersion = None
        self.HTTPStatus = None
        self.ResponseHead = ""
        self.ResponseBody = ""
        self.keep_alive = False


    @staticmethod
    def ProcessingHeader(request):
        """
        To seperate different parts of HTTP header into different variables
        
        Input: decoded HTTP request
        Output: RequestType (GET or HEAD), FileName (The name of the file requested), RestOfHeader ({Other headers})
        """

        RestOfHeader = {}
        # Divide GET and path for the file
        fields = request[0].split()
        RequestType = fields[0]
        FileName = fields[1]

        for header in request:
            if header.find(": ") != -1:     # Find the header with ": "
                HeaderName, HeaderValue = header.split(": ")
                RestOfHeader[HeaderName.lower()] = HeaderValue
        
        return RequestType.upper(), FileName, RestOfHeader


    def ProcessingRequest(self, request):
        FilePath = ""
        BadRequestStatus = False

        self.HTTPMethod, self.FileURL, RestOfHeader = HTTPRequest.ProcessingHeader(request)
        print(self.HTTPMethod, self.FileURL)

        # Checking HTTP Method
        if self.HTTPMethod == "GET" or self.HTTPMethod == "HEAD":
            if self.FileURL == '/':
                FilePath = 'index.html'
            FilePath = "htdocs/" + FilePath

        else:   # 400 Bad Request
            BadRequestStatus = True
            FilePath = "htdocs/400.html"

        # Checking keep-alive
        if 'connection' in RestOfHeader and RestOfHeader["connection"] == "keep-alive":
            self.keep_alive == True

        self.DraftingResponse(self.HTTPMethod, FilePath, RestOfHeader, BadRequestStatus)


    def DraftingResponse(self, HTTPMethod, FilePath, HeaderDict, BadRequestStatus):

        # Look for the required file
        FileExistFlag = True    # Because we always can find 400 and 404 html

        if not os.path.isfile(FilePath):
            FileExistFlag = False




async def ServerInitialization(serverSocket):
    while True:
        # t1_start = process_time()

        connectedSocket, clientAddress = await loop.sock_accept(serverSocket)
        await ServerManager(connectedSocket, clientAddress)

        # t1_stop = process_time()
        # print("Elapsed time:", t1_stop, t1_start)
        # print("Elapsed time during the whole program in seconds:", t1_stop-t1_start)





async def ServerManager(connectedSocket, clientAddress):
    response = await CreateResponse(connectedSocket, clientAddress)
    await loop.sock_sendall(connectedSocket, response)
    connectedSocket.close()





async def CreateResponse(connectedSocket, clientAddress):

    request = (await loop.sock_recv(connectedSocket, 2048)).decode("utf8")
    request = [x.strip() for x in request.split('\r\n')]

    if request == "" or request == [] or request == [""]:   # Sometime this happens, maybe due to refresh frequently
        return HTTPResponse.NOT_FOUND.encode("utf8")       # This is here to avoid runtime error

    RequestMessage = HTTPRequest()
    RequestType, FileName = RequestMessage.ProcessingRequest(request)

    # if RequestType == "GET":
    # # process the GET request
    #     try:
    #         with open("htdocs" + FileName) as file:
    #             content = file.read()
    #             response = HTTPResponse.OK + content
    #     except:
    #         with open("htdocs/404.html") as file:
    #             content = file.read()
    #             response = HTTPResponse.NOT_FOUND + content # 200
    

    # elif RequestType == "HEAD":
    #     try:
    #         if FileName == '/':
    #             FileName = '/index.html'

    #         with open("htdocs" + FileName) as file:
    #             content = file.read()  # Fail proof
    #             response = HTTPResponse.OK + content
    #     except:
    #             response = HTTPResponse.NOT_FOUND           # 404
    

    # else:
    #     response = HTTPResponse. BAD_REQUEST + "Request Not Supported"  # 400

    return response.encode("utf8")













serverAddress = "localhost"
serverPort = 2130

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((serverAddress, serverPort))
serverSocket.listen(128)





loop = asyncio.get_event_loop()
print(f"Listening on {serverPort}")
loop.run_until_complete(ServerInitialization(serverSocket))


