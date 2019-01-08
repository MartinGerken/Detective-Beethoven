from .detective import Detective, NoPaycheck
import numpy as np
import matplotlib.pyplot as plt


class BPMConstant(Detective):

    def audio(self, sr):
        return self.input

    def midi(self):
        pass

    def text(self):
        pass
