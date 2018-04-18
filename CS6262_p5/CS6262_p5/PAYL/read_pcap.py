import dpkt


def readPcap(fileName, port_neutral="False"):
    payload_list = []
    f = open(fileName, "r")
    pcap = dpkt.pcap.Reader(f)
    for ts, buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            tcp = ip.data
            # Read http payload
            if (tcp.sport == 80 or tcp.dport == 80):  # TASK: Which port ?
                payload = tcp.data
                payload_list.append(str(payload))
            elif (port_neutral == "True"):
                payload = tcp.data
                payload_list.append(str(payload))
        except:
            continue
    return payload_list


def getPayloadStrings():
    payload_list = []

    # HTTP: FOR HTTP PROTOCOL
    list1 = readPcap('HTTP_data/HTTPtext_V1.pcap')
    list2 = readPcap('HTTP_data/HTTPtext_V2.pcap')
    list3 = readPcap('HTTP_data/modified_new3_simple_http.pcap')
    list4 = readPcap('HTTP_data/modified_new4_simple_http.pcap')
    list5 = readPcap('HTTP_data/modified_new5_simple_http.pcap')
    list6 = readPcap('HTTP_data/modified_new6_simple_http.pcap')
    list7 = readPcap('HTTP_data/modified_new_simple_http.pcap')

    payload_list.extend(list1)
    payload_list.extend(list2)
    payload_list.extend(list3)
    payload_list.extend(list4)
    payload_list.extend(list5)
    payload_list.extend(list6)
    payload_list.extend(list7)

    return payload_list


def read_attack_data(filename):
    listl = open(filename)
    listl1 = listl.read()
    return [listl1]
