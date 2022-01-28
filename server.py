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

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):

        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        
        #get request and splite method(only GET) and path 
        self.data = self.data.decode('utf-8')
        temp_data = self.data.split()
        method = temp_data[0]
        path = temp_data[1]

        #check invalid method
        if self.check_method(method):
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed", 'utf-8'))

        #check invalid path    
        elif self.check_path(path):
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", 'utf-8'))

        #start handle
        else:
            self.response(method, path)
            
    #this function simply check if method is "GET"
    def check_method(self, method):
        if method != "GET":
            return True
        else:
            return False

    #this method check if a same level path or last level path is given
    def check_path(self, path):
        if "/." in path or "/.." in path:
            return True
        else:
            return False

    #all test pass, start response
    def response(self, method, path):

        #get full path and compare in local
        full_path = os.path.abspath('www'+path)

        #if the given pass is a file, check if it is a html request or css request
        if os.path.isfile(full_path):
            if full_path.endswith('html'):

                file = open(full_path)
                data = file.read()
                self.request.sendall(bytearray(f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{data}', 'utf-8'))
                file.close()

            elif full_path.endswith('css'):
                
                file = open(full_path)
                data = file.read()
                self.request.sendall(bytearray(f'HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n{data}', 'utf-8'))
                file.close()

        #if the path is a dir
        elif os.path.isdir(full_path):
            
            #if dir ends with /, add 'index.html' to open it
            if full_path.endswith('/'):
                new_route = path +'index.html'
                full_path = os.path.join(os.getcwd()+"/www"+new_route)
                file = open(full_path)
                data = file.read()
                self.request.sendall(bytearray(f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{data}\r\n', 'utf-8'))
                file.close()
            
            #if not, redirct, add / at the end
            else:
                new_path = path + '/'
                self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: " + "http://127.0.0.1:8080" + new_path + "\r\n", 'utf-8'))

        #for other cases, return 404 not found  
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
