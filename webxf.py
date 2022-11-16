"""
WebX Framework
Developer: VladosNX (VladosNX on GitHub)
This is beta version - please report all bugs!
"""
import socket
import os
import jinja2

error = '\x1b[41;30mERROR\x1b[0m '
warn = '\x1b[43;30mWARN \x1b[0m '
messg = '\x1b[44;30mMESSG\x1b[0m '
done = '\x1b[42;30mDONE \x1b[0m '

def render(template, data={}):
    if os.path.exists(f'templates/{template}'):
        # f = open(f'templates/{template}')
        # t = f.read()
        # f.close()
        tl = jinja2.Environment(loader=jinja2.PackageLoader("webxf"),
        autoescape=jinja2.select_autoescape()).get_template(f'templates/{template}')
        return tl.render(**data)
    else:
        raise FileNotFoundError()

class WebxfException(Exception): pass

class Response():
    def __init__(self, text):
        self.text = text

class Website():
    def __init__(self):
        self.routes = []
        self.funcs = []
        self.page400 = '<html><body><h1>400 Bad request</h1></body></html>'
        self.page404 = '<html><body><h1>404 Not found</h1></body></html>'
        self.page500 = '<html><body><h1>500 Internal server error</h1></body></html>'
    def addRoute(self, path, func):
        if path[0] != '/': raise WebxfException('Incorrect path')
        self.routes.append(path)
        self.funcs.append(func)
    def listen(self, host='127.0.0.1', port=8080):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(1000)
        print(f'{messg}Listening started')
        while True:
            try:
                client, address = server.accept()
                data = client.recv(1024).decode()
            except KeyboardInterrupt:
                server.shutdown(socket.SHUT_RDWR)
                server.close()
                print('Server stopped')
                exit(0)
            try: rroute = data.split(' ')[1]
            except IndexError:
                client.send('HTTP/1.1 400 BADREQUEST\n\n'.encode() + self.page400.encode())
                try:
                    client.shutdown(socket.SHUT_RDWR)
                    client.close()
                except OSError: pass
                print(f'{address[0]}:{address[1]} [400] {rroute}')
            if rroute in self.routes:
                func = self.funcs[self.routes.index(rroute)]()
                try:
                    client.send('HTTP/1.1 200 OK\n\n'.encode() + func.text.encode())
                    try:
                        client.shutdown(socket.SHUT_RDWR)
                        client.close()
                    except OSError: pass
                    print(f'{address[0]}:{address[1]} [200] {rroute}')
                except Exception as e:
                    client.send('HTTP/1.1 500 INTERNALSERVERERROR\n\n'.encode() + self.page500.encode())
                    try:
                        client.shutdown(socket.SHUT_RDWR)
                        client.close()
                    except OSError: pass
                    print(f'{address[0]}:{address[1]} [500] {rroute}')
                    if type(func) != Response:
                        # print(' ____________________________________[x]')
                        # print('|                                      |')
                        # print('| Internal server error                |')
                        # print('| Function must return webxf.Response  |')
                        # print('|______________________________________|')
                        print(f'{error}Internal server error while processing route {rroute}')
                        print(f'{error}Expected Response, but got {type(func)}')
            elif os.path.exists(f'routeignore/{rroute}'):
                f = open(f'routeignore/{rroute}', 'rb')
                t = f.read()
                f.close()
                client.send('HTTP/1.1 200 OK\n\n'.encode() + t)
                try:
                    client.shutdown(socket.SHUT_RDWR)
                    client.close()
                except OSError: pass
                print(f'{address[0]}:{address[1]} [200 ROUTEIGNORE] {rroute}')
            else:
                client.send('HTTP/1.1 404 NOTFOUND\n\n'.encode() + self.page404.encode())
                try:
                    client.shutdown(socket.SHUT_RDWR)
                    client.close()
                except OSError: pass
                print(f'{address[0]}:{address[1]} [404] {rroute}')