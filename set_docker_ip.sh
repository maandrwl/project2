cd Restapi
echo -e "import socket
import os
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
local = f'http://{local_ip}'
STAGE2 = 'http://stage2-service:5001/stage2'
apiFinal = f'{local}:8000/finalStage/'
" > ApiUrls.py
cd ..

cd stage2
echo -e "import socket
import os
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
local = f'http://{local_ip}'
STAGE3 = 'http://stage3-service:5002'
" > ApiUrls.py
cd ..

cd stage3
echo -e "import socket
import os
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
local = f'http://{local_ip}'
STAGE4 = 'http://stage4-service:5003/stage4'
" > ApiUrls.py
cd ..

cd stage4
echo -e "import socket
import os
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
local = f'http://{local_ip}'
" > ApiUrls.py
cd ..