### How to run the scripts:
* Starting the server: `./server.sh <req_code>`
  
  Example:
  ```bash
  $ ./server.sh 143
  ```
* Starting the client: `./client.sh <server_addr> <n_port> <req_code> <message>`

  Example:
  ```bash
  $ ./client.sh 129.97.167.27 49283 143 "message to be reversed"
  ```
  
### Python version: 
```
Python 2.7.15rc1 (default, Nov 12 2018, 14:31:15)
[GCC 7.3.0] on linux2
```

### Tested on:
* Local machine with Python 2.7
* Student environment in same machine with Python 2.7
  * ubuntu1804-008.student.cs.uwaterloo.ca
* Student environment in 2 different machines with Python 2.7
  * ubuntu1804-008.student.cs.uwaterloo.ca
  * ubuntu1804-002.student.cs.uwaterloo.ca