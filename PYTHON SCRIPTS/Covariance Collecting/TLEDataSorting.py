### This sorts comprehensive data from SpaceTrack.org (daily elsets) into usable 3LE name, line1, line2. 
### Daily elsets data contains multiple tle data for the same satellite but it is the only 'old' data I can get.
import time

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

    def storeData(fileName, TLEarray):
        with open(str(fileName)+".txt", 'w') as f:
            for i in range(len(TLEarray)):
                f.write(str(TLEarray[i]))

    def sortData(mainTLE, otherTLE,comp1or2):
        # Put IDs in list from primary data
        IDs = getIntID(mainTLE)

        # Put IDs in list from comprehensive data
        compIDs = getIntID(otherTLE)

        newTLE = []

        for z in range(len(IDs)):
            try:
                if comp1or2:
                    i = compIDs.index(IDs[z])
                else:
                    i = len(compIDs) - 1 - compIDs[::-1].index(IDs[z])

                newTLE.append(mainTLE[3*z])
                newTLE.append(otherTLE[2*i])
                newTLE.append(otherTLE[2*i+1])
            
            except ValueError:
                pass

        return newTLE
    
    ### Main ###

    # Get text file data into array
    t0 = time.monotonic()
    print("Phase 1...")
    mainTLEarray = getData(mainTLEdata)
    compTLE1array = getData(compTLEdata1)
    compTLE2array = getData(compTLEdata2)
    t1 = time.monotonic()
    print(f"Phase 1 complete after {t1-t0:.2f} seconds.")

    # Sort comprehensive data
    print("Phase 2.1:")
    sortedTLE1 = sortData(mainTLEarray, compTLE1array, True)
    t21 = time.monotonic()
    print(f"Phase 2.1 complete after {t21-t1:.2f} seconds.")

    print("Phase 2.2:")
    sortedTLE2 = sortData(mainTLEarray, compTLE2array, False)
    t22 = time.monotonic()
    print(f"Phase 2.2 complete after {t22-t21:.2f} seconds.")

    t3 = time.monotonic()
    print("Phase 3:")
    # Store this data in TLE format
    storeData("TLE Satellite Data 2026-04-13", sortedTLE1)
    storeData("TLE Satellite Data 2026-04-14", sortedTLE2)
    tf = time.monotonic()
    print(f"Phase 3 complete after {tf-t3:.2f} seconds.")