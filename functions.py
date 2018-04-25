import socket
import sched
import time
from struct import Struct

INFINITY = 16
HOST = socket.gethostname()
entry_struct = Struct('!Hiii')
header_struct = Struct('!BBH')

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

def create_table(costs, routerids, outputs, timeout):
    
    routing_table = []
    for i in range(0, len(costs)):
        entry = Route_Entry(costs[i], outputs[i], routerids[i], routerids[i], timeout, (timeout * (2 / 3)), False) #Create an object of class Route_Entry
        routing_table.append(entry) #Add this Route_Entry object to the routing_table
    return routing_table
            
def send_update(routing_table, neighbours, out_socket, router_id):
    for router_port in neighbours:
        routing_table_copy = split_horizon_preverse(routing_table, router_port)
        packet = header_to_bytes(router_id)
        for entry in routing_table_copy:
            packet += entry_to_bytes(entry)
        print(packet)
        out_socket.sendto(packet, (HOST, router_port))
        
def process_update(routing_table, entries, source_router, neighbours):
    if source_router not in neighbours:
        pass
    else:
        for entry in routing_table:
            if entry.destination == source_router:
                src_router_entry = entry
        for rip_entry in entries:
            if rip_entry.metric >= INFINITY or rip_entry.metric < 1:
                pass
            else:
                this_metric = min(rip_entry.metric + src_router_entry[0], INFINITY)
                existing_route = False
                for entry in routing_table:
                    if entry.destination == rip_entry.destination_id:
                        existing_route = True
                        existing_entry = entry
                if existing_route:      
                    if existing_entry.next_hop == source_router:
                        existing_entry.timeout = 0 #Reset timeout to 0
                        if existing_entry.cost != this_metric:
                            existing_entry.cost = this_metric
                            existing_entry.change_flag = True #Set change flag
                else:
                    if this_metric < INFINITY:
                        new_entry = Route_Entry(this_metric, src_router_entry[1], source_router, rip_entry.destination_id, 0, 0, True)
                        routing_table.append(new_entry)
                        
    
def print_routing_table(routing_table):
    print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print(" Dest  Cost  Interface Next-hop Timeout Garbage Change-Flag")    
    for entry in routing_table:
        print("   %d     %d     %d      %d        %d     %d         %d  " % (entry.destination, entry.cost, entry.interface, entry.next_hop, entry.timeout, entry.garbage_timer, entry.change_flag))
    print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    
def split_horizon_preverse(routing_table, neighbour_port):
    for entry in routing_table:
        if entry.interface == neighbour_port:
            entry.cost = INFINITY
    return routing_table
                                                     
class Route_Entry:
    
    def __init__(self, cost, interface, next_hop, destination, timeout, garbage_timer, change_flag):
        self.cost = cost
        self.interface = interface
        self.next_hop = next_hop
        self.destination = destination
        self.timeout = timeout
        self.garbage_timer = garbage_timer
        self.change_flag = change_flag
        
class RIP_Entry:
    
    def __init__(self, address_family, destination, interface, metric):
        self.address_family = address_family
        self.destination_router = destination
        self.interface = interface
        self.metric = metric
          
def header_to_bytes(router_id):
    header = header_struct.pack(
        2, 1, router_id)
    return header
    
def entry_to_bytes(entry):
    rip_entry = entry_struct.pack(
        2, entry.destination, entry.cost, entry.interface)
    return rip_entry
    
def extract_fields(byte_str):
    index = header_struct.size
    command, version, source_router = header_struct.unpack(byte_str[:index])
    if command != 2 or version != 1:
        raise ValueError('Incorrect command/version')
    
    entries = []
    entries_str = byte_str[index:]
    for i in range(entry_struct.size, len(entries_str), entry_struct.size):
        address_family, destination, cost, interface = entry_struct.unpack(entries_str[:i])
        entry = RIP_Entry(address_family, destination, interface, cost)
        entries.append(entry)
            
    return entries, source_router
            
        
        