#IOC Parser by Jose Oregon
#Sort an IOC list for Splunk searches
#needs function to defang URL/IPs
#one IOC per line on text file

import optparse

def get_file():
    parser=optparse.OptionParser()
    parser.add_option('-f', '--file', dest='filename', help='Name of file to parse, ensure to use full path')
    (options, arguments)=parser.parse_args()
    if not options.filename:
        parser.error('Please enter the full path of the file to parse, use --help for options')
    return options

def prep_file(z):
    with open(z, 'r') as f:
        lines = f.readlines()
    return lines

options=get_file()
file_ready=prep_file(options.filename)

def sort_file(s):
    sorted_ioc = []
    for line in s:
        sorted_ioc.append(line.replace('\n', ' OR '))
        
        with open('sorted_ioc.txt', 'w') as v:
            v.writelines(sorted_ioc)
    return sorted_ioc
        
sort_file(file_ready)
print('Success, File saved as: sorted_ioc.txt')                 
