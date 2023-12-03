from socket import *

httpVersion = "HTTP/1.1"
statusLine200 = httpVersion + " 200 OK\r\n"
statusLine304 = httpVersion + " 304 Not Modified\r\n"
statusLine400 = httpVersion + " 400 Bad Request\r\n"
statusLine403 = httpVersion + " 403 Forbidden\r\n"
statusLine404 = httpVersion + " 404 Not Found\r\n"
statusLine411 = httpVersion + " 411 Length required\r\n"

supportedMethods = ["GET", "POST"]


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
    httpVersion = data.split(' ')[2]
    headerRaw = data.split("\r\n\r\n")[0].split("\r\n")[1:]
    header = {}
    for heading in headerRaw:
        key = heading.split(":")[0]
        value = heading.split(":")[1]
        header[key] = value
    
    print(data + "\n")
    print(method)
    print(route)
    print("ROUTE IS " + route)
    # check for malformed request, respond with status code 400
    if not route.startswith("/") or not httpVersion.startswith("HTTP/") or method not in supportedMethods:
        http = statusLine400 + "\n"
    elif route == "/":
        if method == "POST" and "Content-Length" not in header: # if post requests w/o content-length header
            http = statusLine411 +"\n"
        else:
            http = statusLine200 + "\n"
    elif route == "/test.html":
        if method == "GET":
            if "If-Modified-Since" in header:
                http = "HTTP/1.1 304 Not Modified\r\n\n"
            else: 
                f = open("test.html", "r")
                http = "HTTP/1.1 200 OK\r\n" + "Content-Type: text/html\n"+"\n"+f.read()
    elif route == "/secure": # secure route, exists but is forbidden 
        http = statusLine403 + "\n" + "this route is forbidden for regular users"
    else:
        http = "HTTP/1.1 404 Not Found\r\n"

    connectionSocket.send(http.encode())
    connectionSocket.shutdown(SHUT_WR)
    connectionSocket.close()
 
