# burp-cli
Burp Suite functionalities in the terminal

## Goal
Implement most functionalities of Burp Suite for CLI usage

## Why
When going through [Portswigger's Academy](https://portswigger.net/web-security),
some workshops require sending a lot of requests, and this can be pretty slow with
the free version of Burp Suite. 

This little project can't really compete with the ease of use of Burp Suite, even
with the free version, so its aim is not to become a substitute of Burp. It could rather be
its companion.

## Install
- clone this repo
- run 
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python burp-cli.py -r ./request.txt -p ./payloads.txt
```
## Usage
```
usage: burp-cli.py [-h] [-v] [-r REQUEST] [-c PLACEHOLDER] [-p PAYLOAD]

burp-cli - Burp Suite functionalities in the terminal

options:
  -h, --help            show this help message and exit
  -v, --verbose         Verbose output.
  -r REQUEST, --request REQUEST
                        Path of the file containing a request
  -c PLACEHOLDER, --payload-positions-char PLACEHOLDER
                        Character used to identify payload positions in the request
  -p PAYLOAD, --payload PAYLOAD
                        Path of the file containing payloads
```

## Features
As of now it only implements *Intruder* with the *Sniper* attack type. You can specify as many positions as
you want, however just one file for payloads is supported, so in the same request
each payload position will have the same payload.

## TODO
A lot.
