from flask import Flask, request, jsonify
import json
import socket
import requests

app = Flask(__name__)

DNS_SERVER_IP = "0.0.0.0"
DNS_SERVER_PORT = 53533

@app.route("/home", methods=['GET'])
def home():
    return "Welcome"

def register_with_dns_server(hostname, ip, as_ip, as_port):
    registration_message = f'TYPE=A NAME={hostname} VALUE={ip} TTL=10'

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(registration_message.encode('utf-8'), (as_ip, as_port))
        response, addr = s.recvfrom(1024)

    return response.decode('utf-8')

def query_dns_for_fs_ip(hostname, as_ip, as_port):
    dns_query = {'NAME': hostname, 'TYPE': 'A'}
    message = json.dumps(dns_query).encode('utf-8')

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(message, (as_ip, as_port))
        data, addr = s.recvfrom(2048) 

    response_data = json.loads(data.decode('utf-8'))
    fs_ip = response_data.get("VALUE")

    return fs_ip


@app.route("/register", methods=['PUT'])
def register_fibonacci_server():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = int(data.get('as_port'))

    if not all([hostname, ip, as_ip, as_port]):
        return 'Bad Request', 400

    response = register_with_dns_server(hostname, ip, as_ip, as_port)

    if response == 'Registered':
        return 'Registered with DNS Server', 201
    else:
        return 'Failed to register with DNS Server', 500

def calculate_fibonacci(number):
    try:
        x = int(number)
    except ValueError:
        return 'Bad Format', 400

    result = fibonacci_recursive(x)
    return str(result), 200
    
def fibonacci_recursive(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    number = request.args.get('number')
    return calculate_fibonacci(number)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
