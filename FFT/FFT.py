#!/usr/bin/env python

# Source: https://community.splunk.com/t5/Security/Detecting-Beaconing-Using-Fourier-Transform-FFT/m-p/581384#M15813

import numpy as np
import pandas as pd

from base import BaseAlgo

class FFT(BaseAlgo):
    def __init__(self, options):
        # Option checking & initializations here
        pass

    def fit(self, df, options):
        # Fit an estimator to df, a pandas DataFrame of the search results

        s = df[self.target_variable]
        t = df[self.feature_variables]

        fft = np.fft.fft(s)
        T = t[t.columns[0]][1] - t[t.columns[0]][0]
        N = fft.size
        freq = np.linspace(0, 1 / T, N)[:N // 2]
        amp = np.abs(fft)[:N //2 ] * 1 / N

        df = pd.DataFrame({'Frequency': freq, 'Amplitude': amp}, columns=['Frequency', 'Amplitude'])

        return df
