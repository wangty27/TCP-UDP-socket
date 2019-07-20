import sys
import socket

# Check if the correct number of command line parameters are correctly supplied
if not len(sys.argv) == 5:
  print('Error: the number of parameter supplied is incorrect, only 4 is allowed')
  sys.exit(2)

# Check if the negotiation port number and request code are numbers
try:
  neg_port_check = int(sys.argv[2])
  req_code_check = int(sys.argv[3])
except:
  print('Error: the negotiation port number and request code must be number')
  sys.exit(2)

# Get server address, server port, require code and message from command line input
server_addr = sys.argv[1]
neg_port = int(sys.argv[2])
req_code = sys.argv[3]
message = sys.argv[4]

# Create the TCP socket for negotiation (getting the UDP socket port number)
client_neg_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_neg_socket.connect((server_addr, neg_port))
# Send the request code to the server and wait for response
client_neg_socket.send(req_code.encode())
# Using try/except to detect any errors
# Possible error: message_port_raw is not a number, which means it's an error message
# Display the error message and exit with a non-zero code
try:
  message_port_raw = client_neg_socket.recv(1024).decode()
  message_port = int(message_port_raw)
except:
  print(message_port_raw)
  sys.exit(1)
client_neg_socket.close()

# initiate client UDP socket to send message
client_trans_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_trans_socket.sendto(message.encode(), (server_addr, message_port))
# Set timeout to 30 to prevent client not exiting if server crashes or connection lost
client_trans_socket.settimeout(30)
modified_message, server_addr = client_trans_socket.recvfrom(1024)
client_trans_socket.close()
print(modified_message.decode())