import os

command_path = 'mininet/util/m'  # Script to send commands to hosts and routers

controllers = 0 # Number of controllers
hosts       = 4 # Number of hosts
switches    = 0 # Number of Switches
routers     = 0 # Number of routers

# Device (ex. h1 = host1, r1 = router1)
# Command (Command to send)
def sendCommand(device, command):
    print("Sending " + device + " command: '" + command + "'")
    os.system(command_path + " " + device + " " + command)

# Type (Format of host/switch name ex. h = host, r = router)
# device_count (Number of devices to command)
# Command (Command to send)
def sendCommandToMultiple(type, device_count, command):
    for i in range (0, device_count):
        sendCommand(type + str(i+1), command)

# Type (Format of host name ex. h1 = Host 1)
# device_count (Number of devices to command)
# Command (Command to send)
def adjustAllBuffers(type, device_count, minBuffer, defaultBuffer, maxBuffer):
    sendCommandToMultiple(type, device_count, "sysctl -w net.ipv4.tcp_rmem='" + minBuffer + " " + defaultBuffer + " " + maxBuffer + "'")