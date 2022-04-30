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
```

## Example
To make a simple attack, run
```
python burp-cli.py -r ./request.txt -p ./payloads.txt
```
If you get
```
 __                                              ___           
/\ \                                            /\_ \    __    
\ \ \____  __  __  _ __   _____              ___\//\ \  /\_\   
 \ \ '__`\/\ \/\ \/\`'__\/\ '__`\  _______  /'___\\ \ \ \/\ \  
  \ \ \L\ \ \ \_\ \ \ \/ \ \ \L\ \/\______\/\ \__/ \_\ \_\ \ \ 
   \ \_,__/\ \____/\ \_\  \ \ ,__/\/______/\ \____\/\____\\ \_\
    \/___/  \/___/  \/_/   \ \ \/           \/____/\/____/ \/_/
                            \ \_\                              
                             \/_/                              

Status: 200 | Time: 0.063 | Size: 4901
Status: 200 | Time: 0.0513 | Size: 4607
Status: 200 | Time: 0.0512 | Size: 4607
```
Yay! The attack was successful. Response status code, response time and length in bytes is displayed.

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
                        Character used to identify payload positions in
                        the request. Defaults to '~'
  -p PAYLOAD, --payload PAYLOAD
                        Path of the file containing payloads
```

## Features
As of now it only implements *Intruder* with the *Sniper* attack type. You can specify as many positions as
you want, however just one file for payloads is supported, so in the same request
each payload position will have the same payload.

## Problems
Currently burp-cli only supports HTTP 1.0 for request, due to using sockets directly.

## TODO
A lot.
