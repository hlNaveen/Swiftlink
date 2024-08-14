import socket
from swiftlink_protocol import create_swiftlink_message, parse_swiftlink_message

def swiftlink_server(host: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"SwiftLink Server running on {host}:{port}")
    
    while True:
        data, addr = sock.recvfrom(1024)
        try:
            message = parse_swiftlink_message(data)
            print(f"Received message from {addr}: {message}")
            ack_message = create_swiftlink_message('A', message['device_id'], message['session_id'], message['sequence_number'], b'')
            sock.sendto(ack_message, addr)
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    swiftlink_server('127.0.0.1', 5000)
