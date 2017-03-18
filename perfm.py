import psutil
import time
from time import gmtime, strftime

name = input("Enter testname: ")
lan_interface = input("Enter lan interface name (as in ifconfig): ")

initial_net = psutil.net_io_counters(pernic = True)[lan_interface]
ibytes_sent, ibytes_recv, ipackets_sent, ipackets_recv, _, _, _, _ = initial_net

cpu_data = list()
lan_data = list()

for i in range(10):
    time.sleep(10)
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    cpu_data.append([str(x) for x in cpu_usage])

    netw = psutil.net_io_counters(pernic = True)[lan_interface]    
    nbytes_sent, nbytes_recv, npackets_sent, npackets_recv, _, _, _, _ = netw
    nbytes_sent, nbytes_recv, npackets_sent, npackets_recv = nbytes_sent - ibytes_sent, nbytes_recv - ibytes_recv, npackets_sent - ipackets_sent, npackets_recv - ipackets_recv
    d = [str(x) for x in [nbytes_sent, nbytes_recv, npackets_sent, npackets_recv]]
    lan_data.append(d)


f = open(name, 'a')
ttime = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
f.write(ttime + '\n')
for x in range(len(cpu_data)):
    i = cpu_data[x]
    f.write(str(x) + ',' +  ','.join(i) + '\n')

for x in range(len(lan_data)):
    i = lan_data[x]
    f.write(str(x) + ',' +  ','.join(i) + '\n')

f.close()
