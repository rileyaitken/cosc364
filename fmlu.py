import socket
import configparser
import sys
import random
import time
import select
from functions import parse_ports, create_table, INFINITY, process_update, send_update, print_routing_table, extract_fields


def main(argv):
    
    loop = True
    
    try:
        configFile = argv[1]
    except (IndexError):
        return 'Missing file name'
    
    try:
        config = configparser.ConfigParser()
        config.read(configFile);
        
        router_id = int(config['ROUTER']['routerid'])
        input_ports_str = config['ROUTER']['inputports']
        outputs_str = config['ROUTER']['outputports']
        timeout = int(config['TIMER']['timeout'])
        update = int(config['TIMER']['update'])
        
        if router_id < 1 or router_id > 64000:
            raise ValueError('Router id is not in the specified range')
        
        input_ports = []
        input_ports_list = input_ports_str.split(',')
        for port in input_ports_list:
            input_port = int(port.strip())
            input_ports.append(input_port)
        
        parse_ports(input_ports)
        
        output_ports = []
        output_costs = []
        output_routerids = []
        outputs = outputs_str.split(',')
        for output in outputs:
            output_info = output.split('-')
            output_ports.append(int(output_info[0]))
            output_costs.append(int(output_info[1]))
            output_routerids.append(int(output_info[2]))
            
        parse_ports(output_ports)
        
        for i in range(0, len(output_ports)):
            for j in range(0, len(input_ports)):
                if output_ports[i] == input_ports[j]:
                    raise ValueError('A pair of input/output ports are equal')
        
        if timeout / update != 6:
            raise ValueError('Incorrect timeout/update timer ratio')
        
    except ValueError as e:
        print('ERROR: ' + str(e))
        sys.exit()
        
    in_socks = []
    for port in input_ports:
        host = socket.gethostname()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))
        in_socks.append(sock)
        
    out_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    routing_table = create_table(output_costs, output_routerids, output_ports, timeout)
    print_routing_table(routing_table)
    
    while loop == True:
        
        time_before = time.time()
        
        #if triggered_updates_table.length > 0:
            #triggered_update(triggered_updates_table)
            
        offset = random.randrange(-200, 200, 1)
        update_timer = update * (1 + (offset / 1000))
        
        readables, writables, exceptionables = select.select(in_socks, [], [], update_timer)

        if readables:
            for sock in readables:
                print("Hello received packet thankyou")
                packet = sock.recv(2**16)
                entries, source_router = extract_fields(packet)
                process_update(routing_table, entries, source_router, output_ports)
            
        time_after = time.time()
        
        for i in range(0, len(routing_table)):
            entry = routing_table[i]
            
            if entry.timeout != 420:
                entry.timeout -= time_after - time_before
                if entry.timeout >= timeout:
                    entry.cost = INFINITY
                    entry.timeout = 420
                    entry.change_flag = 1
                    #triggered_update_table.append(entry)
            else:
                entry.garbage_timer -= time_after - time_before
                if entry.garbage_timer <= 0:
                    delete_route(entry)
            
        send_update(routing_table, output_ports, output_routerids, out_sock, router_id)           
        print_routing_table(routing_table)
                    
        
            
        
        
        
    
    

if __name__ == '__main__':
    sys.exit(main(sys.argv))


