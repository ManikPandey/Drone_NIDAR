import socket
import json
import time
from typing import Union

# Use a broadcast address to send to all devices on the network.
# This is simple and effective for a local network environment.
BROADCAST_IP = '<broadcast>'
COMMS_PORT = 12345

class ScoutComms:
    """
    Handles sending all messages from the Scout drone.
    """
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Enable broadcasting mode for the socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print(f"[COMMS] ScoutComms sender initialized. Broadcasting to port {COMMS_PORT}")

    def send_survivor_location(self, latitude: float, longitude: float):
        """Packages and sends a survivor's coordinates."""
        message = {
            'type': 'survivor_location',
            'lat': latitude,
            'lon': longitude,
            'timestamp': time.time()
        }
        self._send(message)

    def send_mission_complete_signal(self):
        """
        Sends the critical signal indicating the scout has finished its entire
        survey mission. This is the trigger for the delivery drone.
        """
        print("[COMMS] Sending Scout Mission Complete signal.")
        message = {'type': 'scout_mission_complete', 'timestamp': time.time()}
        self._send(message)

    def _send(self, message: dict):
        """Private helper function to encode and send any message."""
        payload = json.dumps(message).encode('utf--8')
        try:
            self.sock.sendto(payload, (BROADCAST_IP, COMMS_PORT))
        except Exception as e:
            print(f"[COMMS] Error sending message: {e}")


class DeliveryComms:
    """
    Handles receiving all messages on the Delivery drone.
    """
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind to the port to listen for incoming messages
        self.sock.bind(('', COMMS_PORT))
        # Set to non-blocking to prevent the main loop from freezing
        self.sock.setblocking(False)
        print(f"[COMMS] DeliveryComms receiver initialized. Listening on port {COMMS_PORT}")

    def check_for_message(self) -> Union[dict, None]:
        """
        Checks for any new message. Returns the message dictionary if received,
        otherwise returns None. This is non-blocking.
        """
        # FIX for Python 3.8 compatibility: Uses 'Union' instead of '|'
        try:
            data, addr = self.sock.recvfrom(1024) # Buffer size
            message = json.loads(data.decode('utf-8'))
            print(f"[COMMS] Received message of type '{message.get('type')}' from {addr}")
            return message
        except BlockingIOError:
            # This is not an error, it simply means no message is waiting.
            return None
        except (json.JSONDecodeError, KeyError) as e:
            # This handles corrupted or improperly formatted messages.
            print(f"[COMMS] Error decoding message packet: {e}")
            return None