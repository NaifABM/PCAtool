


def parse(filename):
    print('called parse function in packet_parser.py')
    lists = []
    with open(filename) as file:
        for line in file:
            lists.append(line)
    
    return lists