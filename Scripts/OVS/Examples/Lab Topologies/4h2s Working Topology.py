from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

#
#       Topology:
#
#   h1          h3
#     \        /
#      s1 - s2
#     /        \
#   h2          h4
#


def myNetwork():
    
    # Setup mininet
    net = Mininet(topo = None, build = False, ipBase = '10.0.0.0/8')
    
    info("*** Creating Controllers ***\n")
    
    info("*** Creating Switches ***\n")
    s1 = net.addSwitch('s1', cls = OVSKernelSwitch, failMode = 'standalone')
    s2 = net.addSwitch('s2', cls = OVSKernelSwitch, failMode = 'standalone')
    
    info("*** Creating Hosts ***\n")
    h1 = net.addHost('h1', cls = Host, ip = '10.0.0.1', defaultRoute = None)
    h2 = net.addHost('h2', cls = Host, ip = '10.0.0.2', defaultRoute = None)
    h3 = net.addHost('h3', cls = Host, ip = '10.0.0.3', defaultRoute = None)
    h4 = net.addHost('h4', cls = Host, ip = '10.0.0.4', defaultRoute = None)
    
    info("*** Creating Links ***\n")
    # Switch to Switch Links
    net.addLink(s1, s2)
    
    # Switch to Host Links
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(s2, h3)
    net.addLink(s2, h4)
    
    info("Starting Network....\n")
    net.build()
    
    info("Starting Controllers....\n")
    for controller in net.controllers:
        controller.start()
    
    info("Starting Switches....\n")
    net.get('s1').start([])
    net.get('s2').start([])
    
    info("Beginning Configuration\n")

    CLI(net)
    net.stop()
    
if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()