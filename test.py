import http.client
import pprint

# I am UAT file
# I can test server's response on
#        HTTP request method and HTTP request header


Connection = http.client.HTTPConnection("localhost", 2130)
Method = input("Input the method you would like to try. (GET, POST, HEAD)\n")
Method = Method.upper()

Header = {
          "Connection" : "keep-alive",
          "If-Modified-Since": "Tue, 18 Apr 2023 23:59:59 -0000"
         }
Connection.request(Method, "/", headers=Header)
Response = Connection.getresponse() # response
print(f"{Response.status} {Response.reason}")
ResponseHeader = Response.getheaders()
pp = pprint.PrettyPrinter(indent = 4)
pp.pprint(f"Headers: {ResponseHeader}")
print(f"Response Content:\n{Response.read().decode()}") # utf8: string 
Connection.close()