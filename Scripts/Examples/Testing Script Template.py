import os

command_path = '/home/admin/mininet/util/m'  # Script to send commands to hosts and routers

def main():
    print("Beginning Tests")
    runIPerf3Server(["h3", "h4"])
    runIPerf3ClientArg(["h1"], "10.0.0.3", "-J > h1.json")
    runIPerf3ClientArg(["h2"], "10.0.0.4", "-J > h2.json")
    reboot()

## Commands

# Sends command to a host
# device (ex. h1 = host1, r1 = router1)
# command (Command to send)
def sendCommand(device, command, path_required, run_as_background):
    if (run_as_background == True):
        command = command + " &"
    
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
def sendCommandToMultiple(type, device_count, command, path_required, run_as_background):
    for i in range (0, device_count):
        sendCommand(type + str(i+1), command, path_required, run_as_background)

# Sends commands to hosts in a range
# type (Format of host/router name ex. h = host, r = router)
# start && end (Range of devices to command)
# command (Command to send)
def sendCommandToMultipleArray(hosts, command, path_required, run_as_background):
    for host in hosts:
        sendCommand(host, command, path_required, run_as_background)

## IPerf testing

# Opens IPerf3 as a server in the background
# hosts (Array of different host names)
# agruments (Arguments to pass through)
def runIPerf3ServerArg(hosts, arguments):
    sendCommandToMultipleArray(hosts, 'iperf3 -s ' + arguments + " -1", True, True)
    
# Opens IPerf3 as a server in the background
# hosts (Array of different host names)
# no arguments
def runIPerf3Server(hosts):
    runIPerf3ServerArg(hosts, "")

# Opens IPerf3 as a server in the background
# hosts (Array of different host names)
# agruments (Arguments to pass through)
def runIPerf3ClientArg(hosts, server, arguments):
    sendCommandToMultipleArray(hosts, 'iperf3 -c ' + server + " " + arguments, True, True)
    
# Opens IPerf3 as a server in the background
# hosts (Array of different host names)
# no arguments
def runIPerf3Client(hosts, server):
    runIPerf3ClientArg(hosts, server, "")

## Pinging

# Pings a host
# hosts_to (Array of different host names)
# ip_to (IP address to ping)
# agruments (Arguments to pass through)
def pingArg(hosts_from, ip_to, arguments):
    sendCommandToMultipleArray(hosts_from, "ping " + ip_to + " " + arguments, True, True)

# Pings a host
# hosts_to (Array of different host names)
# ip_to (IP address to ping)
# agruments (Arguments to pass through)
def ping(hosts_from, ip_to):
    pingArg(hosts_from, ip_to, "")


def reboot(hosts):
    sendCommandToMultipleArray(hosts, "reboot", True, True)

main()