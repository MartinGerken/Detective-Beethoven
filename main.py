from argparse import ArgumentParser
from detectives.mapping import string_to_detective as mapping
from scipy.io import wavfile


def main():
    parser = ArgumentParser()
    parser.add_argument('filename', nargs='+')

    detective_arg = 'bpm_constant'

    args = parser.parse_args()

    for fn in args.filename:
        print('Analysing file: {0}'.format(fn))

        sr, data = wavfile.read(fn)

        detective = mapping[detective_arg](data)
        result = detective.audio(sr)
        print(result)


if __name__ == '__main__':
    main()
