# A network scanner, discover hosts on your network and their MAC address
# by Jose Oregon

import scapy.all as scapy 
import optparse

def get_target():

    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Enter a subnet using CIDR notation or IP address to scan")
    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error("Please enter an IP or a subnet in CIDR notation to scan, use --help for options")
    return options
    
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request 
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    client_list = []
    for element in answered_list:
        client_dict = {"ip" : element[1].psrc, "MAC" : element[1].hwsrc} 
        client_list.append(client_dict)
    return (client_list)

def print_results(results_list):
    print("IP\t\t\tMAC Address\n------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["MAC"])

options = get_target()
scan_result = scan(options.target)

if not scan_result:
    print("No results found: Verify you are connected to the target network you are trying to scan!") 
else:
    print_results(scan_result)


