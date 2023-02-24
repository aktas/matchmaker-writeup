from pwn import *
import time
import networkx as nx
import sys
from colorama import init
from termcolor import colored

def classification(data_list):
    print(colored("[*] ",'green') + f"Öğrenci Sayısı -> {str(len(data_list))}")
    matched_list = []

    G = nx.Graph()

    for i in range(len(data_list)):
        G.add_node('st'+str(i))

    for idx, st in enumerate(data_list):
        for idx2, st2 in enumerate(data_list):
            if idx == idx2:
                continue
            c1 = idx
            c2 = idx2
            if idx <= idx2:
                c2 = c2 - 1
            if idx2 <= idx:
                c1 = c1 - 1
            #print(str(idx) + "|" + str(idx2))
            matched_list.append(('st'+str(idx), 'st'+str(idx2), st[c2]+st2[c1]))

    G.add_weighted_edges_from(matched_list)
    #print(G.nodes)
    eslesme = nx.algorithms.matching.max_weight_matching(G, maxcardinality=True)
    
    matched_str = ""
    for x in eslesme:
        matched_str = matched_str + str(x[0]).replace('st','') + ',' + str(x[1]).replace('st','') + ';'
        matched_str = matched_str + str(x[1]).replace('st','') + ',' + str(x[0]).replace('st','') + ';'

    data = matched_str.strip(';')
    print(colored("[*] ",'green') + "Gönderilecek Veri -> " + data.strip(';'))
    return data.strip(';')

def retrieve_data(host, port):
    # Sunucuya bağlan
    start_time = time.perf_counter()
    conn = remote(host, port)
    i = 1
    while True:
        try:
            data = conn.recvuntil(b'>')[:-1]
        except EOFError:
            print("EOFError")
            sys.exit(0)
        if "ctf" in data.decode():
            print(data)
        # boş bir liste oluşturun
        result = []
        # her satırı \n karakterine göre ayırarak dizi listesine ekleyin
        for line in data.split(b'\n'):
            if line:
                result.append([int(x) for x in line.split()])

        send_data = classification(result)
        conn.sendline(send_data.encode())
        if i >= 3:
            print(colored("[!] ",'green') + (conn.recvline(1024)).decode() )
            break
        i = i + 1
        time.sleep(3)

        
    conn.close()
    finish_time = time.perf_counter()

    print(colored("[!] ",'green') + 'Program ' + str(round((finish_time - start_time) / 60.0, 2)) + ' saniye sürdü!')

if __name__ == '__main__':
    host = '0.cloud.chals.io'
    port = 22304
    retrieve_data(host, port)