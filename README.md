# Simple HTTP library

Simple HTTP library in Python. For educational purposes. Wraps the use of sockets and provides an interface around HTTP requests/responses. Does not support [chunked transfer encoding](https://en.wikipedia.org/wiki/Chunked_transfer_encoding) or HTTPS.

Currently, 

Example code for a client:
```
from simplehttpserver import *

origin = Origin('info.cern.ch', 80)
request = Request('GET', '/', 'HTTP/1.1', { 'Host': 'info.cern.ch:80' }, b'')

responseData = getResponseDataForRequest(origin, request)  # get raw response data
response = Response.fromData(responseData)  # create a Response object from the response data
print(f'Server responded:\n{response.data()}')
```

Example code for a (single-threaded, blocking) server:
```
from simplehttpserver import *

responseHtml = '<html><head><title>Hello world</title></head><body><h1>Hello</h1><p>Hi there.</p></body></html>'
response = Response('HTTP/1.1', 200, {'Content-Length': len(responseHtml)}, responseHtml.encode())

with ConnectionListener(8080) as connectionListener:
    while True:
        with connectionListener.waitForConnection() as connection:
            requestData = connection.receiveData()
            print(f'Received request from {connection.origin}:\n{requestData}')
            request = Request.fromData(requestData)
            connection.sendResponse(response)
```
