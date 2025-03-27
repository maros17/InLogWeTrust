import re
from datetime import datetime


class LogMessage:
    raw_message: bytes
    timestamp: datetime
    client_ip: str
    final_message: bytes

    def __init__(self, client_ip: str, message: bytes = b""):
        self.client_ip = client_ip
        self.timestamp = datetime.now()
        self.raw_message = message
        self.decoded_message = self.raw_message.decode('utf-8')
        self.set_final_message()

    def __str__(self):
        return f"{self.timestamp} - Received from ({self.client_ip}): {self.decoded_message}"

    def set_final_message(self):
        """ Add timestamp and client's IP to the message """
        message = f"{self.timestamp} - from ({self.client_ip}): {self.decoded_message}"
        self.final_message = message.encode('utf-8')

    def check_message_for_config(self):
        """
         Check whether message has instructions for IP/Port.
         The convention needs to be in this format in the beginning of the message:
         [IP=____][PORT=____]

         :return: Tuple of (IP, Port) if exists in message, else None
        """
        match = re.match(r"^\[IP=(.*?)\]\[PORT=(.*?)\] (.+)", self.decoded_message)
        if match:
            ip, port, content = match.groups()
            return ip, int(port)
