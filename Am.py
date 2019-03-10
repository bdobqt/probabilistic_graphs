import argparse


parser = argparse.ArgumentParser()
parser.add_argument("v", default=0, help="vertices")
parser.add_argument("e", default=0, help="edges")
parser.add_argument("-r", "--random", help="Random example with v and e", action="count",default=0)
parser.add_argument("-l", "--load", help="load a file", default=0)
args = parser.parse_args()
#print(args.load_e)

if args.random:
    print(args.v)
    print(args.e)
'''
if args.load_e:
    print(args.load_e)
if args.load:
    print(args.load)
'''