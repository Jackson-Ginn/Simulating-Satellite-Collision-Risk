import time
from TLEDataFiltering import tleDataFiltering
from TLECovariance import tleCovariance
from CovarianceReduction import CovarianceReduction
from CovarianceOutliers import CovarianceOutliers

files = [
    #"TLE Satellite Data 2026-04-21.txt",
    #"TLE Satellite Data 2026-04-24.txt",
    #"TLE Satellite Data 2026-04-26.txt",
    #"TLE Satellite Data 2026-04-27.txt",
    "TLE Satellite Data 2026-04-28.txt",
    "TLE Satellite Data 2026-04-28pm.txt",
    "TLE Satellite Data 2026-04-30.txt",
    "TLE Satellite Data 2026-04-30pm.txt"
]

filtered_files = [
    file.replace(".txt", " filtered.txt")
    for file in files
]

def run_step(name, func, *args):
    print(f"\n{name} Starting...")
    start = time.monotonic()
    result = func(*args)
    end = time.monotonic()
    print(f"{name} finished after {end - start:.2f} seconds.")
    return result


print("Script 1 not needed...")

run_step("Script 2", tleDataFiltering, *files)

run_step("Script 3", tleCovariance, *filtered_files)

input_csv = "TLE_Covariance_RIC5.csv"
output_csv = "TLE_PosUnc.csv"

run_step("Script 4", CovarianceReduction, input_csv, output_csv)

sigmaOutlier = 3

run_step("Script 5", CovarianceOutliers, output_csv, sigmaOutlier, False, False, False)