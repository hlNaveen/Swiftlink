import struct
import hashlib

# Constants for the protocol
XOR_KEY = 0x42  # Simple XOR encryption key

def xor_encrypt_decrypt(data: bytes, key: int = XOR_KEY) -> bytes:
    return bytes([b ^ key for b in data])

def calculate_checksum(data: bytes) -> int:
    return sum(data) % 256

def calculate_mac(data: bytes) -> int:
    return hashlib.sha256(data).digest()[0]  # Simplified MAC, only using the first byte

def create_swiftlink_message(message_type: str, device_id: int, session_id: int, sequence_number: int, payload: bytes) -> bytes:
    version = 1
    payload_length = len(payload)
    header = struct.pack('!BBBBBB', version, message_type.encode()[0], device_id, session_id, sequence_number, payload_length)
    encrypted_payload = xor_encrypt_decrypt(payload)
    footer = struct.pack('!BB', calculate_checksum(header + encrypted_payload), calculate_mac(header + encrypted_payload))
    return header + encrypted_payload + footer

def parse_swiftlink_message(data: bytes) -> dict:
    header = data[:6]
    version, message_type, device_id, session_id, sequence_number, payload_length = struct.unpack('!BBBBBB', header)
    payload = xor_encrypt_decrypt(data[6:6 + payload_length])
    checksum, mac = struct.unpack('!BB', data[6 + payload_length:])
    
    # Validate checksum and MAC
    if checksum != calculate_checksum(header + data[6:6 + payload_length]):
        raise ValueError("Invalid checksum")
    if mac != calculate_mac(header + data[6:6 + payload_length]):
        raise ValueError("Invalid MAC")
    
    return {
        'version': version,
        'message_type': chr(message_type),
        'device_id': device_id,
        'session_id': session_id,
        'sequence_number': sequence_number,
        'payload': payload.decode(),
        'checksum': checksum,
        'mac': mac
    }
