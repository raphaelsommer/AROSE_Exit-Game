import socket

class MAC:

    MAC_ADDRESS = ""
    RIGHT_MAC_ADRESS = "fe80::ac:0x45:bd45:24fd"

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('0.0.0.0', 1050))

    def getMAC(self):
        return self.MAC_ADDRESS

    def listen(self):
        while self.MAC_ADDRESS == "":
            data, addr = self.server_socket.recvfrom(1050)
            msg = data.decode().split()
            mac = msg[0]
            #print(f"{mac} (received)")
            #print(self.RIGHT_MAC_ADRESS)
            if mac == self.RIGHT_MAC_ADRESS:
                self.MAC_ADDRESS = data.decode()
                response = "Right MAC entered"
                self.server_socket.sendto(response.encode(), addr) 
            else:
                response = "Wrong MAC entered"
                self.server_socket.sendto(response.encode(), addr)

    def stop(self):
        self.server_socket.close()