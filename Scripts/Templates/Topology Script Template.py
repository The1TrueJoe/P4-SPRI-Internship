from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
 
# Setup mininet
net = Mininet(topo = None, build = False, ipBase = '10.0.0.0/8')

# Sets up mininet
def myNetwork():
    
    info("*** Controllers ***\n")
    
    info("*** Switches ***\n")
    s = createSwitches('s', 2)
    
    info("*** Hosts ***\n")
    h = createHosts('h', 4, '10.0.0.')

    info("*** Links ***\n")
    createLink(s[0], s[1])
    createLink(getRange('h', 4), [s[0], s[0], s[1], s[1]])
    
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
def createHostsArg(host_name_format, host_count, ip_base, default_route):
    hosts = []

    print("\tCreating " + str(host_count) + " hosts(s)")
    for i in range(0, host_count):
        print("\tCreating Host " + host_name_format + str(i+1) + " with ip " + ip_base + str(i+1))
        hosts.append(net.addHost(host_name_format + str(i+1), cls = Host, ip = ip_base + str(i+1), defaultRoute = default_route))

    return hosts

# Creates a host namespace
# Uses default route settings
# host_name_format (The format of the host name. ex h -> h1, h2)
# host_count (The number of hosts to create)
# ip_base (Format of the ip address. ex 10.0.0. -> 10.0.0.1, 10.0.0.2)
def createHosts(host_name_format, host_count, ip_base):
    return createHostsArg(host_name_format, host_count, ip_base, None)

# Creates a switch namespace
# switch_name_format (The format of the switch name. ex h -> h1, h2, etc)
# switch_count (The number of switches to create)
# cls (Type of switch to create) Default: OVSKernelSwitch
# fail_mode (Fail mode of the switch) Default: 'standalone'
def createSwitchesArg(switch_name_format, switch_count, cls, fail_mode):
    switches = []

    print("\tCreating " + str(switch_count) + " switch(es)")
    for i in range(0, switch_count):
        print("\tCreating switch " + switch_name_format + str(i+1))
        switches.append(net.addSwitch(switch_name_format + str(i+1), cls = cls, failMode = fail_mode))

    return switches


# Creates a switch namespace
# Uses default OVSKernel and standalone fail
# switch_name_format (The format of the switch name. ex h -> h1, h2, etc)
# switch_count (The number of switches to create)
def createSwitches(switch_name_format, switch_count):
    return createSwitchesArg(switch_name_format, switch_count, OVSKernelSwitch, 'standalone')

# Creates and array of hosts
# Output ex. getRange('h', 4) -> ['h1', 'h2', 'h3', 'h4']
# name_format (Format that the host names are created ex. h -> h1, h2)
# host_count (Number of hosts)
def getRange(name_format, host_count):
    hosts = []
    for i in range(0, host_count):
        hosts.append(name_format + str(i+1))
    return hosts

# Creates a network link between two namespaces
# Supports individual objects or arrays
# side1 & side2 (The objects associated with the link)
def createLink(side1, side2):
    # Checks to see if multiple links need to be created
    if (isinstance(side1, list) == False and isinstance(side2, list) == False):
        print("\tCreating 1 link")
        net.addLink(side1, side2)
        print("\tDone.")
        return
    elif (isinstance(side1, list) == False or isinstance(side2, list) == False):
        print("\tArguments are not the same type")
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
        print("\tFound unequal array length")
    elif (s1len < s2len):
        length = s1len
        print("\tFound unequal array length")

    print("\tCreating " + str(length) + " links")
    for i in range(0, length):
        net.addLink(side1[i], side2[i])

    print("\tDone.")

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()