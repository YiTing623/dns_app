import socket
import json

dns_records = {}

def listen():
    UDP_IP = "0.0.0.0"
    UDP_PORT = 53533

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT)

    while True:
        data, addr = sock.recvfrom(1024)
        data = data.decode('utf-8')
        response = None

        request_type, request_data = parse_dns_request(data)

        if request_type == "REGISTER":
            response = register_dns_record(request_data)
        elif request_type == "QUERY":
            response = handle_dns_query(request_data)

        sock.sendto(json.dumps(response).encode('utf-8'), addr)

def parse_dns_request(data):
    parts = data.split()
    request_type = parts[0]
    request_data = {}
    
    for part in parts[1:]:
        key, value = part.split('=')
        request_data[key] = value

    return request_type, request_data

def register_dns_record(data):
    name = data["NAME"]
    dns_records[name] = data
    return 'TYPE=A NAME={0} VALUE={1} TTL=10'.format(data["NAME"], data["VALUE"])

def handle_dns_query(data):
    name = data["NAME"]
    record = dns_records.get(name)
    
    if record:
        return 'TYPE=A NAME={0} VALUE={1} TTL=10'.format(record["NAME"], record["VALUE"])
    else:
        return 'TYPE=A NAME={0} VALUE=Not Found TTL=10'.format(name)

if __name__ == '__main__':
    listen()
