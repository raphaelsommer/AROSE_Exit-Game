from ip_game import IP

IpGame = IP()

finished = False

while not finished:
    IpGame.listen()
    if IpGame.getIP() != "":
        print("Opened the door to the rescue capsule!")
        finished = True