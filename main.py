# Cheung Man Tik Tommy
# 22083184D
#
# Comp2322 Project

import socket
import asyncio
# from time import process_time
import os 
import datetime
from email import utils

class HTTPStatus(object):
    OK = "HTTP/1.1 200 OK\r\n"
    BAD_REQUEST = "HTTP/1.1 400 Bad Request\r\n"
    NOT_FOUND = "HTTP/1.1 404 Not Found\r\n"
    NOT_MODIFIED = "HTTP/1.1 304 Not Modified\r\n"


class TypeOfContent(object):
    HTML = 'Content-Type: text/html\r\n'
    PNG = 'Content-Type: img/png\r\n'
    JPG = 'Content-Type: img/jpg\r\n'


class HTTPResponse(object):
    def __init__(self):
        # Essential Header
        self.HTTPStatus = None
        self.Date = None
        self.Server = "Server: Tommy's overnight work!!!!!!\r\n"
        self.ContentType = None

        # Optional Header
        self.Connection = ""
        self.KeepAlive = ""
        self.LastModified = ""
        
        # The message itself
        self.ResponseHeader = ""
        self.ResponseBody = ""
        self.Response = ""

    
    def GetHTTPDate(self):
        # https://stackoverflow.com/questions/3453177/convert-python-datetime-to-rfc-2822
        RFC2822Date = utils.format_datetime(datetime.datetime.now())
        return RFC2822Date

    def CreateResponseHeader(self):
        self.ResponseHeader = self.HTTPStatus + self.ContentType + "Date: " + self.Date + "\r\n" + self.Server + self.Connection + self.KeepAlive + self.LastModified + "\r\n"
        return self.ResponseHeader

class HTTPRequest(object):
    def __init__(self):
        self.HTTPMethod = None
        self.FileURL = None
        self.HTTPVersion = None
        self.HTTPStatus = None
        self.KeepAlive = False
        self.IfModifiedSince = None


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
                RestOfHeader[HeaderName.lower()] = HeaderValue.lower()
        
        return RequestType.upper(), FileName, RestOfHeader


    def ProcessingRequest(self, request):
        FilePath = ""
        BadRequestStatus = False

        self.HTTPMethod, self.FileURL, RestOfHeader = HTTPRequest.ProcessingHeader(request)
        print(self.HTTPMethod, self.FileURL)

        # Checking HTTP Method
        if self.HTTPMethod == "GET" or self.HTTPMethod == "HEAD":
            if self.FileURL == '/':
                self.FileURL = '/index.html'
            FilePath = "htdocs" + self.FileURL

        else:   # 400 Bad Request
            BadRequestStatus = True
            FilePath = "htdocs/400.html"

        # Checking keep-alive
        if 'connection' in RestOfHeader and RestOfHeader["connection"] == "keep-alive":
            self.KeepAlive = True

        return (FilePath, RestOfHeader, BadRequestStatus)



#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------


async def ServerInitialization(serverSocket):
    while True:
        # t1_start = process_time()

        connectedSocket, clientAddress = await loop.sock_accept(serverSocket)
        await ServerManager(connectedSocket)

        # t1_stop = process_time()
        # print("Elapsed time:", t1_stop, t1_start)
        # print("Elapsed time during the whole program in seconds:", t1_stop-t1_start)



async def ServerManager(connectedSocket):
    response = await CreateResponse(connectedSocket)
    await loop.sock_sendall(connectedSocket, response)
    connectedSocket.close()





