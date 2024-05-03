import socket

class IP:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('0.0.0.0', 1050))
        self.IP_ADDRESS = ""
        self.RIGHT_IP_ADDRESS = "192.168.100.122" 
        self.finished = False

    def getIP(self):
        return self.IP_ADDRESS

    def listen(self):
        
        while not self.finished:
            print("UDP-Server is listening...")
            data, addr = self.server_socket.recvfrom(1024)  # Standard buffer size
            msg = data.decode().split()
            ip = msg[0]
            print(f"Received IP from {addr}: {ip}")  # Debug print
            if ip == self.RIGHT_IP_ADDRESS:
                self.IP_ADDRESS = ip 
                response = "Right IP entered"
                self.server_socket.sendto(response.encode(), addr)
                print("Correct IP received, server stopping...")
                self.finished = True
                self.stop()
                #break
            else:
                response = "Wrong IP entered"
                self.server_socket.sendto(response.encode(), addr)

    def stop(self):
        self.server_socket.close()
        self.IP_ADDRESS = ""
        print("UDP-Server socket closed.")
