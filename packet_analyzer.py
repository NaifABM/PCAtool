from filter_packets import *
from packet_parser import *
from compute_metrics import *
import sys
import os

def main():
    fn = sys.argv[1]
    filename_sep = fn.split(".")
    filename = filename_sep[0] + "_filtered.txt"


    if( "1" in fn):
        node1 = Node()
        node1.ip = "192.168.100.1"
        n = 1
        nd = node1
    elif( "2" in fn):
        node2 = Node()
        node2.ip = "192.168.100.2"
        n = 2
        nd = node2
    elif( "3" in fn):
        node3 = Node()
        node3.ip = "192.168.200.1"
        n = 3
        nd = node3
    elif( "4" in fn):
        node4 = Node()
        node4.ip = "192.168.200.2"
        n = 4
        nd = node4
    

    filter(fn)
    lists = parse(filename)
    compute(filename, nd, lists)
    os.system("touch output.csv")
    output(nd, n)


if __name__ == "__main__":
    main()