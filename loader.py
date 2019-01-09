import enum
from scipy.io import wavfile

magic_bytes = {
    'wav': bytes([0x52, 0x49, 0x46, 0x46]),
    'midi': bytes([0x4D, 0x54, 0x68, 0x64])
}


class InputType(enum.Enum):
    AUDIO, MIDI, TEXT = 1, 2, 3


def load(fn):
    with open(fn, 'rb') as fd:
        file_head = fd.read(max([len(b) for b in magic_bytes.values()]))
    if file_head.startswith(magic_bytes['wav']):
        sr, data = wavfile.read(fn)
        # Check other 0x00, 0x00, 0x00, 0x00, 0x57, 0x41, 0x56, 0x45, 0x66, 0x6D, 0x74, 0x20]
        return InputType.AUDIO, {'sr': sr, 'data': data}
    if file_head.startswith(magic_bytes['midi']):
        return InputType.MIDI, {'data': ""}
    else:
        return InputType.TEXT, {'data': ""}
