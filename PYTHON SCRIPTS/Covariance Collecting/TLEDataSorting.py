def tleDataSorting(mainTLEdata, compTLEdata1, compTLEdata2):
    def getIntID(TLEdata):
        IDs = []
        for i in range(len(TLEdata)):
            line = TLEdata[i]
            if line[0] != '1': continue
            else:
                IDs.append(line[9:16].strip())
        return IDs

    def getData(txtFile):
        raw_data = []
        with open(txtFile, 'r') as f:
            for row in f:
                raw_data.append(row)
        return raw_data

    def sortData(mainTLE, otherTLE,comp1or2):
        # Put IDs in list from primary data
        IDs = getIntID(mainTLE)

        # Put IDs in list from comprehensive data
        compIDs = getIntID(otherTLE)

        indexes = []
        if comp1or2 == True:
            for z in range(len(IDs)):
                i = compIDs.index(IDs[z])
                indexes.append(i)

        if comp1or2 == False:
            for z in range(len(IDs)):
                i = len(compIDs) - 1 - compIDs[::-1].index(3)
                indexes.append(i)

        
