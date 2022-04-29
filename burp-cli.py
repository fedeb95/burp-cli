import argparse
import os.path
import requests
import re

def make_request(args, request_lines):
    # first line is like POST /resource 
    method = request_lines[0].split(' ')[0]
    resource = request_lines[0].split(' ')[1]
    # second line is like Host: host.com
    host = request_lines[1].split(' ')[1]
    url = f'https://{host}{resource}'

    headers = {}
    body_list = []
    end_header = False
    for line in request_lines[1:]:
        # stop at new line between headers and body
        if line == '' or line == '\n':
            end_header = True
        if end_header:
            body_list.append(line)
        else:
            split = line.split(':')
            headers[split[0].strip()] = split[1].strip()

    request_txt = '\n'.join(body_list)
    if method == 'POST':
        res = requests.post(url, data=request_txt, headers=headers)
        print('=== REQUEST START ===')
        print(f'Called {res.request.url}')
        print(f'Body {res.request.body}')
        print(f'Headers {res.request.headers}')
        print('=== REQUEST END ===')
        print('=== RESPONSE START ===')
        print(res.headers)
        print('=== RESPONSE END ===')
    else:
        print('Method not yet implemented!')

def read_file(filename):
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
    parser.add_argument('-c', '--placeholder-char', dest='placeholder', action='store', default='~',
                        help='Character used to identify positions in the request')
    parser.add_argument('-p', '--payload', dest='payload', action='store',
                        help='Path of the file containing payloads')
    args = parser.parse_args()

    request_lines = read_file(args.request)
    payloads = read_file(args.payload)
    placeholder = args.placeholder
    for payload in payloads:
       sub_lines = [re.sub(f'{placeholder}.*{placeholder}', payload, line) for line in request_lines]
       make_request(args, sub_lines)
    
if __name__=='__main__':
    main()
