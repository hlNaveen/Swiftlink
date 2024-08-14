import unittest
from swiftlink_protocol import create_swiftlink_message, parse_swiftlink_message

class TestSwiftLinkProtocol(unittest.TestCase):
    
    def test_message_creation_and_parsing(self):
        device_id = 1
        session_id = 1
        sequence_number = 1
        payload = b'Test Message'
        
        message = create_swiftlink_message('D', device_id, session_id, sequence_number, payload)
        parsed_message = parse_swiftlink_message(message)
        
        self.assertEqual(parsed_message['device_id'], device_id)
        self.assertEqual(parsed_message['session_id'], session_id)
        self.assertEqual(parsed_message['sequence_number'], sequence_number)
        self.assertEqual(parsed_message['payload'], payload.decode())
        self.assertEqual(parsed_message['message_type'], 'D')

    def test_invalid_checksum(self):
        device_id = 1
        session_id = 1
        sequence_number = 1
        payload = b'Invalid Checksum'
        
        message = create_swiftlink_message('D', device_id, session_id, sequence_number, payload)
        message = message[:-2] + b'\x00\x00'  # Corrupt the checksum
        
        with self.assertRaises(ValueError):
            parse_swiftlink_message(message)

    def test_invalid_mac(self):
        device_id = 1
        session_id = 1
        sequence_number = 1
        payload = b'Invalid MAC'
        
        message = create_swiftlink_message('D', device_id, session_id, sequence_number, payload)
        message = message[:-1] + b'\x00'  # Corrupt the MAC
        
        with self.assertRaises(ValueError):
            parse_swiftlink_message(message)

if __name__ == '__main__':
    unittest.main()
