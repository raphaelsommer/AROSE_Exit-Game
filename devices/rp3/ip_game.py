import socket

class IP:
    def __init__(self):
        # Create a UDP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('0.0.0.0', 1050))  # Bind to all available network interfaces
        self.IP_ADDRESS = ""  # Initialize an empty string to store the received IP address
        self.RIGHT_IP_ADDRESS = "192.168.100.122"  # Predefined correct IP address
        self.finished = False  # Flag to indicate whether the server should continue listening

    def getIP(self):
        return self.IP_ADDRESS

    def listen(self):
        while not self.finished:
            print("UDP-Server is listening...")  # Debug print
            data, addr = self.server_socket.recvfrom(1024)  # Receive data (buffer size: 1024 bytes)
            msg = data.decode().split()  # Split the received message into words
            ip = msg[0]  # Extract the first word (presumably an IP address)
            print(f"Received IP from {addr}: {ip}")  # Debug print
            if ip == self.RIGHT_IP_ADDRESS:
                self.IP_ADDRESS = ip  # Store the correct IP address
                response = "Right IP entered"
                self.server_socket.sendto(response.encode(), addr)  # Send acknowledgment
                print("Correct IP received, server stopping...")  # Debug print
                self.finished = True  # Stop listening
                self.stop()  # Call the stop method to close the socket
            else:
                response = "Wrong IP entered"
                self.server_socket.sendto(response.encode(), addr)  # Send error message

    def stop(self):
        self.server_socket.close()  # Close the server socket
        self.IP_ADDRESS = ""  # Reset the stored IP address
        print("UDP-Server socket closed.")  # Debug print
