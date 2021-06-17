from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
 
net = "n"

# Sets up mininet
def myNetwork():
    
    # Setup mininet
    net = Mininet(topo = None, build = False, ipBase = '10.0.0.0/8')
    
    info("*** Controllers ***\n")
    
    info("*** Switches ***\n")
    
    info("*** Hosts ***\n")
    
    info("*** Links ***\n")
    
    info("Starting Network....\n")
    net.build()
    
    info("Starting Controllers....\n")
    for controller in net.controllers:
        controller.start()
    
    info("Starting Switches....\n")
    
    info("Configuring\n")
    
    CLI(net)
    net.stop()

# Creates a host namespace
# host_name_format (The format of the host name. ex h -> h1, h2)
# host_count (The number of hosts to create)
# ip_base (Format of the ip address. ex 10.0.0. -> 10.0.0.1, 10.0.0.2)
# default_route Default: None
def createHosts(host_name_format, host_count, ip_base, default_route):
    hosts = []

    print("Creating " + host_count + " hosts(s)")
    for i in range(0, host_count):
        print("Creating Host " + host_name_format + str(i+1) + " with ip " + ip_base + str(i))
        hosts.append(net.addHost(host_name_format + str(i+1), cls = Host, ip = ip_base + str(i), defaultRoute = default_route))

    return hosts

# Creates a host namespace
# Uses default route settings
# host_name_format (The format of the host name. ex h -> h1, h2)
# host_count (The number of hosts to create)
# ip_base (Format of the ip address. ex 10.0.0. -> 10.0.0.1, 10.0.0.2)
def createHosts(host_name_format, host_count, ip_base):
    return createHosts(host_name_format, host_count, ip_base, None)

# Creates a switch namespace
# switch_name_format (The format of the switch name. ex h -> h1, h2, etc)
# switch_count (The number of switches to create)
# cls (Type of switch to create) Default: OVSKernelSwitch
# fail_mode (Fail mode of the switch) Default: 'standalone'
def createSwitches(switch_name_format, switch_count, cls, fail_mode):
    switches = []

    print("Creating " + switch_count + " switch(es)")
    for i in range(0, switch_count):
        print("Creating switch " + switch_name_format + str(i+1))
        switches.append(net.addSwitch(switch_name_format + str(i+1), cls = cls, failMode = fail_mode))

    return switches


# Creates a switch namespace
# Uses default OVSKernel and standalone fail
# switch_name_format (The format of the switch name. ex h -> h1, h2, etc)
# switch_count (The number of switches to create)
def createSwitches(switch_name_format, switch_count):
    return createSwitches(switch_name_format, switch_count, OVSKernelSwitch, 'standalone')

# Creates a network link between two namespaces
# Supports individual objects or arrays
# side1 & side2 (The objects associated with the link)
def createLink(side1, side2):
    # Checks to see if multiple links need to be created
    if (isinstance(side1, list) == False and isinstance(side2, list) == False):
        print("Creating 1 link")
        net.addLink(side1, side2)
        return
    elif (isinstance(side1, list) == False or isinstance(side2, list) == False):
        print("Arguments are not the same type")
        return

    # Get array lengths
    length = 0;
    s1len = len(side1)
    s2len = len(side2)

    # Checks to see if lengths are equal. If not, the smallest length is used
    if (s1len == s2len):
        length = s1len
    elif (s1len > s2len):
        length = s2len
        print("Found unequal array length")
    elif (s1len < s2len):
        length = s1len
        print("Found unequal array length")

    print("Creating " + length + " links")
    for i in range(0, length):
        net.addLink(side1[i], side2[i])

    print("Done.")

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()