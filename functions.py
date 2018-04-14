def parse_ports(ports):
    for i in range(0, len(ports)):
        if ports[i] < 1024 or ports[i] > 64000:
            raise ValueError('Port not in specified range')
        for j in range(0, len(ports)):
            if i == j:
                pass
            else:
                if ports[i] == ports[j]:
                    raise ValueError('There are duplicate port numbers')
        
                
def convertPortsToInts(ports):
    new_ports = []
    
    for port in ports:
        print(port)
        new_ports.append(int(port))
    return new_ports