import socket
import configparser
import sys
from functions import parse_ports, create_table

def main(argv):
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
        update = int(config['TIMER']['update'])
        
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
        
        if timeout / update != 6:
            raise ValueError('Incorrect timeout/update timer ratio')
        
    except ValueError as e:
        print('ERROR: ' + str(e))
        sys.exit()
        
    for port in input_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', port))
        
    out_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    out_sock.bind(('127.0.0.1', 6300))
    
    routing_table = create_table(output_costs, output_routerids, output_ports)

if __name__ == '__main__':
    sys.exit(main(sys.argv))


