# Cheung Man Tik Tommy
# 22083184D
#
# Comp2322 Project

import socket
import asyncio





class HTTPresponse(object):
    OK = "HTTP/1.1 200 OK\n\n"
    BAD_REQUEST = "HTTP/1.1 400 Bad Request\n\n"
    NOT_FOUND = "HTTP/1.1 404 Not Found\n\n"
    NOT_MODIFIED = "HTTP/1.1 304 Not Modified"
    

def main():
    serverAddress = "127.0.0.1"
    serverPort = 2130

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((serverAddress, serverPort))
    serverSocket.listen(5)

    while True:
        # Wait for client connections
        client_connection, client_address = serverSocket.accept()
        
        # Get the client request
        request = client_connection.recv(1024).decode()
        print(request)
        
        # Send HTTP response
        response = 'HTTP/1.1 200 OK\n\nHello World'
        client_connection.sendall(response.encode())
        client_connection.close()
    
    # Close socket
    server_socket.close()





if __name__ == "__main__":
    main()

