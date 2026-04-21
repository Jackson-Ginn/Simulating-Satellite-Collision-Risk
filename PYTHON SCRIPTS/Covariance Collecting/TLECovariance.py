### This estimates a per-satellite covariance matrix in the RSW reference frame
### from three filtered 3-line TLE files. For each satellite, all three TLEs are
### propagated to the epoch of the middle file, transformed into the RSW frame,
### and a 6x6 sample covariance matrix is formed from the three [dR,dS,dW,dVR,dVS,dVW]
### samples. The results are saved as a CSV file.
import time
import csv
import numpy as np
from sgp4.api import Satrec

def tleCovariance(dataFile1, dataFile2, dataFile3):
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

    def storeCSV(fileName, rows, header):
        with open(str(fileName) + ".csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for i in range(len(rows)):
                writer.writerow(rows[i])

    def tleTriplesToDict(TLEdata):
        tleDict = {}

        for i in range(0, len(TLEdata), 3):
            try:
                name = TLEdata[i].strip()
                line1 = TLEdata[i+1].rstrip('\n')
                line2 = TLEdata[i+2].rstrip('\n')

                if line1[0] != '1' or line2[0] != '2':
                    continue

                satID = line1[9:16].strip()
                tleDict[satID] = [name, line1, line2]
            except IndexError:
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

        # Rows are the basis vectors of the RSW frame
        T = np.array([Rhat, Shat, What], dtype=float)
        return T

    def inertialToRSW(T, vec):
        return T @ vec

    def covarianceFrom3TLEs(tle1, tle2, tle3):
        sat1 = makeSatrec(tle1)
        sat2 = makeSatrec(tle2)
        sat3 = makeSatrec(tle3)

        # Use epoch of middle file as common comparison epoch
        jd2, fr2 = getEpochJD(sat2)

        r1, v1 = propagateSat(sat1, jd2, fr2)
        r2, v2 = propagateSat(sat2, jd2, fr2)
        r3, v3 = propagateSat(sat3, jd2, fr2)

        if r1 is None or r2 is None or r3 is None:
            return None

        # Simple reference state from mean of the propagated states
        # (practical 3-file approximation)
        rRef = (r1 + r2 + r3) / 3.0
        vRef = (v1 + v2 + v3) / 3.0

        T = getRSWframe(rRef, vRef)
        if T is None:
            return None

        dr1 = inertialToRSW(T, r1 - rRef)
        dv1 = inertialToRSW(T, v1 - vRef)

        dr2 = inertialToRSW(T, r2 - rRef)
        dv2 = inertialToRSW(T, v2 - vRef)

        dr3 = inertialToRSW(T, r3 - rRef)
        dv3 = inertialToRSW(T, v3 - vRef)

        samples = np.array([
            [dr1[0], dr1[1], dr1[2], dv1[0], dv1[1], dv1[2]],
            [dr2[0], dr2[1], dr2[2], dv2[0], dv2[1], dv2[2]],
            [dr3[0], dr3[1], dr3[2], dv3[0], dv3[1], dv3[2]]
        ], dtype=float)

        # Need at least 2 samples; here we have 3
        cov = np.cov(samples, rowvar=False, ddof=1)

        return cov

    ### Main ###

    # Get text file data into array
    t0 = time.monotonic()
    print("Phase 1:")
    TLEarray1 = getData(dataFile1)
    TLEarray2 = getData(dataFile2)
    TLEarray3 = getData(dataFile3)
    t1 = time.monotonic()
    print(f"Phase 1 complete {t1-t0:.2f} seconds later.")

    # Convert files into dictionaries keyed by NORAD ID
    print("Phase 2:")
    tleDict1 = tleTriplesToDict(TLEarray1)
    tleDict2 = tleTriplesToDict(TLEarray2)
    tleDict3 = tleTriplesToDict(TLEarray3)
    t2 = time.monotonic()
    print(f"Phase 2 complete {t2-t1:.2f} seconds later.")

    # Find satellites present in all three files
    print("Phase 3:")
    IDs1 = set(tleDict1.keys())
    IDs2 = set(tleDict2.keys())
    IDs3 = set(tleDict3.keys())

    commonIDs = sorted(list(IDs1 & IDs2 & IDs3))
    t3 = time.monotonic()
    print(f"Phase 3 complete {t3-t2:.2f} seconds later.")

    # Compute covariance matrix for each satellite
    print("Phase 4:")
    rows = []

    header = [
        "satellite_name", "norad_id",
        "C_pR_pR", "C_pR_pI", "C_pR_pC", "C_pR_vR", "C_pR_vI", "C_pR_vC",
        "C_pI_pR", "C_pI_pI", "C_pI_pC", "C_pI_vR", "C_pI_vI", "C_pI_vC",
        "C_pC_pR", "C_pC_pI", "C_pC_pC", "C_pC_vR", "C_rC_vI", "C_pC_vC",
        "C_vR_pR", "C_vR_pI", "C_vR_pC", "C_vR_vR", "C_vR_vI", "C_vR_vC",
        "C_vI_pR", "C_vI_pI", "C_vI_pC", "C_vI_vR", "C_vI_vI", "C_vI_vC",
        "C_vC_pR", "C_vC_pI", "C_vC_pC", "C_vC_vR", "C_vC_vI", "C_vC_vC"
    ]

    for i in range(len(commonIDs)):
        satID = commonIDs[i]

        tle1 = tleDict1[satID]
        tle2 = tleDict2[satID]
        tle3 = tleDict3[satID]

        cov = covarianceFrom3TLEs(tle1, tle2, tle3)
        if cov is None:
            continue

        row = [tle2[0], satID]
        for a in range(6):
            for b in range(6):
                row.append(cov[a, b])

        rows.append(row)

    t4 = time.monotonic()
    print(f"Phase 4 complete {t4-t3:.2f} seconds later.")

    # Store covariance data
    print("Phase 5:")
    storeCSV("TLE_Covariance_RIC", rows, header)
    tf = time.monotonic()
    print(f"Phase 5 complete {tf-t4:.2f} seconds later.")