from argparse import ArgumentParser
from detectives.mapping import string_to_detective as mapping
from scipy.io import wavfile
import loader


def main():
    parser = ArgumentParser()
    parser.add_argument('filename', nargs='+')

    detective_arg = 'bpm_constant'

    args = parser.parse_args()

    for fn in args.filename:
        print('Analysing file: {0}'.format(fn))

        typ, data = loader.load(fn)

        detective = mapping[detective_arg](data['data'])

        if typ == loader.InputType.AUDIO:
            result = detective.audio(data['sr'])
            print(result)
        else:
            print("Not supported file")


if __name__ == '__main__':
    main()
