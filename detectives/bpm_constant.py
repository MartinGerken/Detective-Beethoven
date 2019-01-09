from .detective import Detective, NoPaycheck
import numpy as np
import pywt
from scipy.signal import lfilter

LEVELS = 4
SECONDS = 3


class BPMConstant(Detective):

    # based on http://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=21F84EAE182EC9FB519EA8A7FF005821?doi=10.1.1.63.5712&rep=rep1&type=pdf
    # Adjustments like other correlation function were made, cause original papers had very poor perfomance
    # TODO: Clean up this mess
    # TODO: Try to improve speed
    def audio(self, sr):
        # Histogram
        histo = []

        # Downsampling changes sampling rate
        downsampled_sr = (sr / 2 ** (LEVELS - 1))

        # Index-boundaries for min and max bpm
        # Fast Temp -> High frequenzy -> small number in  frequency spectrum -> Ignore all lower than min_inxed
        min_index = int(60 / 220 * downsampled_sr)
        # Analog to min, but slow temp
        max_index = int(60 / 40 * downsampled_sr)

        # SECONDS Windowing
        for sec in range(0, self.input.size, SECONDS * sr):
            step = self.input[sec:min(sec + SECONDS * sr, self.input.size)]
            if step.size == 0:
                break

            # Mono
            window = np.mean(step, axis=1)

            # Results of DWT: Approximation and Detailed
            dwtA = []
            dwtD = []

            # Sum of all levels
            envelope_sum = [0]

            # Each level filters one octave
            for level in range(0, LEVELS):
                # 1) DWT
                # Calc all bands
                if level == 0:
                    [dwtA, dwtD] = pywt.dwt(window, 'db4')
                # Calc next octave based on last
                else:
                    [dwtA, dwtD] = pywt.dwt(dwtA, 'db4')

                # 2) LPF, could be dropped i think
                dwtD = lfilter([0.01], [0.99], dwtD)
                # 3, 4) Downsample and Full Wave Retification
                dwtD = abs(dwtD[::pow(2, LEVELS - level - 1)])

                # 5) normalize with mean AND standard deviation
                mean = np.mean(dwtD)
                sigma = np.std(dwtD)

                dwtD = [(i - mean) / sigma for i in dwtD]

                # Sum up envelopes
                envelope_sum = add_envelope(np.array(envelope_sum), np.array(dwtD))

            # ACRL
            acrl = list(acf(envelope_sum))[min_index:max_index]

            # BPM
            # The best BPM guess corresponds to the strongest amplitude
            bpm_frequencies = np.where(acrl == max(acrl))

            # Equally strong beats
            for bpm_frequency in bpm_frequencies[0]:
                # ACRL has a offset of min_index
                bpm_frequency = bpm_frequency + min_index

                # Calc actual BPM
                bpm = 60. / bpm_frequency * downsampled_sr
                histo.append(bpm)

        # Median, maybe do some gaussian analysis
        return np.median(histo)

    def midi(self):
        pass

    def text(self):
        pass


# https://stackoverflow.com/questions/14297012/estimate-autocorrelation-using-python
def acf(series):
    n = len(series)
    data = np.asarray(series)
    mean = np.mean(data)
    c0 = np.sum((data - mean) ** 2) / float(n)

    def r(h):
        acf_lag = ((data[:n - h] - mean) * (data[h:] - mean)).sum() / float(n) / c0
        return round(acf_lag, 3)

    x = np.arange(n)  # Avoiding lag 0 calculation
    acf_coeffs = map(r, x)
    return acf_coeffs


# adds two arrays, pads out, if too currently to short (adding behind)
def add_envelope(curr, series):
    if not series.size == curr.size:
        curr = np.pad(curr, (0, abs(series.size - curr.size)), mode='constant')
    return np.add(curr, series)
