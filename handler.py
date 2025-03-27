import logging
from socket import socket

import config
import forwarder
from log_message import LogMessage


def handle_client(client_socket: socket, client_ip: str):
    """
    Handle individual client connection in a separate thread
    """
    try:
        logging.info(f"New connection from {client_ip}")
        data = b""
        while True:
            chunk = client_socket.recv(config.BUFFER_SIZE)
            if not chunk:
                # Stop if the client disconnects
                break
            data += chunk

        if data:
            message = LogMessage(client_ip, data)
            # Forward the message
            forwarder.send_to_centralized_logging_service(message=message, host=config.CENTRALIZED_LOGGING_SERVICE_IP,
                                                          port=config.CENTRALIZED_LOGGING_SERVICE_PORT)
            logging.info(message)


    except Exception as e:
        logging.error(f"Error handling client {client_ip}: {e}")

    finally:
        client_socket.close()
        logging.info(f"Connection from {client_ip} closed")
