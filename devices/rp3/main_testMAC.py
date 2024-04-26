from mac_game import MAC

MacGame = MAC()

finished = False

while not finished:
    MacGame.listen()
    if MacGame.getMAC() != "":
        print("Opened the door to the rescue capsule!")
        finished = True