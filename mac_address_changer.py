#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", dest="mac_address", help="New MAC address")
    (options, arguements) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an Interface , type --help for more info")
    elif not options.mac_address:
        parser.error("[-] Please enter new MAC address , type --help for more info")
    return options


def mac_changer(interface, new_mac_address):
    print("[+] Changing the mac address of " + interface + " to new " + new_mac_address)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac_address])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifcnf_result = subprocess.check_output(["ifconfig", interface])

    mac_changer_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifcnf_result)

    if mac_changer_result:
        return mac_changer_result.group(0)
    else:
        print("[-] Could not read MAC address")


options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current mac = " + str(current_mac))


mac_changer(options.interface, options.mac_address)

current_mac = get_current_mac(options.interface)

if current_mac == options.mac_address:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[+] Sorry! MAC address did not get changed")

