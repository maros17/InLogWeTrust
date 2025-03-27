import concurrent.futures
import logging
import socket

import config
import handler


def start_logo_server():
    """
    Start Logo's server using managed thread pool for concurrently get messages from multiple clients
    """
    # Create the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    logging.info(f"Logo listening on {config.LOGO_IP}:{config.LOGO_PORT}")

    # Create a thread pool executor
    with concurrent.futures.ThreadPoolExecutor(max_workers=config.LOGO_MAX_CLIENTS) as executor:
        try:
            server_socket.bind((config.LOGO_IP, config.LOGO_PORT))
            server_socket.listen(config.LOGO_MAX_CLIENTS)
            while True:
                client_socket, client_address = server_socket.accept()
                client_ip, _ = client_address

                # Pass the socket to be handled in an individual thread
                executor.submit(handler.handle_client, client_socket, client_ip)

        except KeyboardInterrupt:
            logging.info("Server shutting down...")

        finally:
            server_socket.close()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s'
    )
    start_logo_server()
