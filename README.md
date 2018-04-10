
# DHCP client simulator

The main objective of this project is to simulate DHCP client scenarios and get IP addresses for virtual hosts from DHCP server.

User input will be accepted for simulation of one or more virtual clients and check DHCP bindings on DHCP server and local file created after running python script.

### Prerequisites

Build the topology as shown in screenshot.png in GSN3 to check output. Virtualbox VM (Debian 7) is used as a host in GNS topology.

### Initial Configurations on router(R1)

Refer Initial_config.txt file and do similar steps on router to act it like a DHCP server.

### Final Steps

Run dhcp_cli_sim.py script on host (Debian 7 VM).

### Features

1. User can enter number of clients he/she would like to simulate. DHCP bindings (IP address assigned to client, MAC address of client, Server IP) will be stored in 'ip_lease.txt' file.

2. User can release DHCP bindings for single or multiple IP addresses.
 