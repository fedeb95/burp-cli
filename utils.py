import os.path
import time

import socket
import ssl

def make_request(args, request_text):
    print(request_text)
    request_lines = request_text.split('\n')
    # second line is like Host: host.com
    host = request_lines[1].split(' ')[1]

    context = ssl.create_default_context()
    sock = socket.create_connection((host.strip(),443))  
    ssock = context.wrap_socket(sock, server_hostname=host)

    request = '\r\n'.join(request_lines).encode('utf-8') + b'\r\n'
    ssock.sendall(request)  
     
    start = time.perf_counter()
    response = b''
    while True:
        data = ssock.recv(2048)
        if ( len(data) < 1 ) :
            break
        response += data
    request_time = time.perf_counter()
    request_time = '{0:.4g}'.format(request_time-start)

    if args.verbose:
        print('=== REQUEST START ===')
        print(request)
        print('=== REQUEST END ===')
        print('=== RESPONSE START ===')
        print(response)
        print('=== RESPONSE END ===')

    status = re.search(r'HTTP\/[0-9](.[0-9])? ([0-9]{3})', str(response))
    status = status.group(2)
    size = len(response)
    print(f'Status: {status} | Time: {request_time} | Size: {size}')

def read_file(filename):
    lines = []
    if not os.path.isfile(filename):
        print(f'File {filename} not found')
    else:
        with open(filename) as f:
            lines = f.read().splitlines()
    return lines


