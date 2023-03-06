#!/bin/python3

import optparse
import requests 

parser=optparse.OptionParser()
parser.add_option('-w','--wordlist', dest='wordlist', help='Enter full wordlist path')
parser.add_option('-d','--domain', dest='domain', help='Enter the domain to scan')
(options, arguments) = parser.parse_args()
if not options.wordlist:
    parser.error('Please enter a wordlist, use --help for more info')
elif not options.domain:
    parser.error('Please enter a domain or IP, use --help for more info')

dir_list = open(options.wordlist).read() 
dir = dir_list.splitlines()

for d in dir:
    sub_dir = f'http://{options.domain}/{d}.html'
    r = requests.get(sub_dir)
    if r.status_code == 404:
        pass
    else:
        print('Valid Directory:', sub_dir)
        with open('results.txt', 'w') as f:
            f.writelines(sub_dir)
