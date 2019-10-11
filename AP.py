import argparse
import Probability_Graph
import Algorithm_dfs
import File_Loader
import time
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--random", type=int, nargs=2, help="Random G(v,e)")
parser.add_argument("-l", "--load", default='', nargs=1, help="Load graph from input")
parser.add_argument("-k", "--topk", help="Assign the number of top maximal cliques",default=3, type=int)
parser.add_argument("-s", "--size", help="Assign the required size of each clique",default=3, type=int)
parser.add_argument("-del", "--delete", help="Delete all local files", default=0)
args = parser.parse_args()

if args.random:
    if __name__ == "__main__":
        f = open("times.txt","a")
        f.write("Filename : Random({0},{1}) s : {2}, k : {3} \n".format(args.random[0],args.random[1],args.size,args.topk))
        f.close()
        start_prep = time.time()
        Gobject = Probability_Graph.ProbabilityGraph(None, args.random[0], args.random[1])
        bnb1 = Algorithm_dfs.Algorithm(args.topk, args.size, Gobject)
        end_prep = time.time()
        prep_dur = end_prep - start_prep
        start_alg = time.time()
        bnb1.branch_and_bound()
        end_alg = time.time()
        alg_dur = end_alg - start_alg
        f = open("times.txt", "a")
        f.write("Preparation : {0} \n".format(str(datetime.timedelta(seconds=prep_dur))))
        f.write("Algorithm : {0} \n\n".format(str(datetime.timedelta(seconds=alg_dur))))
        f.write("\n")
        f.close()

if args.load:
    f = open("times.txt", "a")
    f.write("Filename : {0}, s : {1}, k : {2} \n".format(args.load[0], args.size, args.topk))
    f.close()
    start_prep = time.time()
    filename = 'stats_' + args.load[0]
    Gobject = File_Loader.loading(args.load)
    bnb1 = Algorithm_dfs.Algorithm(args.topk, args.size, Gobject)
    end_prep = time.time()
    prep_dur = end_prep - start_prep
    start_alg = time.time()
    bnb1.branch_and_bound()
    end_alg = time.time()
    alg_dur =  end_alg - start_alg
    f = open("times.txt", "a")
    f.write("Preparation : {0} \n".format(str(datetime.timedelta(seconds=prep_dur))))
    f.write("Algorithm : {0} \n".format(str(datetime.timedelta(seconds=alg_dur))))
    f.write("\n")
    f.close()

if args.delete == 'True':
    print(args.delete)

