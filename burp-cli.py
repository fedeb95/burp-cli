import argparse
import random
import pyfiglet

import re
import itertools

from utils import read_file, make_request


def main():
    parser = argparse.ArgumentParser(description='burp-cli - Burp Suite functionalities in the terminal')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='Verbose output.')
    parser.add_argument('-r', '--request', dest='request', action='store',
                        help='Path of the file containing a request')
    parser.add_argument('-c', '--payload-positions-char', dest='placeholder', action='store', default='~',
                        help="Character used to identify payload positions in the request. Defaults to '~'")
    parser.add_argument('-p', '--payload', dest='payload', action='store',
                        help='Path of the file containing payloads')
    args = parser.parse_args()

    banner = pyfiglet.Figlet(font=random.choice(pyfiglet.FigletFont.getFonts()))
    print(banner.renderText('burp-cli'))

    request_lines = read_file(args.request)
    request_text = '\r\n'.join(request_lines)
    payloads = read_file(args.payload)
    placeholder = args.placeholder
    positions = re.findall(f'{placeholder}[^~]*{placeholder}', request_text, re.MULTILINE)

    # python magic to get all permutations with repetitions of payloads
    parameters = itertools.product(*([payloads] * len(positions)))
    for param in parameters:
        substituted = request_text
        for i in range(0, len(positions)):
            substituted = re.sub(positions[i], param[i], substituted, re.MULTILINE)
        make_request(args, substituted)
    
if __name__=='__main__':
    main()
