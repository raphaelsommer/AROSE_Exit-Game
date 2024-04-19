import mido

PORT = 'Akai LPK25 Wireless:Akai LPK25 Wireless MIDI 1 20:0'

with mido.open_input(PORT) as listener:
    for input in listener:
        if not input.is_meta and input.type == 'note_on':
            print(f"Received {input.note}")