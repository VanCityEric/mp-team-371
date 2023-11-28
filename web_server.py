from socket import *

httpVersion = "HTTP/1.1"
statusLine200 = httpVersion + " 200 OK\r\n"
statusLine304 = httpVersion + " 304 Not Modified\r\n"
statusLine400 = httpVersion + " 400 Bad Request\r\n"
statusLine403 = httpVersion + " 403 Forbidden\r\n"
statusLine404 = httpVersion + " 404 Not Found\r\n"
statusLine411 = httpVersion + " 411 Length required\r\n"

possibleMethods = ["GET"]

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
    ver = data.split(' ')[2]
    print(method)
    print(route)
    headerRaw = data.split("\r\n\r\n")[0].split("\r\n")[1:]
    print(data + "\n")
    header = {}
    for heading in headerRaw:
        key = heading.split(":")[0]
        value = heading.split(":")[1]
        header[key] = value
    print("ROUTE IS " + route)
    # check for malformed request, respond with status code 400
    if not route.startswith("/") or not ver.startswith("HTTP/") or method not in possibleMethods:
        http = statusLine400 + "\n"
    if route == "/":
        http = "HTTP/1.1 404 Not Found\r\n\n"
    if route == "/test.html":
        if method == "GET":
            if "If-Modified-Since" in header:
                http = "HTTP/1.1 304 Not Modified\r\n\n"
            else: 
                f = open("test.html", "r")
                http = "HTTP/1.1 200 OK\r\n" + "Content-Type: text/html\n"+"\n"+f.read()
    else:
        http = "HTTP/1.1 404 Not Found\r\n"

    # do stuff

    connectionSocket.send(http.encode())
    connectionSocket.shutdown(SHUT_WR)
    connectionSocket.close()