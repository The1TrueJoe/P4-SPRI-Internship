from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

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
    
if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()