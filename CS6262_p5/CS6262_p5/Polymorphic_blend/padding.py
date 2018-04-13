#!/usr/bin/env python2
import struct
import math
import random
from frequency import *
from collections import Counter


def padding(artificial_payload, raw_payload):
    padding = ""
    # Get frequency of raw_payload and artificial profile payload
    artificial_frequency = frequency(artificial_payload)
    raw_payload_frequency = frequency(raw_payload)
    for k, v in artificial_frequency.items():
        # if type(k) == int:
        # j = chr(k)
        if k in raw_payload_frequency:
            # while artificial_frequency[k] != raw_payload_frequency[k]:
            #     if artificial_frequency[k] > raw_payload_frequency[k]:
            #         raw_payload.append(k)
            #         raw_payload_frequency = frequency(raw_payload)
            #     if artificial_frequency[k] < raw_payload_frequency[k]:
            #         raw_payload.remove(k)
            #         raw_payload_frequency = frequency(raw_payload)
            while artificial_frequency[k] > raw_payload_frequency[k]:
                raw_payload.append(k)
                raw_payload_frequency = frequency(raw_payload)
        else:
            raw_payload.append(k)
            raw_payload_frequency = frequency(raw_payload)
            while artificial_frequency[k] > raw_payload_frequency[k]:
                raw_payload.append(k)
                raw_payload_frequency = frequency(raw_payload)

# To simplify padding, you only need to find the maximum frequency difference for each byte in raw_payload and
# artificial_payload, and pad that byte at the end of the raw_payload. Note: only consider the differences when
# artificial profile has higher frequency.


# Depending upon the difference, call raw_payload.append


# Your code here ...
