#Sort IOC text file and prepare for Splunk search

with open('ioc.txt', 'r') as f:
    lines = f.readlines()

sorted_ioc = []
for line in lines:
    sorted_ioc.append(line.replace('\n', ' OR '))

with open('sorted_ioc.txt', 'w') as x:
    x.writelines(sorted_ioc)

print(sorted_ioc)                      
