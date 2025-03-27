In Log We Trust
===============

## Folder Structure:
```
in_logo_we_trust/          # Project root
|-- logo_the_server.py     # Main entry point
|-- handler.py             # Handles client connections
|-- log_message.py         # Defines the LogMessage class
|-- forwarder.py           # Sends processed logs to the centralized logging server
|-- config.py              # Stores configuration constants
```

## How to use:
### Before Running: 
- Ensure Python is installed (I've used 3.12)
- Make sure port 1313 is free
 
### How to run:
1. Run the main entry point in logo_the_server.py and the server will start
2. Send a log messages to the configured port
    - Message can contain instructions for IP/Port of the centralized logging service with this convention in the beginning of the message: `[IP=____][PORT=____]`
3. Check the Logs

## Run Example:
In bash run this to run Logo:
```
python logo_the_server.py
```

After that you can use simple Python code to send messages, for example:
```
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 1313))
client.sendall(b"Very important log content")
client.close()
```


## Basic Assumptions
- Since we're dealing with logs, I assumed that the message content isn't binary data but needs to be readable, so I figured it's encoded in UTF-8.