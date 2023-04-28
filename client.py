from simplehttpserver import *

origin = Origin('remote-server', 8080)
request = Request('GET', '/', 'HTTP/1.1', {}, b'')

response = getResponseForRequest(origin, request)
pass
