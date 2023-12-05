from socket import *
from datetime import datetime

def processHttpReqHeader(data):
    method = data.split(' ')[0]
    route = data.split(' ')[1]
    httpVersion = data.split(' ')[2]
    headerRaw = data.split("\r\n\r\n")[0].split("\r\n")[1:]
    headers = {}
    for heading in headerRaw:
        key = heading.split(":")[0]
        value = heading.split(":")[1]
        headers[key] = value
    return method, route, httpVersion, headers

httpVersion = "HTTP/1.1"
statusLine200 = httpVersion + " 200 OK\r\n"
statusLine304 = httpVersion + " 304 Not Modified\r\n"
statusLine400 = httpVersion + " 400 Bad Request\r\n"
statusLine403 = httpVersion + " 403 Forbidden\r\n"
statusLine404 = httpVersion + " 404 Not Found\r\n"
statusLine411 = httpVersion + " 411 Length required\r\n"

supportedMethods = ["GET", "POST"]
num_of_reqs = 0

serverPort = 9000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(5)
print("The server ready to receive")
while True:
    connectionSocket, addr = serverSocket.accept()
    data = connectionSocket.recv(1024).decode('utf-8')
    num_of_reqs += 1
    print("request number {} received from client at time {}".format(num_of_reqs, datetime.now().strftime("%H:%M:%S")))
    method, route, httpVersion, headers = processHttpReqHeader(data)

    # check for malformed request, respond with status code 400
    if not route.startswith("/") or not httpVersion.startswith("HTTP/") or method not in supportedMethods:
        http = statusLine400 + "\r\n"
    elif route == "/":
        if method == "POST" and "Content-Length" not in headers: # if post requests w/o content-length header
            http = statusLine411 +"\r\n"
        else:
            http = statusLine200 + "\r\n"
    elif route == "/test.html":
        if method == "GET":
            if "If-Modified-Since" in headers:
                http = "HTTP/1.1 304 Not Modified\r\n\r\n"
            else: 
                f = open("test.html", "r")
                http = "HTTP/1.1 200 OK\r\n" + "Content-Type: text/html\r\n"+"\r\n"+f.read()
    elif route == "/secure": # secure route, exists but is forbidden 
        http = statusLine403 + "\r\n" + "this route is forbidden for regular users"
    else:
        http = "HTTP/1.1 404 Not Found\r\n\r\n"

    connectionSocket.send(http.encode())
    connectionSocket.shutdown(SHUT_WR)
    connectionSocket.close()
 