import socket

def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]

p = socket.gethostname()
ip = socket.gethostbyname(p)
    
toconnect = input("Would you like the program accessible to the network?[y/n]")

try:
    
    if toconnect == 'Y' or toconnect == 'y':
        #enterip = input("Enter IP: 192.168.")
        myipaddress = getNetworkIp()
        
        GET_IP_CMD ="chromium-browser --app-id=jogiikclklfklnnkmebpbhdcjdcgdccc"
    
        print(myipaddress)
        print(GET_IP_CMD)
    
    elif toconnect == 'N' or toconnect == 'n':
        
        myipaddress = ip
        
        GET_IP_CMD ="chromium-browser --app-id=cgihijhammjeaifnfgbngjlddhinmohf"
        
        print(myipaddress)
        print(GET_IP_CMD)

except:
    
    print("YOU ARE NOT CONNECTED TO THE NETWORK")