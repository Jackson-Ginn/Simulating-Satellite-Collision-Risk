import time

def tleDataFiltering(*dataFiles):
    def getIntIDs(TLEdata):
        IDs = []
        for line in TLEdata:
            if line.startswith("1"):
                IDs.append(line[9:16].strip())
        return IDs

    def getData(txtFile):
        with open(txtFile, "r") as f:
            return f.readlines()

    def storeData(fileName, TLEarray):
        with open(fileName + ".txt", "w") as f:
            for line in TLEarray:
                f.write(line)

    def filterData(TLEarrays):
        # Get ID list for each TLE file
        allIDs = [getIntIDs(TLEarray) for TLEarray in TLEarrays]

        # Find IDs which appear in every file
        commonIDs = set(allIDs[0])
        for IDs in allIDs[1:]:
            commonIDs = commonIDs.intersection(set(IDs))

        filteredTLEarrays = []

        for fileIndex, TLEarray in enumerate(TLEarrays):
            IDs = allIDs[fileIndex]
            newTLE = []

            for commonID in commonIDs:
                j = IDs.index(commonID)

                newTLE.append(TLEarray[3 * j])
                newTLE.append(TLEarray[3 * j + 1])
                newTLE.append(TLEarray[3 * j + 2])

            filteredTLEarrays.append(newTLE)

        return filteredTLEarrays

    ### Main ###

    if len(dataFiles) < 2:
        raise ValueError("Please provide at least two TLE data files.")

    # Get text file data into arrays
    t0 = time.monotonic()
    print("Phase 1:")
    TLEarrays = [getData(dataFile) for dataFile in dataFiles]
    t1 = time.monotonic()
    print(f"Phase 1 complete {t1 - t0:.2f} seconds later.")

    # Filter data
    print("Phase 2:")
    filteredTLEarrays = filterData(TLEarrays)
    t2 = time.monotonic()
    print(f"Phase 2 complete {t2 - t1:.2f} seconds later.")

    # Store filtered data
    print("Phase 3:")
    for dataFile, filteredTLE in zip(dataFiles, filteredTLEarrays):
        outputName = dataFile.replace(".txt", "") + " filtered"
        storeData(outputName, filteredTLE)

    t3 = time.monotonic()
    print(f"Phase 3 complete {t3 - t2:.2f} seconds later.")