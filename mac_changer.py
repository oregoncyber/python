# Simple script to change your MAC address
# By Jose Oregon
# use  sudo when executing, use --help for options

import subprocess
import optparse
import re

def get_arguments():

    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface you want to change")
    parser.add_option("-m", "--mac", dest="new_mac", help="New mac address" )
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Please enter an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("Please enter a new mac address, use --help for more info") 
    return options

def change_mac(interface, new_mac):
        
    subprocess.call(["ifconfig", interface, "down"]) # ifconfig eth0 down
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac]) # ifconfig eth0 hw ether <mac>
    subprocess.call(["ifconfig", interface, "up"]) # ifconfig eth0 up

def get_current_mac(interface):

    ifconfig_result = subprocess.check_output(["ifconfig", interface]) #check_outputs as bytes causing "type" errors on line 28
    check_mac = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', str(ifconfig_result)) #converting ifconfig result to string due to type errors
    if check_mac.group(0):
        return check_mac.group(0) 
    else:
        print("Could not read MAC address ")   
    
options = get_arguments()
current_mac = get_current_mac(options.interface)
print(f"Current MAC address is = {current_mac}")
print(f"Changing MAC address to = {options.new_mac}")
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface) #verify mac was changed

if current_mac == options.new_mac:
    print(f"MAC address was successfully changed to = {current_mac}")
else:
    print("MAC address was not changed.")
