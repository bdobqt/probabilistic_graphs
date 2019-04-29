import os
import PGraph
import pickle

def test1(input):
    files = ' '.join(input)
    files = files.split()
    #print(files)
    for file in files:
        temp = file.replace(".txt","")
        temppickle = temp + str('.pickle')
        if(os.path.isfile(temppickle)):
            PG = loadPGfromFile(temppickle)
            return PG
        else:
            alllines = []
            txtfile = open(file,"r")
            for line in txtfile:
                line = line.rstrip('\n')
                templine = line.split()
                alllines.append(templine)
            txtfile.close()
            PG = PGraph.ProbabilityGraph(alllines, None, None)
            #writePGtoFile(temp, PG)
            return PG
            #save to G kai close arxeia kai trexe bnb

def writePGtoFile(filename, PG):
    with open(filename + '.pickle', 'wb') as handle:
        pickle.dump(PG, handle, protocol=pickle.HIGHEST_PROTOCOL)
    handle.close()

def loadPGfromFile(filename):
    PG = pickle.load(open(filename, "rb"))
    return PG


