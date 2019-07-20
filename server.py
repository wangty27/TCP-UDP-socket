import sys
import socket
from contextlib import closing

# References:
#

# Function for creating a UDP socket for message transaction with the client
def genTransSocket(client_socket):
  # Create new UDP socket and bind to a randomly assigned avaliable port
  t_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  t_socket.bind(('', 0))
  t_addr, t_port = t_socket.getsockname()

  # Send the UDP port number to the client
  client_socket.send(str(t_port).encode())
  client_socket.close()
  # Set UDP socket timeout to 30 seconds
  t_socket.settimeout(30)

  # Start waiting for UDP message
  # Using try/except to prevent timeout exception and other errors crashing the server
  try:
    client_message, client_addr = t_socket.recvfrom(1024)
  except:
    # Error case, the connection is lost (Timeout) or the message is invalid
    return

  # Change the message case to uppercase then send it back to the client
  client_modmessage = client_message.decode()[::-1]
  t_socket.sendto(client_modmessage.encode(), client_addr)
  t_socket.close()


# Function for creating a TCP socket for negotiating the transaction port with the client
def genNegSocket(req_code):
  # Check if request code is a number
  try:
    req_code_check = int(req_code)
  except:
    print('Error: the request code must be a number')
    sys.exit(2)

  # Open TCP socket and bind to a randomly assigned avalible port
  n_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  n_socket.bind(('', 0))
  n_addr, n_port = n_socket.getsockname()
  print('SERVER_PORT={}'.format(n_port))

  # Start listening for connections
  n_socket.listen(1)
  while True:
    # Block while waiting for client connection
    client_socket, client_addr = n_socket.accept()

    # After connection with a client is established, set the timeout to be 30 seconds
    client_socket.settimeout(30)

    # Using try/except to prevent timeout exception crashing the server
    try:
      client_req_code = client_socket.recv(1024).decode()
    except socket.timeout:
      # Close the connection after timeout
      client_socket.send('Error: connection timeout, connection closed'.encode())
      client_socket.close()
      continue
    if not client_req_code:
      # Prevent server crashing from errors (Client sending invalid request code or losing connection)
      continue
    elif not client_req_code == req_code:
      # Send an error message to the client if the request code is not matched and close the socket
      client_socket.send('Error: wrong req_code is supplied, connection closed'.encode())
      client_socket.close()
    else:
      # Request code is successfully matched, create new UDP socket
      client_socket.settimeout(None)
      genTransSocket(client_socket)



# Check if the correct number of command line parameters are correctly supplied
if not len(sys.argv) == 2:
  print('Error: the number of parameter supplied is incorrect, only one is allowed (req_code)')
  sys.exit(2)

genNegSocket(sys.argv[1])