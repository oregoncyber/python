#!/bin/python3

import requests
import optparse

parser=optparse.OptionParser()
parser.add_option('-w','--wordlist', dest='wordlist', help='Enter full wordlist path')
parser.add_option('-d','--domain', dest='domain', help='Enter the domain to scan')
(options, arguments) = parser.parse_args()
if not options.wordlist:
    parser.error('Please enter a wordlist, use --help for more info')
elif not options.domain:
    parser.error('Please enter a domain or IP, use --help for more info')

domain_list=open(options.wordlist).read()
sub_domains=domain_list.splitlines()

for i in sub_domains:
    subdoms=f'http://{i}.{options.domain}'

    try:
        requests.get(subdoms)

    except requests.ConnectionError:
        pass

    else:
        print('Valid Domain:', subdoms)
        with open('sub_results.txt', 'w') as f:
            f.writelines(subdoms)
