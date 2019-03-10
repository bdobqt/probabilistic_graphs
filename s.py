def importfiles(self):
    alllines = []
    directory = 'datasets'
    wd = os.getcwd()
    G = nx.Graph()
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(file)
            if file.endswith('.txt'):
                f = open(wd + '\\' + directory + '\\' + file, 'r')
                for line in f:
                    lines = line.rstrip('\n')
                    lines = lines.split()
                    alllines.append(lines)
                # G = ts.convertListToGraph(alllines)
                f.close()
            # ts.writeGtoFile(G,file)
            alllines = []


def showmenuandload(self):
    wd = os.getcwd()
    i = 1
    for root, dirs, files in os.walk(wd):
        for file in files:
            if file.endswith('.pickle'):
                print(str(i) + '. ' + str(file))
                with open(wd + '\\' + file, 'rb') as handle:
                    b = pickle.load(handle)
                handle.close()
                i = i + 1
    self.G = b
    # print(self.G.nodes(data = True))