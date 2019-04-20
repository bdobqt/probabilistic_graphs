import argparse
import PGraph
import branchandbound
import s
import time

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--random", type=int, nargs=2, help="Random G(v,e)")
parser.add_argument("-l", "--load", default='', nargs=1, help="Load graph from input")
parser.add_argument("-k", "--topk", help="Assign the number of top maximal cliques",default=3, type=int)
parser.add_argument("-s", "--size", help="Assign the required size of each clique",default=3, type=int)
parser.add_argument("-del", "--delete", help="Delete all local files", default=0)
args = parser.parse_args()

if args.random:
    if __name__ == "__main__":
        f = open("results.txt","a")
        f.write(str(args.random) + "\n")
        f.write("Clique size %s " % str(args.size) + "\n")
        f.write("Top %s " % str(args.topk) + "\n")
        start = time.time()
        start1 = time.time()
        Gobject = PGraph.ProbabilityGraph(None,args.random[0],args.random[1])
        end1 = time.time()
        start2 = time.time()
        bnb1 = branchandbound.Bnb(args.topk, args.size, Gobject)
        end2 = time.time()
        start3 = time.time()
        bnb1.branch_and_bound()
        end3 = time.time()
        end = time.time()
        f.write("Creating G  Elapsed time %g seconds \n" % (end1 - start1))
        f.write("BnB intting Elapsed time %g seconds \n" % (end2 - start2))
        f.write("BnB  Elapsed time %g seconds \n" % (end3 - start3))
        f.write("Elapsed time %g seconds \n" % (end - start))
        f.close()

if args.load:
    f = open("results.txt", "a")
    f.write(str(args.load) + "\n")
    f.write("Clique size %s " % str(args.size) + "\n")
    f.write("Top %s " % str(args.topk) + "\n")
    start4 = time.time()
    start = time.time()
    Gobject = s.test1(args.load)
    end = time.time()
    f.write("Loading file Elapsed time %g seconds \n" % (end - start))
    start1 =time.time()
    bnb1 = branchandbound.Bnb(args.topk, args.size, Gobject)
    end1 = time.time()
    f.write("Bnb inting Elapsed time %g seconds \n" % (end1 - start1))
    start2 = time.time()
    bnb1.branch_and_bound()
    end2 = time.time()
    f.write("Bnb   Elapsed time %g seconds \n" % (end2 - start2))
    end4 = time.time()
    f.write("Elapsed time %g seconds \n" % (end4 - start4))
    f.close()

if args.delete == 'True':
    print(args.delete)



