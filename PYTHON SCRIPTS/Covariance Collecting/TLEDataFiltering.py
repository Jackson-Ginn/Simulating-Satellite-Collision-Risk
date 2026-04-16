### This checks all satellites between three TLE data sets from different times and reduces it to 
### the satellites which are only present in all three of them. The 3 filtered data sets are then
### saved as text files with 'filtered' added to the end.
import time

def tleDataFiltering(dataFile1, dataFile2, dataFile3):
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

    def storeData(fileName, TLEarray):
        with open(str(fileName) + ".txt", 'w') as f:
            for i in range(len(TLEarray)):
                f.write(str(TLEarray[i]))

    def filterData(TLE1, TLE2, TLE3):
        IDs1 = getIntID(TLE1)
        IDs2 = getIntID(TLE2)
        IDs3 = getIntID(TLE3)

        commonIDs = []
        for i in range(len(IDs1)):
            if IDs1[i] in IDs2 and IDs1[i] in IDs3:
                commonIDs.append(IDs1[i])

        newTLE1 = []
        newTLE2 = []
        newTLE3 = []

        for i in range(len(commonIDs)):
            try:
                j1 = IDs1.index(commonIDs[i])
                j2 = IDs2.index(commonIDs[i])
                j3 = IDs3.index(commonIDs[i])

                newTLE1.append(TLE1[3*j1])
                newTLE1.append(TLE1[3*j1+1])
                newTLE1.append(TLE1[3*j1+2])

                newTLE2.append(TLE2[3*j2])
                newTLE2.append(TLE2[3*j2+1])
                newTLE2.append(TLE2[3*j2+2])

                newTLE3.append(TLE3[3*j3])
                newTLE3.append(TLE3[3*j3+1])
                newTLE3.append(TLE3[3*j3+2])

            except ValueError:
                pass

        return newTLE1, newTLE2, newTLE3

    ### Main ###

    # Get text file data into array
    t0 = time.monotonic()
    print("Phase 1:")
    TLEarray1 = getData(dataFile1)
    TLEarray2 = getData(dataFile2)
    TLEarray3 = getData(dataFile3)
    t1 = time.monotonic()
    print(f"Phase 1 complete {t1-t0:.2f} seconds later.")

    # Filter data
    print("Phase 2:")
    filteredTLE1, filteredTLE2, filteredTLE3 = filterData(TLEarray1, TLEarray2, TLEarray3)
    t2 = time.monotonic()
    print(f"Phase 2 complete {t2-t1:.2f} seconds later.")

    # Store filtered data
    print("Phase 3:")
    storeData(dataFile1.replace(".txt", "") + " filtered", filteredTLE1)
    storeData(dataFile2.replace(".txt", "") + " filtered", filteredTLE2)
    storeData(dataFile3.replace(".txt", "") + " filtered", filteredTLE3)
    t3 = time.monotonic()
    print(f"Phase 3 complete {t3-t2:.2f} seconds later.")