import socket

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

def create_table(costs, routerids, outputs):
    
    routing_table = []
    for i in range(0, len(costs)):
        routing_table.append([costs[i], outputs[i], routerids[i], routerids[i]]) # Create an entry for each output that was listed, of the form cost, outgoing interface, next-hop router, destination router id
    print(routing_table)
    return routing_table
            
def send_update(routing_table, neighbours, out_socket):
    for router_ports in neighbours:
        out_socket.connect(('127.0.0.1', router_port))
        out_socket.send(
            
class RIP_Packet:
    
                