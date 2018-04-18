import socket
INFINITY = 16

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
        entry = Route_Entry(costs[i], outputs[i], routerids[i], routerids[i], 0, 0, False) #Create an object of class Route_Entry
        routing_table.append(entry) #Add this Route_Entry object to the routing_table
    print(routing_table)
    return routing_table
            
def send_update(routing_table, neighbours, out_socket):
    for router_port in neighbours:
        out_socket.connect(('127.0.0.1', router_port))
        out_socket.send(routing_table)
        
def process_update(routing_table, update_table):
    if rip_message.source_router not in neighbours:
        pass
    else:
        for entry in routing_table:
            if entry.destination == rip_message.source_router:
                src_router_entry = entry
        for rte in rip_message.rtes:
            if rte.metric >= INFINITY or rte.metric < 1:
                pass
            else:
                this_metric = min(rte.metric + src_router_entry[0], INFINITY)
                existing_route = False
                for entry in routing_table:
                    if entry.destination == rte.destination_id:
                        existing_route = True
                        existing_entry = entry
                if existing_route:      
                    if existing_entry[2] == rip_message.source_router:
                        existing_entry[5] = 0 #Reset timeout to 0
                        if existing_entry[0] != this_metric:
                            existing_entry[0] = this_metric
                            existing_entry[
                            existing_entry[6] = True #Set change flag
                            
                            
                else:
                    if this_metric < INFINITY:
                        new_entry = Route_Entry(this_metric, src_router_entry[1], rip_message.source_router, rte.destination_id, 0, 0, True)
                        routing_table.append(new_entry)
                        
                        
                        
                
def triggered_update(            
                              
class Route_Entry:
    
    def __init__(self, cost, interface, next_hop, destination, timeout, garbage_timer, change_flag):
        self.cost = cost
        self.interface = interface
        self.next_hop = next_hop
        self.destination = destination
        self.timeout
        self.garbage_timer
        self.change_flag
        
class RIP_Entry:
    
    def __init__(self, address_family, source, metric):
        self.address_family = address_family
        self.source_router = source
        self.metric = metric
        