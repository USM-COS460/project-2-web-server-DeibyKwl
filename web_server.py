import socket
import sys
from threading import Thread
import os
from datetime import datetime

def create_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('Socket creation failed.')
    return s

def header_format(status_code, file_type, file_length):
    cur_time = datetime.now()
    cur_time = cur_time.strftime('%a, %d %b %Y %H:%M:%S GMT')

    status_message = ''
    if status_code == 200:
        status_message = 'OK'
    elif status_code == 404:
        status_message = 'Not Found'

    header = [
        f'HTTP/1.1 {status_code} {status_message}\r\n'.encode(),
        f'Date: {cur_time}\r\n'.encode(),
        f'Server: DeibysServer2.0\r\n'.encode(),
        f'Content-Type: {file_type}\r\n'.encode(),
        f'Content-Length: {file_length}\r\n'.encode(),
        '\r\n'.encode()
    ]
    return header

# Function to assign the type of a file for header
def check_type(file_name):
    if file_name.endswith('.html'):
        return 'text/html'
    elif file_name.endswith('.css'):
        return 'text/css'
    elif file_name.endswith('.jpeg'):
        return 'image/jpeg'
    

def server_process(sock, folder_path):

    # # Forced the \r\n\r\n when doing GET
    request = b''
    while b'\r\n\r\n' not in request:
        # Make sure user do \r\n\r\n, basically pressing Enter twice after GET request
        request += sock.recv(1024)

        # If user press Enter as first argument, then close everything
        if request.startswith(b'\r\n'):
            sock.close()
            return
        
        # Force user to enter GET (No other methods allowed)
        if not request.startswith(b'GET'):
            sock.close()
            return

    request = request.decode('utf-8')
    lines = request.splitlines()
    request = lines[0] # Get the method type
    parts = request.split()
    
    path = parts[1] # Get the path of file needed

    # Forced the path to index.html if nothing is given
    if path == '/':
        path = '/index.html'

    file_path = os.path.join(folder_path, path.lstrip('/'))

    if os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
            file_content = f.read()

        file_type = check_type(file_path)

        header = header_format(200, file_type, len(file_content))
        # print(b''.join(header))
        sock.send(b''.join(header) + file_content)
    
    else:
        # Reused html tags from what I got from testing with original http.server
        file_content = """<!DOCTYPE HTML>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: 404</p>
        <p>Message: File not found.</p>
        <p>Error code explanation: 404 - Nothing matches the given URI.</p>
    </body>
</html>
        """.encode()
        header = header_format(404, 'text/html', len(file_content))
        sock.send(b''.join(header) + file_content)
    sock.close()
        
def main(port, dir):
    # Forced path to include current path where python file is located
    folder_path = os.path.abspath(os.getcwd()) + '/' + dir

    socket = create_socket()
    socket.bind(('localhost', port))
    socket.listen()

    while True:
        element_socket, addr = socket.accept()
        element_thread = Thread(target=server_process, args=(element_socket, folder_path))
        element_thread.start()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        try:
            main(port=int(sys.argv[1]), dir=sys.argv[2])
        except:
            print('\nThere was an error. Connection closed.')
    else:
        print('Wrong args')

    