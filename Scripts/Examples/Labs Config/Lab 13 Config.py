import subprocess
import os

command_path = '/home/admin/mininet/util/m'  # Script to send commands to hosts and routers

hosts = 4 # Number of hosts

def main():
    adjustAllBuffers("h", hosts, 10240, 87380, 131072000)
    addLoss("s1", "eth2", "root handle 1:", "1%")
    addTBF("s1", "eth2", "parent 1: handle 2:", "10gbit", 5000000, 15000000)
    
    for i in range(1, 3):
        for x in range(1, 3):
            adjustMTU("s" + str(i), "eth" + str(x), 9000)



# Sends command to a host
# device (ex. h1 = host1, r1 = router1)
# command (Command to send)
def sendCommand(device, command, path_required):
    if (path_required == True):
        command = command_path + " " + device + " \"" + command + "\""
    elif (path_required == False):
        command = command
    else:
        command = "echo no command available"

    print("Sending " + device + " command: " + command)
    os.system(command)

# Sends commands to multiple hosts
# type (Format of host/router name ex. h = host, r = router)
# device_count (Number of devices to command)
# command (Command to send)
def sendCommandToMultiple(type, device_count, command, path_required):
    for i in range (0, device_count):
        sendCommand(type + str(i+1), command, path_required)

# Sends commands to hosts in a range
# type (Format of host/router name ex. h = host, r = router)
# start && end (Range of devices to command)
# command (Command to send)
def sendCommandToMultipleRange(type, start, end, command, path_required):
    for i in range (start, end):
        sendCommand(type + str(i+1), command, path_required)

# Adjusts the buffer sizes for mtiple hosts
# device_count (Number of devices to command)
# command (Command to send)
def adjustAllBuffers(type, device_count, minBuffer, defaultBuffer, maxBuffer):
    sendCommandToMultiple(type, device_count, "sysctl -w net.ipv4.tcp_rmem=\'" + str(minBuffer) + " " + str(defaultBuffer) + " " + str(maxBuffer) + "\'", True)
    sendCommandToMultiple(type, device_count, "sysctl -w net.ipv4.tcp_wmem=\'" + str(minBuffer) + " " + str(defaultBuffer) + " " + str(maxBuffer) + "\'", True)

# Opens IPerf3 as a server on multiple hosts
# device (Format of host name ex. h1 = host 1)
# device_count (Number of devices to command)
def runIPerf3Server(type, start, end):
    sendCommandToMultipleRange(type, start, end, 'iperf3 -s', True)
    
# Uses Transmission Control with Queuing Disciplines
# device (Format of switch name ex. s1 = switch 1)
# port the port to use (ex. eth1) 
# handle (The handle for the discipline)
# discipline (The discipline to apply to the queue)
def addQDiscipline(device, port, handle, discipline):
    sendCommand(device, "sudo tc qdisc add dev " + device + "-" + port + " " + handle + " " + discipline + "", False)

# Adds a delay to a specific interface
# device (Format of switch name ex. s1 = switch 1)
# port the port to use (ex. eth1) 
# handle (The handle for the discipline)
# delay (The latency to add to the port)
def addDelays(device, port, handle, delay):
    addQDiscipline(device, port, handle, "netem delay " + delay)

# Adds a delay to a specific interface
# device (Format of switch name ex. s1 = switch 1)
# port the port to use (ex. eth1) 
# handle (The handle for the discipline)
# loss (The latency to add to the port)
def addLoss(device, port, handle, loss):
    addQDiscipline(device, port, handle, "netem loss " + loss)

# Uses Transmission Control with Queuing Disciplines
# device (Format of switch name ex. s1 = switch 1)
# port the port to use (ex. eth1) 
# handle (The handle for the discipline)
# rate (The rate that the port is limited to)
# burst (Burst size in bytes)
# limit (Limit in bytes)
def addTBF(device, port, handle, rate, burst, limit):
    addQDiscipline(device, port, handle, "tbf rate " + rate + " burst " + str(burst) + " limit " + str(limit))

# Uses ifconfig to adjust the MTU at a port
# device (Format of switch name ex. s1 = switch 1)
# port the port to use (ex. eth1) 
# MTU (The new MTU)
def adjustMTU(device, port, mtu):
    sendCommand(device, "ifconfig " + device + "-" + port + " mtu " + str(mtu), True)

main()