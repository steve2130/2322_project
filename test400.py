import http.client
import pprint

Connection = http.client.HTTPConnection("localhost", 2130)

Header = {"Connection" : "keep-alive"}
Connection.request("POST", "/", headers=Header)
Response = Connection.getresponse() # response
print(f"{Connection.status} {Connection.reason}")
ResponseHeader = Response.getheaders()
pp = pprint.PrettyPrinter(indent = 4)
pp.pprint(f"Headers: {ResponseHeader}")
print(f"Response Content:\n{ResponseHeader.read().decode()}") # utf8: string 
Connection.close()