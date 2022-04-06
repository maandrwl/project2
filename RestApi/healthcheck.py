# Simple health check
import socket
import requests

import ApiUrls


PORT_NOT_OPEN = "1023"


def is_port_open(host, port):
    # in python3, socket already works as a context manager
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # for localhost, it should not take long to timeout
    # unless under heavy load
    sock.settimeout(1)
    res = sock.connect_ex((host, int(port)))
    return res == 0


host = "localhost"
if is_port_open(host, ApiUrls.PORT_RESTAPI):
    PORT = ApiUrls.PORT_RESTAPI
elif is_port_open(host, ApiUrls.PORT_STAGE2):
    PORT = ApiUrls.PORT_STAGE2
elif is_port_open(host, ApiUrls.PORT_STAGE3):
    PORT = ApiUrls.PORT_STAGE3
elif is_port_open(host, ApiUrls.PORT_STAGE4):
    PORT = ApiUrls.PORT_STAGE4
else:
    # should not reach here
    PORT = NOT_OPEN_PORT


URL = f"http://{host}:{PORT}"
res = requests.get(URL)

# TODO: should check for request response
#       for now, check only if the port is open
if PORT != PORT_NOT_OPEN:
    print(f"Status: OK")
    exit(0)
else:
    print(f"Status: ERROR")
    exit(1)
