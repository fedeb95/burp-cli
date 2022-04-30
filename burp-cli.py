import argparse
import random
import pyfiglet

import os.path
import re
import time

import socket
import ssl


def make_request(args, request_lines):
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
    request_time = time.perf_counter() - start

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

def main():
    parser = argparse.ArgumentParser(description='burp-cli - Burp Suite functionalities in the terminal')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='Verbose output.')
    parser.add_argument('-r', '--request', dest='request', action='store',
                        help='Path of the file containing a request')
    parser.add_argument('-c', '--payload-positions-char', dest='placeholder', action='store', default='~',
                        help='Character used to identify payload positions in the request')
    parser.add_argument('-p', '--payload', dest='payload', action='store',
                        help='Path of the file containing payloads')
    args = parser.parse_args()

    banner = pyfiglet.Figlet(font=random.choice(pyfiglet.FigletFont.getFonts()))
    print(banner.renderText('burp-cli'))

    request_lines = read_file(args.request)
    payloads = read_file(args.payload)
    placeholder = args.placeholder
    for payload in payloads:
       sub_lines = [re.sub(f'{placeholder}.*{placeholder}', payload, line) for line in request_lines]
       make_request(args, sub_lines)
    
if __name__=='__main__':
    main()
