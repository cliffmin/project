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
    # elif nope:
    #     raw_payload.append(nope[0])
    # else:
    #     raw_payload.append(artificial_payload[0])

    return

    for k in artificial_payload:
        # if type(k) == int:
        # j = chr(k)
        # if len(artificial_payload) > len(raw_payload):
        #     raw_payload.append(k)
        #     raw_payload_frequency = frequency(raw_payload)
        if k in raw_payload:
            # while artificial_frequency[k] != raw_payload_frequency[k]:
            #     if artificial_frequency[k] > raw_payload_frequency[k]:
            #         raw_payload.append(k)
            #         raw_payload_frequency = frequency(raw_payload)
            #     if artificial_frequency[k] < raw_payload_frequency[k]:
            #         raw_payload.remove(k)
            #         raw_payload_frequency = frequency(raw_payload)
            # c = copy.copy(raw_payload)
            # c.append(k)
            # cf = frequency(c)
            # if artificial_frequency[k] < cf[k]:
            #     continue
            while artificial_frequency[k] > raw_payload_frequency[k] and len(artificial_payload) > len(raw_payload):
                raw_payload.append(k)
                raw_payload_frequency = frequency(raw_payload)
        else:
            if len(artificial_payload) > len(raw_payload):
                raw_payload.append(k)
                raw_payload_frequency = frequency(raw_payload)
                while artificial_frequency[k] > raw_payload_frequency[k] and len(artificial_payload) > len(raw_payload):
                    raw_payload.append(k)
                    raw_payload_frequency = frequency(raw_payload)





# Your code here ...