async def CreateResponse(connectedSocket):

    request = (await loop.sock_recv(connectedSocket, 2048)).decode("utf8")
    request = [x.strip() for x in request.split('\r\n')]

    if request == "" or request == [] or request == [""]:   # Sometime this happens, maybe due to refresh frequently
        return HTTPStatus.NOT_FOUND.encode("utf8")       # This is here to avoid runtime error

    RequestMessage = HTTPRequest()
    TypeOfFile = TypeOfContent()
    ResponseMessage = HTTPResponse()
    FilePath, HeaderDict, BadRequestStatus = RequestMessage.ProcessingRequest(request)

    if RequestMessage.KeepAlive == True:
        ResponseMessage.Connection = "Connection: Keep-Alive\r\n"
        ResponseMessage.KeepAlive = "Keep-Alive: timeout=10, max=997\r\n"
        

    # Look for the required file
    FileExistFlag = False
    if os.path.isfile(FilePath):
        FileExistFlag = True


    ResponseMessage.Date = ResponseMessage.GetHTTPDate()

    if BadRequestStatus == True:    # 400
        ResponseMessage.HTTPStatus = HTTPStatus.BAD_REQUEST

    else:
        if FileExistFlag == True:
            FileExtension = FilePath.split(".")
            FileExtension = FileExtension[(len(FileExtension) - 1)].lower()     # Get the extension (jpg, png, html)
            ResponseMessage.LastModified = "Last-Modified: " + ResponseMessage.GetHTTPDate() + "\r\n"

            if "if-modified-since" in HeaderDict:
                SinceTimestamp = HeaderDict["if-modified-since"]
                SinceTimestamp = datetime.datetime.strptime(SinceTimestamp, '%a, %d %b %Y %H:%M:%S GMT').timestamp()




            if FileExtension == "jpg" or FileExtension == "png":
                with open(FilePath, "rb") as File:  # open image in binary mode
                    ResponseMessage.ResponseBody = File.read()
                    ResponseMessage.HTTPStatus = HTTPStatus.OK
                    
                    if FileExtension == "jpg":
                        ResponseMessage.ContentType = TypeOfFile.JPG

                    elif FileExtension == "png":
                        ResponseMessage.ContentType = TypeOfFile.PNG

                ResponseMessage.ResponseHeader = ResponseMessage.CreateResponseHeader()



            elif FileExtension == "html":
                with open(FilePath, "r") as File:
                    ResponseMessage.ResponseBody = File.read()
                    ResponseMessage.HTTPStatus = HTTPStatus.OK
                    ResponseMessage.ContentType = TypeOfFile.HTML
                
                ResponseMessage.ResponseHeader = ResponseMessage.CreateResponseHeader()

            if RequestMessage.HTTPMethod == "HEAD":
                # return only the header    
                # Should be a nest higher if statement but I am too lazy on recreating header
                ResponseMessage.ResponseBody = ""
                # Send the exactly header as using GET
                ResponseMessage.ResponseHeader = ResponseMessage.CreateResponseHeader()


        else:  # Cannot find the file
            FilePath = "htdocs/404.html"
            with open(FilePath, "r") as File:
                ResponseMessage.ResponseBody = File.read()
                ResponseMessage.HTTPStatus = HTTPStatus.NOT_FOUND
                ResponseMessage.ContentType = TypeOfFile.HTML

            if RequestMessage.HTTPMethod == "HEAD":
                ResponseMessage.ResponseBody = ""


    # Create response for GET
    if isinstance(ResponseMessage.ResponseBody, str):   # Meaning ResponseBody contains HTML file 
        ResponseMessage.Response = (ResponseMessage.ResponseHeader + ResponseMessage.ResponseBody).encode("utf8") 
        return ResponseMessage.Response

    else:   # Meaning ResponseBody contains an image
        ResponseMessage.Response = (ResponseMessage.ResponseHeader).encode("utf8") + ResponseMessage.ResponseBody
        return ResponseMessage.Response
    





    # if RequestType == "GET":
    # # process the GET request
    #     try:
    #         with open("htdocs" + FileName) as file:
    #             content = file.read()
    #             response = HTTPStatus.OK + content
    #     except:
    #         with open("htdocs/404.html") as file:
    #             content = file.read()
    #             response = HTTPStatus.NOT_FOUND + content # 200
    

    # elif RequestType == "HEAD":
    #     try:
    #         if FileName == '/':
    #             FileName = '/index.html'

    #         with open("htdocs" + FileName) as file:
    #             content = file.read()  # Fail proof
    #             response = HTTPStatus.OK + content
    #     except:
    #             response = HTTPStatus.NOT_FOUND           # 404
    

    # else:
    #     response = HTTPStatus. BAD_REQUEST + "Request Not Supported"  # 400

    # return response.encode("utf8")













serverAddress = "localhost"
serverPort = 2130

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((serverAddress, serverPort))
serverSocket.listen(128)





loop = asyncio.get_event_loop()
print(f"Listening on Port {serverPort}")
loop.run_until_complete(ServerInitialization(serverSocket))


