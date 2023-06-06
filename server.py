# Author: Colin Cummins
# Github Username: augustsunday
# Date: 6/6/2023
# Description:

from socketlib import *

s = ServerSocket()
clientsocket, address = s.accept()
print(f"Accepted connection from {address}:{clientsocket}")