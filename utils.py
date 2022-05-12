import os.path
import time
import re

import socket
import ssl

def make_request(args, request_text):
    request_lines = request_text.split('\n')
    # second line is like Host: host.com
    host = request_lines[1].split(' ')[1]
    ssock = None
    for line in request_lines:
        res = re.search(r'Origin: (http(s)?)', line)
        if hasattr(res, 'groups') and 's' in res.groups():
            # https matched
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            sock = socket.create_connection((host.strip(),443))  
            ssock = context.wrap_socket(sock, server_hostname=host)
            break
        elif hasattr(res, 'groups') and 'http' in res.groups():
            #http matched
            ssock = socket.create_connection((host.strip(),80))  
            break
    if ssock is None:
        raise RuntimeError("Origin header not found!")

    ssock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    request = '\n'.join(request_lines).encode('utf-8')
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

    ssock.close()

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


