import socket

# Create the endpoint to receive data
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# dial the 'phone' to 'call' a server
mysock.connect(('data.pr4e.org', 80))

# tell the server what you want
# "\r\n\r\n is where you add headers"
# encode into UTF-8 format (more efficient than unicode)
cmd = 'GET http://data.pr4e.org/page1.htm HTTP/1.0\r\n\r\n'.encode()
mysock.send(cmd)

# receive and render the information
while True:
    # wait until 512 chars received at a time
    data = mysock.recv(512)
    # if no more data, socket is closed and stop loop
    if len(data) < 1:
        break
    # convert from UTF-8 back to unicode
    print(data.decode(), end=' ')

mysock.close()
