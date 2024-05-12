import mido

port = mido.open_output()

print(mido.get_output_names())

PORT = 'Akai LPK25 Wireless:Akai LPK25 Wireless MIDI 1 24:0'

with mido.open_input(PORT) as listener:
    for input in listener:
        if not input.is_meta and input.type == 'note_on':
            print(f"Received {input.note}")
