#!/bin/python3
import socket
import os
from signal import signal, SIGPIPE, SIG_DFL
try: from termcolor import colored
except ModuleNotFoundError:
    os.system('pip install termcolor')
    from termcolor import colored
try: import yaml
except ModuleNotFoundError:
    os.system('pip install yaml')
    import yaml
import sys
import random

headers = 'HTTP/1.1 200 OK\n\n'.encode('utf-8')

class Errors():
    E404 = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>404 Not found</title>
</head>
<body>
<h1>404 Not found<h1/></body>
</html>""".encode('utf-8')
errors = Errors()
class Messages():
    DONE = colored(text='DONE', on_color='on_green') + ' '
    ERROR = colored(text='ERROR', on_color='on_red') + ' '
    WARN = colored(text='WARN', on_color='on_yellow') + ' '
    MESSG = colored(text='MESSG', on_color='on_blue') + ' '
    REQST = colored(text='REQST', on_color='on_cyan') + ' '
messages = Messages()

if len(sys.argv) < 2:
    print("Printing help for WebX")
    print("-s [config]  Start server")
elif sys.argv[1] == '-s':
    if len(sys.argv) != 3:
        print("Usage: webx -s [config]")
        exit(1)
    if os.path.exists('/etc/webx/configs/' + sys.argv[2] + '.yml') == False:
        print(messages.ERROR + "Config not found")
        exit(1)
    config = open('/etc/webx/configs/' + sys.argv[2] + '.yml')
    conf = yaml.safe_load(config)
    config.close()
    host = conf['host']
    port = conf['port']
    mainfile = conf['mainfile']
    workdir = conf['workdir']
    max_requests = conf['max_requests']

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try: server.bind((host, port))
    except OSError:
        print(messages.ERROR + "Can't listen port " + str(port))
        exit(1)
    server.listen(max_requests)
    print(messages.DONE + 'Listening at ' + host + ':' + str(port))
    while True:
        try:
            client_socket, address = server.accept()
            data = client_socket.recv(1024).decode('utf-8')
        except KeyboardInterrupt:
            print(messages.WARN + 'Closing server')
            server.shutdown(socket.SHUT_RDWR)
            server.close()
            exit()
        try: requested_file = workdir + data.split(' ')[1]
        except: continue
        if requested_file == workdir + '/':
            requested_file = workdir + '/' + mainfile
        if os.path.exists(requested_file) == False:
            print(messages.REQST + '[GET/404] ' + requested_file)
            signal(SIGPIPE, SIG_DFL)
            client_socket.send(headers + errors.E404)
            client_socket.shutdown(socket.SHUT_WR)
        else:
            if len(requested_file.split('.')) > 1 and requested_file.split('.')[1] == 'py':
                rid = random.randint(0, 99999)
                os.system('python3 ' + requested_file + ' > /tmp/webx-out' + str(rid))
                outputFile = open('/tmp/webx-out' + str(rid))
                output = outputFile.read()
                outputFile.close()
                print(messages.REQST + '[GET/200] ' + requested_file)
                signal(SIGPIPE, SIG_DFL)
                client_socket.send(headers + output.encode('utf-8'))
                client_socket.shutdown(socket.SHUT_WR)
            elif len(requested_file.split('.')) > 1 and requested_file.split('.')[1] == 'php':
                rid = random.randint(0, 99999)
                os.system('php ' + requested_file + ' > /tmp/webx-out' + str(rid))
                outputFile = open('/tmp/webx-out' + str(rid))
                output = outputFile.read()
                outputFile.close()
                print(messages.REQST + '[GET/200] ' + requested_file)
                signal(SIGPIPE, SIG_DFL)
                client_socket.send(headers + output.encode('utf-8'))
                client_socket.shutdown(socket.SHUT_WR)
            else:
                file = open(requested_file)
                response = file.read()
                file.close()
                signal(SIGPIPE,SIG_DFL)
                client_socket.send(headers + response.encode('utf-8'))
                print(messages.REQST + '[GET/200] ' + requested_file)
                client_socket.shutdown(socket.SHUT_WR)