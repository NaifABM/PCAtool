import re


#Create Node class object
class Node:
    #Source IP for this node
    ip = 0

    #Data size metrics
    totalreq = 0
    requestsrec = 0
    repliesrec = 0
    requestssent = 0
    repliessent = 0
    requestbytessent = 0
    requestbytesrec = 0
    requestdatasent = 0
    requestdatarec = 0

    #Time metrics
    avgrtt = 0
    requestthrough = 0
    requestgoodput = 0
    replydelay = 0

    #Distance metric
    echohop = 0
    
    #Packet counter
    packets = 0

#Identifies if a packet is a request or reply, and after that, whether it was sent from the source IP or an outsite IP and assigns values accordingly
def id(splitpacket, node, lists):
    request = False

    # define the icmp payload
    icmppayload = int(splitpacket[5]) - 42

    # if this packet is an echo request
    if "request" == splitpacket[8]:
        node.totalreq += 1
        request = True
        # find TTL
        ttl = int(splitpacket[11][4:])
        # calculate echo hop from the TTL
        node.echohop += (129 - ttl)
        
        # if the packets IP is the source nodes IP
        if (splitpacket[2] == node.ip):
            #update requests sent, request bytes sent, request data sent and the total RTT
            node.requestssent += 1

            node.requestbytessent += int(splitpacket[5]) #bytes sent 
    
            node.requestdatasent += icmppayload

            #getting total rtt time
            node.avgrtt += rtt(splitpacket, lists, node)

        # if the packets IP is not the source nodes
        else:
            #update requests recieved, requests bytes recieved, request data recieved and the total reply delay
            node.requestsrec += 1

            node.requestbytesrec += int(splitpacket[5])

            node.requestdatarec += icmppayload

            node.replydelay += rtt(splitpacket, lists, node)

    # if this packet is an echo reply
    elif "reply" == splitpacket[8]:
        
        if (splitpacket[2] == node.ip):
            #update replies sent
            node.repliessent += 1

        else:
            #update replies recieved
            node.repliesrec += 1

#Calculated the time between two packets for either rtt or echohop
def rtt(request, lists, node):
    #create a list from the current packet onwards
    limitedlist = lists[node.packets:]
    #assign the ID we are trying to match
    replyid = request[14].strip(')')

    #traverse the packets in the list
    for packet in limitedlist:
        #if the current packets ID matches the one we are looking for
        if replyid == packet.split()[0]:
            #return a float of the reply time - the request time
            return float(packet.split()[1]) - float(request[1])

#Read through the file given and return a list of lines(packets)
def read_data(filename):
    lists = []
    with open(filename) as file:
        for line in file:
            lists.append(line)

    return lists

#Do most of the calls and assignments for the packets
def compute(filename, node, lists):
    print('called compute function in compute_metrics.py')

    #Go through the list packet by packet
    for packet in lists:
        #parse the packet into readable pieces
        splitpacket = packet.split()

        #Call ID method
        id(splitpacket, node, lists)
 
        #increment packet counter every time the loop goes
        node.packets += 1

    #Calculate throughput and goodput
    node.requestthrough = int(node.requestbytessent) / node.avgrtt
    node.requestgoodput = int(node.requestdatasent) / node.avgrtt

    # turning total rtt time, reply delay and echohop into average
    node.avgrtt = round((node.avgrtt / node.requestssent)*1000.0, 2)
    node.replydelay = round((node.replydelay / node.requestsrec)*1000000.0, 2)
    node.echohop = node.echohop / (node.requestssent)
    
    #assigning and rounding out request throughput, goodput and echo hop
    node.requestthrough = round(node.requestthrough/1000.000, 1)
    node.requestgoodput = round(node.requestgoodput/1000.000, 1)
    node.echohop = round(node.echohop, 2)

def output(node, number, filename="output.csv"):
    """
    Outputs a given node into the proper format.
    Params:
     - Node: the node to be processed
     - filename: the file to output to
    """
    file = open(filename, "a") #denotes appending to a file, not overwriting
    
    #first half
    if(number == 1):
        file.write("Node " + str(number) + "\n\n")
    else:
        file.write("\n\nNode " + str(number) + "\n\n")
    file.write("Echo Requests Sent,Echo Requests Received,Echo Replies Sent,Echo Replies Received\n")
    file.write(str(node.requestssent) + "," + str(node.requestsrec) + "," + str(node.repliessent) + "," + str(node.repliesrec) + "\n")
    file.write("Echo Request Bytes Sent (bytes),Echo Request Data Sent (bytes)\n")
    file.write(str(node.requestbytessent) + "," + str(node.requestdatasent) + "\n")
    file.write("Echo Request Bytes Received (bytes),Echo Request Data Received (bytes)\n")
    file.write(str(node.requestbytesrec) + "," + str(node.requestdatarec) + "\n\n")
    #second half
    file.write("Average RTT (milliseconds)," + str(node.avgrtt) + "\n")
    file.write("Echo Request Throughput (kB/sec)," + str(node.requestthrough) + "\n")
    file.write("Echo Request Goodput (kB/sec)," + str(node.requestgoodput) + "\n")
    file.write("Average Reply Delay (microseconds)," + str(node.replydelay) + "\n")
    file.write("Average Echo Request Hop Count," + str(node.echohop) + "\n\n")
    
    file.close()
