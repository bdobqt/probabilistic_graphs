import argparse
import PGraph
import branchandbound
import s

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--random", type=int, nargs=2, help="Random G(v,e)")
parser.add_argument("-l", "--load", default='', nargs=1, help="Load graph from input")
parser.add_argument("-k", "--topk", help="Assign the number of top maximal cliques",default=3, type=int)
parser.add_argument("-s", "--size", help="Assign the required size of each clique",default=3, type=int)
parser.add_argument("-del", "--delete", help="Delete all local files", default=0)
args = parser.parse_args()

if args.random:
    Gobject = PGraph.ProbabilityGraph(None,args.random[0],args.random[1])
    bnb1 = branchandbound.Bnb(args.topk, args.size, Gobject)
    bnb1.branch_and_bound()
if args.load:
    Gobject = s.test1(args.load)
    bnb1 = branchandbound.Bnb(args.topk, args.size, Gobject)
    bnb1.branch_and_bound()
if args.delete == 'True':
    print(args.delete)



