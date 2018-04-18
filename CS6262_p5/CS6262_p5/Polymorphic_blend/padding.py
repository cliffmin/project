#!/usr/bin/env python2
import struct
import math
import random
from frequency import *
from collections import Counter
import copy

# To simplify padding, you only need to find the maximum frequency difference for each byte in raw_payload and
# artificial_payload, and pad that byte at the end of the raw_payload. Note: only consider the differences when
# artificial profile has higher frequency.
# Depending upon the difference, call raw_payload.append
def padding(artificial_payload, raw_payload):
    padding = ""
    # Get frequency of raw_payload and artificial profile payload
    artificial_frequency = frequency(artificial_payload)
    raw_payload_frequency = frequency(raw_payload)
    sorted_artifical_frequency = sorting(artificial_frequency)
    sorted_raw_payload_frequency = sorting(raw_payload_frequency)

    # Your code here ...
    diffs = []
    nope = []

    for k in raw_payload:
        if k in artificial_frequency and artificial_payload:
            m = raw_payload_frequency[k]
            n = artificial_frequency[k]
            if n > m:
                diffs.append((k, n - m))
        else:
            nope.append(k)
    if diffs:
        max_diff = sorted(diffs)[0]
        raw_payload.append(max_diff[0])


