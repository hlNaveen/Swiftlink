import socket
from swiftlink_protocol import create_swiftlink_message, parse_swiftlink_message

def swiftlink_client(host: str, port: int, device_id: int, session_id: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sequence_number = 1
    payload = b'Hello, SwiftLink!'
    message = create_swiftlink_message('D', device_id, session_id, sequence_number, payload)
    
    sock.sendto(message, (host, port))
    data, _ = sock.recvfrom(1024)
    
    try:
        response = parse_swiftlink_message(data)
        print(f"Received response: {response}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    swiftlink_client('127.0.0.1', 5000, 1, 1)
