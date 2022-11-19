


import sys
def filter(filename) :
	print('called filter function in filter_packets.py')
	original_filename = filename.split(".")
	new_filename = original_filename[0] + "_filtered.txt"
	unfil_packets = open(filename, "r")
	fil_packets = open(new_filename, "a")
	
	ln = unfil_packets.readline()
	while ln:
		if "unreachable" not in ln:
			if "ICMP" in ln:
				fil_packets.write(ln)
		ln = unfil_packets.readline()
