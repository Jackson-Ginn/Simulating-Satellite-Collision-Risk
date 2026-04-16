import time
from TLEDataSorting import tleDataSorting
from TLEDataFiltering import tleDataFiltering
from TLECovariance import tleCovariance

### Section 1: Getting TLE data from comprehensive daily records sourced from SpaceTrak

baseFile1 = "TLE Satellite Data 2026-04-02.txt"
compFile1 = "TLE Satellite Data 2026-04-13 COMP.txt"
compFile2 = "TLE Satellite Data 2026-04-14 COMP.txt"

print("Script 1 Starting...")
t1 = time.monotonic()
tleDataSorting(baseFile1,compFile1,compFile2)
t2 = time.monotonic()
print(f"Script 1 finished after {t2-t1:.2f} seconds.")
print("\n")

### Section 2: Removing any satellites which do NOT appear in all three files

tleFile1 = "TLE Satellite Data 2026-04-13.txt"
tleFile2 = "TLE Satellite Data 2026-04-14.txt"
tleFile3 = "TLE Satellite Data 2026-04-15.txt"

print("Script 2 Starting...")
t2 = time.monotonic()
tleDataFiltering(tleFile1, tleFile2, tleFile3)
t3 = time.monotonic()
print(f"Script 2 finished after {t3-t2:.2f} seconds.")
print("\n")

### Section 3: Calculating covariance for all satellites present in 3 data sets

tleFiltered1 = tleFile1.replace(".txt", " filtered.txt")
tleFiltered2 = tleFile2.replace(".txt", " filtered.txt")
tleFiltered3 = tleFile3.replace(".txt", " filtered.txt")
print("Script 3 Starting...")
t3 =time.monotonic()
tleCovariance(tleFiltered1,tleFiltered2,tleFiltered3)
tf = time.monotonic()
print(f"Script 3 finished after {tf-t3} seconds.")
