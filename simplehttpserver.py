import socket


MAX_SIZE = 1 << 20


class Origin:
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def __str__(self):
        return f'[{self.address}]:{self.port}'


class Connection:
    def __init__(self, origin, connection = None):
        self.origin = origin
        if connection is None:
            self.connection = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
            self.connection.connect((origin.address, origin.port))
        else:
            self.connection = connection

    def receiveData(self):
        return self.connection.recv(MAX_SIZE)

    def receiveRequest(self):
        return Request.fromData(self.receiveData())

    def sendData(self, data):
        self.connection.send(data)

    def sendRequest(self, request):
        self.sendData(request.data())

    def sendResponse(self, response):
        self.sendData(response.data())

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.connection.close()


class Request:
    def __init__(self, method, path, protocol, headers, content):
        self.Method = method
        self.Path = path
        self.Protocol = protocol
        self.Headers = headers
        self.Content = content

    def data(self):
        return (f'{self.Method} {self.Path} {self.Protocol}\r\n' + '\r\n'.join(map(lambda k: f'{k}: {self.Headers[k]}', self.Headers)) + '\r\n\r\n').encode() + self.Content
    
    def fromData(data):
        headerData, content = data.split(b'\r\n\r\n')
        args = headerData.decode().split('\r\n', 1)
        statusLine = args[0]
        if len(args) > 1:
            headerText = args[1]
            headers = { header: value for header, value in map(lambda x: x.split(':', 1), headerText.split('\r\n')) }
        else:
            headers = {}
        method, path, protocol = statusLine.split()
        return Request(method, path, protocol, headers, content)


class ConnectionListener:
    def __init__(self, port):
        self.port = port

    def start(self):
        self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.socket.bind(('::', self.port))
        self.socket.listen()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def waitForConnection(self):
        conn, (address, port, _, _) = self.socket.accept()
        return Connection(Origin(address, port), conn)

    def close(self):
        self.socket.close()


class Response:
    def __init__(self, protocol, status, headers, content):
        self.Protocol = protocol
        self.Status = status
        self.Headers = headers
        self.Content = content

    def data(self):
        return (f'{self.Protocol} {self.Status}\r\n' + '\r\n'.join(map(lambda k: f'{k}: {self.Headers[k]}', self.Headers)) + '\r\n\r\n').encode() + self.Content

    def fromData(data):
        headerData, content = data.split(b'\r\n\r\n')
        statusLine, headerText = headerData.decode().split('\r\n', 1)
        protocol, status = statusLine.split(' ', 1)
        headers = { header: value for header, value in map(lambda x: x.split(':', 1), headerText.split('\r\n')) }
        return Response(protocol, status, headers, content)


def getResponseDataForRequest(origin, request):
    connection = Connection(origin)
    connection.sendRequest(request)
    responseData = connection.receiveData()
    return responseData

def getResponseForRequest(origin, request):
    return Response(getResponseDataForRequest(origin, request))
