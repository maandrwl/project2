import socket

# define ports and host URLs

PORT_RESTAPI = "8000"
PORT_STAGE2 = "5002"
PORT_STAGE3 = "5003"
PORT_STAGE4 = "5004"

# hostnames as defined in docker-compose.yml
BASE_URL_RESTAPI = f"http://project-service:{PORT_RESTAPI}"
BASE_URL_STAGE2 = f"http://stage2-service:{PORT_STAGE2}"
BASE_URL_STAGE3 = f"http://stage3-service:{PORT_STAGE3}"
BASE_URL_STAGE4 = f"http://stage4-service:{PORT_STAGE4}"
URL_RESTAPI_COMPILE = f"http://project-service:{PORT_RESTAPI}/api/compile/"
URL_RESTAPI_PROBLEM = f"http://project-service:{PORT_RESTAPI}/api/problem/"

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
