from socket import *

httpVersion = "HTTP/1.1"
statusLine200 = "{} 200 OK\r\n", httpVersion
statusLine304 = "{} 304 Not Modified\r\n", httpVersion
statusLine400 = "{} 400 Bad Request\r\n", httpVersion
statusLine403 = "{} 403 Forbidden\r\n", httpVersion
statusLine404 = "{} 404 Not Found\r\n", httpVersion
statusLine411 = "{} 411 Length required\r\n", httpVersion


serverPort = 9000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(5)
print("The server ready to receive")
while True:
    connectionSocket, addr = serverSocket.accept()
    data = connectionSocket.recv(1024).decode('utf-8')
    method = data.split(' ')[0]
    route = data.split(' ')[1]
    print(data)
    print(data.split("\r\n\r\n"))

    if method == 'GET':
        if route == ("/test.html"):
            f = open("test.html", "r")
            http = "HTTP/1.1 200 OK\n" + "Content-Type: text/html\n"+"\n"+f.read()
        else:
            http = "HTTP/1.1 404 Not Found\n\n404 Not Found"
    
    

    # do stuff
   
    connectionSocket.send(http.encode())
    connectionSocket.shutdown(SHUT_WR)
    connectionSocket.close()
connectionSocket.close()