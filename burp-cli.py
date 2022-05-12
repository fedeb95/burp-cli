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
    parser.add_argument('-p', '--payloads', dest='payloads', action='store', nargs='+',
                        help='Path of the files containing payloads')
    parser.add_argument('-i', '--intruder', dest='intruder', action='store_true',
                        help='Select Intruder attack type')
    parser.add_argument('-cb', '--cluster-bomb', dest='cluster_bomb', action='store_true',
                        help='Select Cluster Bomb attack type')
    args = parser.parse_args()

    banner = pyfiglet.Figlet(font=random.choice(pyfiglet.FigletFont.getFonts()))
    print(banner.renderText('burp-cli'))

    request_lines = read_file(args.request)
    request_text = '\r\n'.join(request_lines)
    placeholder = args.placeholder
    positions = re.findall(f'{placeholder}[^{placeholder}]*{placeholder}', request_text, re.MULTILINE)

    payload_dict = {}
    for i in range(0, len(args.payloads)):
        payload_dict[i] = read_file(args.payloads[i])

    if args.intruder:
        payload = payload_dict[0]
        # python magic to get all permutations with repetitions of payloads
        parameters = itertools.product(*([payload] * len(positions)))
        for param in parameters:
            substituted = request_text
            for i in range(0, len(positions)):
                substituted = re.sub(positions[i], param[i], substituted, re.MULTILINE)
            make_request(args, substituted)
    elif args.cluster_bomb:
        pass
    else:
        print("Specify an attack type. Supported: --intruder")
    
if __name__=='__main__':
    main()
