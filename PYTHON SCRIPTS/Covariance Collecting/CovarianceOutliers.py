import pandas as pd
import numpy as np

def CovarianceOutliers(
    input_csv,
    sigmaOutlier,
    radialMeanOrMed,
    intrackMeanOrMed,
    crosstrackMeanOrMed
):

    df = pd.read_csv(input_csv)

    cov_cols = ["C_pR_pR", "C_pI_pI", "C_pC_pC"]

    col_labels = {
        "C_pR_pR": "radial",
        "C_pI_pI": "in-track",
        "C_pC_pC": "cross-track"
    }

    method_choices = {
        "C_pR_pR": radialMeanOrMed,
        "C_pI_pI": intrackMeanOrMed,
        "C_pC_pC": crosstrackMeanOrMed
    }

    results = {}

    for col in cov_cols:
        df[f"{col_labels[col]}_outlier"] = 0

    for col in cov_cols:
        data = df[col].dropna()

        use_mean = method_choices[col]

        if use_mean:
            center = np.mean(data)
            spread = np.std(data)
            method = "mean/std"
        else:
            center = np.median(data)
            mad = np.median(np.abs(data - center))
            spread = 1.4826 * mad
            method = "median/MAD"

        results[col] = {
            "center": center,
            "spread": spread,
            "method": method
        }

        if spread > 0:
            col_outliers = np.abs(df[col] - center) > sigmaOutlier * spread

            df.loc[col_outliers, f"{col_labels[col]}_outlier"] = 1
            df.loc[col_outliers, col] = center

    summary = pd.DataFrame(results).T
    print("Statistics used:")
    print(summary)

    print("\nOutlier counts by property:")
    for col in cov_cols:
        label = col_labels[col]
        count = df[f"{label}_outlier"].sum()
        print(f"{label}: {count}")

    df.to_csv("TLE_PosUnc_cleaned.csv", index=False)

    print("\nSaved cleaned file as TLE_PosUnc_cleaned.csv")