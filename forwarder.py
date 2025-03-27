import logging
import socket
from typing import Optional

from log_message import LogMessage


def send_to_centralized_logging_service(host: str, port: int, message: Optional[LogMessage] = None):
    # Init socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)

    # Check if message has instruction of IP/Port for the centralized logging service, if true - use it
    alternative_ip_port = message.check_message_for_config()
    if alternative_ip_port:
        host, port = alternative_ip_port

    # Send the message to the centralized logging service
    try:
        client_socket.connect((host, port))
        client_socket.send(message.final_message)
        logging.info(f"Message forwarded to {host}:{port}")

    except ConnectionRefusedError:
        logging.info(f"Connection to {host}:{port} was refused")

    except Exception as e:
        logging.info(f"An error occurred: {e}")

    finally:
        client_socket.close()
