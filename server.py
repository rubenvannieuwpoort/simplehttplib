from simplehttpserver import *

responseHtml = '<html><head><title>Hello world</title></head><body><h1>Hello</h1><p>Hi there.</p></body></html>'
response = Response('HTTP/1.1', 200, {}, responseHtml.encode())

with ConnectionListener(8080) as connectionListener:
    while True:
        with connectionListener.waitForRequest() as (connection, origin, request):
            print(f'Received request from {origin}:\n{request.decode()}')
            connection.send(response)
