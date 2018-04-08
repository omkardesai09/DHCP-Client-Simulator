import subprocess
import sys
import logging
import random

# This will suppress all messages while running or loading scapy

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
logging.getLogger("scapy.interactive").setLevel(logging.ERROR)
logging.getLogger("scapy.loading").setLevel(logging.ERROR)

try:
    from scapy.all import *
except ImportError:
    print "Scapy package is not installed on your system."
    sys.exit()

# Put the interface in promiscous mode
net_iface = raw_input("Enter the interface to the target network: ")
subprocess.call(['ifconfig', net_iface, 'promisc'], stdout=None, stderr=None, shell=False)
print "\n Now interface %s is in promiscous mode\n" %net_iface

# To disable scapy's setting of checking IP addresses

conf.checkIPaddr = False



