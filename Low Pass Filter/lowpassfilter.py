#!/usr/bin/env python

import sys
import os
import numpy as np
from scipy.signal import butter, lfilter


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from splunklib.searchcommands import dispatch, ReportingCommand, Configuration, Option, validators


def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y



@Configuration(requires_preop=True)
class LowPassFilter(ReportingCommand):
    
    """
    Computes a low pass filter on the column specified in as an argument against time. It assumes 1 seconds intervals in the input rows. Cutoff in Hz.

    Example:
    
    ``index=_internal | timechart count span=1s | lowpassfilter column=count cutoff=0.1 ``
    
    Yields:
       Filtered
    """
    column = Option(require=True, name='column')  # capture the input column name
    cutoff = Option(require=True, validate=validators.Float(0))

    def reduce(self, records):
        all_records = list(records)
        values = [float(all_records[x][self.column]) for x in range(len(all_records))]
        filtered_values = butter_lowpass_filter(values, 0.1, 1)
        for i, record in enumerate(all_records):
            record["Filtered"] = filtered_values[i]
            yield record



if __name__ == "__main__":
    dispatch(LowPassFilter, sys.argv, sys.stdin, sys.stdout, __name__)
