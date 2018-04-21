import socket
import configparser
import sys
import random
import time
import select
from functions import parse_ports, create_table, INFINITY, process_update, send_update

def main(argv):
    
    loop = True
    
    try:
        configFile = argv[1]
    except (IndexError):
        return 'Missing file name'
    
    try:
        config = configparser.ConfigParser()
        config.read(configFile);
        
        routerid = int(config['ROUTER']['routerid'])
        input_ports_str = config['ROUTER']['inputports']
        outputs_str = config['ROUTER']['outputports']
        timeout = int(config['TIMER']['timeout'])
        update_timer = int(config['TIMER']['update'])
        
        if routerid < 1 or routerid > 64000:
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
        
        if timeout / update_timer != 6:
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
    
    routing_table = create_table(output_costs, output_routerids, output_ports)
    
    while loop == True:
        time_before = time.time()
        
        offset = random.randrange(-200, 200, 1)
        update_timer = update_timer * (1 + (offset / 1000))
        
        readables, writables, exceptionables = select.select(in_socks, [], [], update_timer)
        
        if not (readables, writables, exceptionables):
            send_update(routing_table, output_ports, out_sock)
            
        time_after = time.time()
        
        for entry in routing_table:
            
            if entry.timeout != 420:
                entry.timeout += time_after - time_before
                if entry.timeout >= timeout:
                    entry.timeout = 420
            else:
                entry.garbage_timer += time_after - time_before
                if entry.garbage_timer >= (timeout * (2 / 3)):
                    delete_route(entry)
                    
        
            
        
        
        
    
    

if __name__ == '__main__':
    sys.exit(main(sys.argv))


