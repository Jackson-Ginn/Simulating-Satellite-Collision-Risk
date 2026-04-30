import time
import csv
import numpy as np
from sgp4.api import Satrec

def tleCovariance(*dataFiles):
    def getData(txtFile):
        with open(txtFile, "r") as f:
            return f.readlines()

    def storeCSV(fileName, rows, header):
        with open(fileName + ".csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)

    def tleTriplesToDict(TLEdata, minMeanMotion=0.9):
        tleDict = {}

        for i in range(0, len(TLEdata), 3):
            try:
                name = TLEdata[i].strip()
                line1 = TLEdata[i + 1].rstrip("\n")
                line2 = TLEdata[i + 2].rstrip("\n")

                if line1[0] != "1" or line2[0] != "2":
                    continue

                meanMotion = float(line2[52:63])

                # Remove objects beyond/near GEO
                # GEO mean motion is about 1 rev/day, so 0.9 adds padding.
                if meanMotion < minMeanMotion:
                    continue

                satID = line1[9:16].strip()
                tleDict[satID] = [name, line1, line2]

            except (IndexError, ValueError):
                pass

        return tleDict

    def makeSatrec(tleTriple):
        return Satrec.twoline2rv(tleTriple[1], tleTriple[2])

    def getEpochJD(sat):
        return sat.jdsatepoch, sat.jdsatepochF

    def propagateSat(sat, jd, fr):
        e, r, v = sat.sgp4(jd, fr)
        if e != 0:
            return None, None
        return np.array(r, dtype=float), np.array(v, dtype=float)

    def getRSWframe(r, v):
        rmag = np.linalg.norm(r)
        if rmag == 0:
            return None

        Rhat = r / rmag

        h = np.cross(r, v)
        hmag = np.linalg.norm(h)
        if hmag == 0:
            return None

        What = h / hmag
        Shat = np.cross(What, Rhat)

        return np.array([Rhat, Shat, What], dtype=float)

    def inertialToRSW(T, vec):
        return T @ vec

    def covarianceFromTLEs(tleList, referenceIndex):
        sats = [makeSatrec(tle) for tle in tleList]

        # Use epoch of the last file as common comparison epoch
        jdRef, frRef = getEpochJD(sats[referenceIndex])

        positions = []
        velocities = []

        for sat in sats:
            r, v = propagateSat(sat, jdRef, frRef)
            if r is None or v is None:
                return None

            positions.append(r)
            velocities.append(v)

        positions = np.array(positions, dtype=float)
        velocities = np.array(velocities, dtype=float)

        # Mean reference state
        rRef = np.mean(positions, axis=0)
        vRef = np.mean(velocities, axis=0)

        T = getRSWframe(rRef, vRef)
        if T is None:
            return None

        samples = []

        for i in range(len(tleList)):
            dr = inertialToRSW(T, positions[i] - rRef)
            dv = inertialToRSW(T, velocities[i] - vRef)

            samples.append([
                dr[0], dr[1], dr[2],
                dv[0], dv[1], dv[2]
            ])

        samples = np.array(samples, dtype=float)

        if len(samples) < 2:
            return None

        cov = np.cov(samples, rowvar=False, ddof=1)

        return cov

    ### Main ###

    if len(dataFiles) < 2:
        raise ValueError("Please provide at least two TLE data files.")

    referenceIndex = len(dataFiles) - 1

    # Get text file data into arrays
    t0 = time.monotonic()
    print("Phase 1:")
    TLEarrays = [getData(dataFile) for dataFile in dataFiles]
    t1 = time.monotonic()
    print(f"Phase 1 complete {t1 - t0:.2f} seconds later.")

    # Convert files into dictionaries keyed by NORAD ID
    print("Phase 2:")
    tleDicts = [tleTriplesToDict(TLEarray) for TLEarray in TLEarrays]
    t2 = time.monotonic()
    print(f"Phase 2 complete {t2 - t1:.2f} seconds later.")

    # Find satellites present in every file
    print("Phase 3:")
    commonIDs = set(tleDicts[0].keys())

    for tleDict in tleDicts[1:]:
        commonIDs = commonIDs.intersection(set(tleDict.keys()))

    commonIDs = sorted(list(commonIDs))
    t3 = time.monotonic()
    print(f"Phase 3 complete {t3 - t2:.2f} seconds later.")

    # Compute covariance matrix for each satellite
    print("Phase 4:")
    rows = []

    header = [
        "satellite_name", "norad_id",
        "C_pR_pR", "C_pR_pI", "C_pR_pC", "C_pR_vR", "C_pR_vI", "C_pR_vC",
        "C_pI_pR", "C_pI_pI", "C_pI_pC", "C_pI_vR", "C_pI_vI", "C_pI_vC",
        "C_pC_pR", "C_pC_pI", "C_pC_pC", "C_pC_vR", "C_pC_vI", "C_pC_vC",
        "C_vR_pR", "C_vR_pI", "C_vR_pC", "C_vR_vR", "C_vR_vI", "C_vR_vC",
        "C_vI_pR", "C_vI_pI", "C_vI_pC", "C_vI_vR", "C_vI_vI", "C_vI_vC",
        "C_vC_pR", "C_vC_pI", "C_vC_pC", "C_vC_vR", "C_vC_vI", "C_vC_vC"
    ]

    for satID in commonIDs:
        tleList = [tleDict[satID] for tleDict in tleDicts]

        cov = covarianceFromTLEs(tleList, referenceIndex)
        if cov is None:
            continue

        referenceTLE = tleList[referenceIndex]

        row = [referenceTLE[0], satID]

        for a in range(6):
            for b in range(6):
                row.append(cov[a, b])

        rows.append(row)

    t4 = time.monotonic()
    print(f"Phase 4 complete {t4 - t3:.2f} seconds later.")

    # Store covariance data
    print("Phase 5:")
    storeCSV("TLE_Covariance_RIC5", rows, header)
    tf = time.monotonic()
    print(f"Phase 5 complete {tf - t4:.2f} seconds later.")