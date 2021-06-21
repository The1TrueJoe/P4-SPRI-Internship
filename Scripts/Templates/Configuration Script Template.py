import os

command_path = '/home/admin/mininet/util/m'  # Script to send commands to hosts and routers

hosts = 4 # Number of hosts

def main():
    adjustBuffer(getRange("h", hosts), 10240, 87380, 131072000)
    addDelays("s1", "eth1", "root", "20ms")
    addTBF("s2", "eth2", "root handle 1:", "1gbit", 500000, 26214400)



# Sends command to a host
# device (ex. h1 = host1, r1 = router1)
# command (Command to send)
def sendCommand(device, command, path_required):
    if (isinstance(device, list)):
        sendCommandToMultipleArray(device, command, path_required)
        return

    if (path_required == True):
        command = command_path + " " + device + " \"" + command + "\""
    elif (path_required == False):
        command = command
    else:
        command = "echo no command available"

    print("Sending " + device + " command: " + command)
    os.system(command)

# Sends commands to hosts in a range
# Does not need to be used normally
# type (Format of host/router name ex. h = host, r = router)
# start && end (Range of devices to command)
# command (Command to send)
def sendCommandToMultipleArray(hosts, command, path_required):
    for host in hosts:
        sendCommand(host, command, path_required)

# Creates and array of hosts
# Output ex. getRange('h', 4) -> ['h1', 'h2', 'h3', 'h4']
# name_format (Format that the host names are created ex. h -> h1, h2)
# host_count (Number of hosts)
def getRange(name_format, host_count):
    hosts = []
    for i in range(0, host_count):
        hosts.append(name_format + str(i+1))
    return hosts

# Adjusts the buffer sizes for mtiple hosts
# device_count (Number of devices to command)
# command (Command to send)
def adjustBuffer(hosts, minBuffer, defaultBuffer, maxBuffer):
    sendCommandToMultipleArray(hosts, "sysctl -w net.ipv4.tcp_rmem=\'" + str(minBuffer) + " " + str(defaultBuffer) + " " + str(maxBuffer) + "\'", True)
    sendCommandToMultipleArray(hosts, "sysctl -w net.ipv4.tcp_wmem=\'" + str(minBuffer) + " " + str(defaultBuffer) + " " + str(maxBuffer) + "\'", True)
    
# Uses Transmission Control with Queuing Disciplines
# type (Format of switch name ex. s1 = switch 1)
# port the port to use (ex. eth1) 
# handle (The handle for the discipline)
# discipline (The discipline to apply to the queue)
def addQDiscipline(device, port, handle, discipline):
    sendCommand(device, "sudo tc qdisc add dev " + device + "-" + port + " " + handle + " " + discipline + "", False)

# Adds a delay to a specific interface
# type (Format of switch name ex. s1 = switch 1)
# port the port to use (ex. eth1) 
# handle (The handle for the discipline)
# delay (The latency to add to the port)
def addDelays(device, port, handle, delay):
    addQDiscipline(device, port, handle, "netem delay " + delay)

# Adds a delay to a specific interface
# type (Format of switch name ex. s1 = switch 1)
# port the port to use (ex. eth1) 
# handle (The handle for the discipline)
# loss (The latency to add to the port)
def addLoss(device, port, handle, loss):
    addQDiscipline(device, port, handle, "netem loss " + loss)

# Uses Transmission Control with Queuing Disciplines
# type (Format of switch name ex. s1 = switch 1)
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