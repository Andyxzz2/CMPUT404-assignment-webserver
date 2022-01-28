#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/
baseurl = "http://127.0.0.1:8080"

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        self.request.sendall(bytearray("OK",'utf-8'))
        decoded_data = self.data.decode('utf-8')
        request = decoded_data.split()
        method = request[0]
        path = request[1]

        if self.check_method(method):
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed", 'utf-8'))
            
        elif self.check_path(path):
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", 'utf-8'))

        else:
            self.response(method, path)
            

    def check_method(self, method):
        if method != "GET":
            return True
        else:
            return False

    def check_path(self, path):
        if "/." in path or "/.." in path:
            return True
        else:
            return False

    def response(self, method, path):
        full_path = os.path.abspath('www'+path)
        if os.path.isfile(full_path):
            if full_path.endswith("html"):

                file = open(path)
                serving_file = file.read()
                self.request.sendall(bytearray(f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{serving_file}', 'utf-8'))
                file.close()

            elif full_path.endswith("css"):
                
                file = open(path)
                serving_file = file.read()
                self.request.sendall(bytearray(f'HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n{serving_file}', 'utf-8'))
                file.close()

        elif os.full_path.isdir(full_path):
            if full_path.endswith("/"):
                path = path + "index.html"
                full_path = os.path.abspath('www'+path)

                file = open(path)
                serving_file = file.read()
                self.request.sendall(bytearray(f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{serving_file}', 'utf-8'))
                file.close()

            else:
                new_route = path + '/'
                self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: " + baseurl + new_route + "\r\n", 'utf-8'))

        else:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
