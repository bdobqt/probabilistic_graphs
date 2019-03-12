import argparse
import PGraph
import branchandbound


parser = argparse.ArgumentParser()
parser.add_argument("v", type=int, help="vertices or filename")
parser.add_argument("e", type=int, help="edges")
parser.add_argument("-r", "--random", help="Random G(v,e)",action='count')
args = parser.parse_args()
#print(args.load_e)


if args.random:
    G = PGraph.ProbabilityGraph(None,args.v,args.e)
    bnb1 = branchandbound.Bnb(4, 3, G)
    bnb1.branch_and_bound()





