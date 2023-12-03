from socket import *

# return index of file in cache array, -1 otherwise
def isInCache(route, cache):
    for (i, item) in enumerate(cache):
        if item.route == route:
            return i
    return -1

httpVersion = "HTTP/1.1"
statusLine200 = httpVersion + " 200 OK\r\n"

serverPort = 8000
originServerPort = 9000
originServerName = 'localhost'
serverSocket = socket(AF_INET, SOCK_STREAM) # socket to connect to client
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(5)
print("The proxy server ready to receive")
cache = []
while True:
    originServerSocket = socket(AF_INET, SOCK_STREAM) # socket to connect to origin server
    connectionSocket, addr = serverSocket.accept()
    encodedData = connectionSocket.recv(1024)
    data = encodedData.decode('utf-8')
    method = data.split(' ')[0]
    route = data.split(' ')[1]
    httpVersion = data.split(' ')[2]
    headerRaw = data.split("\r\n\r\n")[0].split("\r\n")[1:]
    header = {}
    for heading in headerRaw:
        key = heading.split(":")[0]
        value = heading.split(":")[1]
        header[key] = value
    
    if method == "GET": # we only care if the client is sending a GET request, otherwise forward to origin server
        itemIndex = isInCache(route, cache) # check if file is stored in cache
        if itemIndex != -1: # cache hit
            print("yo mama")
        else: # cache miss
            originServerSocket.connect((originServerName, originServerPort))
            originServerSocket.send(encodedData)
            forwardedData = originServerSocket.recv(1024)
            connectionSocket.send(forwardedData)
            originServerSocket.close()
    else: 
        originServerSocket.connect((originServerName, originServerPort))
        originServerSocket.send(encodedData)
        forwardedData = originServerSocket.recv(1024)
        connectionSocket.send(forwardedData)
        originServerSocket.close()

    connectionSocket.shutdown(SHUT_WR)
    connectionSocket.close()

    
