import pandas as pd

def CovarianceReduction(input_csv,output_csv):

    # Input and output file paths
    input_csv = "TLE_Covariance_RIC5.csv"
    output_csv = "TLE_PosUnc.csv"

    # Read the CSV
    df = pd.read_csv(input_csv)

    # Columns to keep
    columns_to_extract = [
        "satellite_name",
        "norad_id",
        "C_pR_pR",
        "C_pI_pI",
        "C_pC_pC"
    ]

    # Extract subset
    df_subset = df[columns_to_extract]

    # Write to new CSV
    df_subset.to_csv(output_csv, index=False)

    print(f"Saved position uncertainty data to {output_csv}")