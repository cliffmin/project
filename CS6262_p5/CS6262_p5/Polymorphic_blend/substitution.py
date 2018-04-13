#!/usr/bin/env python2
import struct
import math
import dpkt
import socket
from collections import Counter
from frequency import *


def substitute(attack_payload, substitution_table):
    # attack_payload = 'qpqppqpq'
    # Using the substitution table you generated to encrypt attack payload
    # Note that you also need to generate a xor_table which will be used to decrypt the attack_payload
    # i.e. (encrypted attack payload) XOR (xor_table) = (original attack payload)
    attack_payload = list(attack_payload)

    # Based on your implementattion of substitution table, please prepare result and xor_table as output
    for k, v in substitution_table.items():
        curr_iter = 0
        for i in range(len(attack_payload)):
            if k == attack_payload[i]:
                attack_payload[i] = v[curr_iter % len(v)]
                curr_iter += 1

    xor_table, attack_payload = create_xor_table(substitution_table, attack_payload)
    # b_attack_payload = bytearray(attack_payload)

    return xor_table, attack_payload

def create_xor_table(substitution_table, attack_payload):
    xor_dict = {}
    for k, v in substitution_table.items():
        for m in v:
            xor_dict[m[0]] = k

    xor_table = []
    for m in attack_payload:
        xor_table.append(ord(m[0]) ^ ord(xor_dict[m[0]]))
    # attack_payload = [ord(m[0]) for m in attack_payload]
    attack_payload = [m[0] for m in attack_payload]
    xor_table = [chr(i) for i in xor_table]
    return xor_table, attack_payload

def getSubstitutionTable(artificial_payload, attack_payload):
    # You will need to generate a substitution table which can be used to encrypt the attack body by replacing
    # the most frequent byte in attack body by the most frequent byte in artificial profile one by one

    # Note that the frequency for each byte is provided below in dictionay format. Please check frequency.py for
    # more details
    artificial_frequency = frequency(artificial_payload)
    attack_frequency = frequency(attack_payload)

    sorted_artificial_frequency = sorting(artificial_frequency)
    sorted_attack_frequency = sorting(attack_frequency)
    # sorted_artificial_frequency = [('b', 0.4), ('a', 0.3), ('c', 0.3)]
    # sorted_attack_frequency = [('p', 0.5), ('q', 0.5)]
    # Your code here ...
    substitution_table = {}
    for i in range(len(sorted_artificial_frequency)):
        att = sorted_attack_frequency[i % len(sorted_attack_frequency)]
        att_key = att[0]
        att_freq = att[1]
        reg = sorted_artificial_frequency[i]
        reg_key = reg[0]
        reg_freq = reg[1]
        if att_key not in substitution_table:
            substitution_table[att_key] = [reg]
        else:
            substitution_table[att_key].append(reg)
        sorted_attack_frequency[i if i < len(sorted_attack_frequency) else 0] = (att_key, att_freq / reg_freq)
        if i >= len(sorted_attack_frequency) - 1:
            sorted_attack_frequency = sorted(sorted_attack_frequency, key=lambda x: x[1], reverse=True)

    # You may implement substitution table in your way. Just make sure it can be used in
    # substitute(attack_payload, substitution_table)
    import json
    # print(json.dumps(substitution_table, indent=2))
    return substitution_table


def create_subsitution_table(m, n, last, sdict):
    if last == len(n):
        return sdict

    m = sorted(m, key=lambda x: x[1])
    for i in range(len(m)):
        a = m[i]
        a0 = a[0]
        if a0 not in sdict:
            sdict[a0] = [n[last]]
        else:
            sdict[a0].append(n[last])
        m[i] = (a0, a[1] / n[last][1])
        last += 1

    create_subsitution_table(m, n, last, sdict)


def getAttackBodyPayload(path):
    f = open(path)
    pcap = dpkt.pcap.Reader(f)
    for ts, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        # TASK: Add in the destination address for your attack payload in quotes
        if socket.inet_ntoa(ip.dst) == "192.150.11.111":
            tcp = ip.data
            if tcp.data == "":
                continue
            return tcp.data.rstrip()


def getArtificialPayload(path):
    f = open(path)
    pcap = dpkt.pcap.Reader(f)
    for ts, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        tcp = ip.data
        # TASK: MODIFY THE PORT NUMBERS FOR IRC TRAFFIC(Similar to what you did in read_pcap.py)
        if tcp.sport == 80 and len(tcp.data) > 0:
            return tcp.data
