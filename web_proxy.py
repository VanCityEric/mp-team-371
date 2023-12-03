from socket import *

# return index of file in cache array, -1 otherwise
def isInCache(route, cache):
    for (i, obj) in enumerate(cache):
        print(obj)
        if obj["route"] == route:
            return i
    return -1

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

def processHttpBody(data):
    return data.split("\r\n\r\n")[1]

httpVersion = "HTTP/1.1"
statusLine200 = httpVersion + " 200 OK\r\n"

serverPort = 8000
originServerPort = 9000
originServerName = 'localhost'
cache = []
serverSocket = socket(AF_INET, SOCK_STREAM) # socket to connect to client
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(5)
print("The proxy server ready to receive")

while True:
    connectionSocket, addr = serverSocket.accept()
    data = connectionSocket.recv(1024).decode('utf-8')
    method, route, httpVersion, headers = processHttpReqHeader(data)
    originServerSocket = socket(AF_INET, SOCK_STREAM) # socket to connect to origin server
    
    if method == "GET": # we only care if the client is sending a GET request, otherwise forward request to origin server
        cacheIndex = isInCache(route, cache)
        if cacheIndex != -1: # cache hit
            print("yo mama")
        else: # cache miss
            originServerSocket.connect((originServerName, originServerPort))
            originServerSocket.send(data.encode('utf-8'))
            forwardedData = originServerSocket.recv(1024).decode("utf-8")
            cache.append({'route': route, 'data': processHttpBody(forwardedData)}) 
            connectionSocket.send(forwardedData.encode("utf-8"))
            originServerSocket.close()
    else: 
        originServerSocket.connect((originServerName, originServerPort))
        originServerSocket.send(data.encode('utf-8'))
        forwardedData = originServerSocket.recv(1024)
        connectionSocket.send(forwardedData)
        originServerSocket.close()

    connectionSocket.shutdown(SHUT_WR)
    connectionSocket.close()

    
